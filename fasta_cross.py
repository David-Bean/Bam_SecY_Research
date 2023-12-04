import re, os
from sys import argv
from Bio import SeqIO

class Fasta_cross():
	def __init__(self):
		self.bacteria_names = []
		self.match_records = {}
		self.ref_descriptions = {}

	def get_names(self,read_file,fasta_type):
		'''
		Pulls names from the the read file. It uses regex to search for names in FASTA descriptions.
		fasta_type argument tells it what kind of regex to use. Add fasta types and their associated
		regex to the regex dictionary as needed. It can take a text file with one name per line as well.
		'''

		regex = {
		'txt' : None,
		'alex' : r'\[(.*)\]',
		'genbank' : r'OS=(\S* \S*)'
		}
		
		if regex[fasta_type] == None:
			with open(read_file) as f:
				self.bacteria_names = [line.strip() for line in f.readlines()]

		with open(read_file) as f:
			self.bacteria_names = re.findall(regex[fasta_type],f.read())
			

	def get_descriptions(self,read_file):
		'''
		Extracts descriptions from FASTA files and builds the self.ref_descriptions dictionary. This dictionary
		allows users to write the output file using the description from the names file instead of the sort file.
		the get_names() method be used first because this method references the self.getnames list to build the
		dictionary.
		'''
		with open(read_file,'r') as f:
			records = SeqIO.parse(read_file,"fasta")
		descriptions = [record.description for record in records]
		for name in self.bacteria_names:
			for description in descriptions:
				match = re.search(name,description)
				if match:
					self.ref_descriptions[name] = description

	
	def cross_ref(self,search_fasta,names,repeat = False):
		'''
		Reads sort file, references self.bactera_names list to extract species of interest from sort file. Saves
		sequences and their descriptions to self.match_species dictionary. If repeat argument is set to false
		only the first sequence from a species of interest will be saved to self.match_species. Otherwise, each
		occurance of a species of interest will be saved.
		'''
		match_species = []
		records = SeqIO.parse(search_fasta,"fasta")
		records = {record.description:str(record.seq) for record in records}

		if repeat == True:
			for name in self.bacteria_names:
				for description in records.keys():
					if re.search(name,description):
						match_species.append(name)
						self.match_records[description] = records[description]

		if repeat == False:
			for name in self.bacteria_names:
				for description in records.keys():
					if name not in match_species and re.search(name,description):
						match_species.append(name)
						self.match_records[description] = records[description]

	def write_fasta(self,records_dict,handle = 'DefaultName.fasta',format = None, ref_descriptions = False):

		with open(handle,'w') as f:
			if ref_descriptions == False:
				for description,sequence in zip(records_dict.keys(),records_dict.values()):
					f.write('>'+description+'\n')
					f.write(sequence+'\n')
			else:
				for name,sequence in zip(self.bacteria_names,records_dict.values()):
					f.write('>'+self.ref_descriptions[name]+'\n')
					f.write(sequence+'\n')

	def align(self,read_fasta):
		'''
		Uses command line to run multiple sequence alignment algorithm. muscle must be installed for this method
		to work.
		'''
		os.system(f"muscle -in {read_fasta} -out aligned_{read_fasta}")

def main():
	obj = Fasta_cross()
	obj.get_names(names_fasta,fasta_type)
	obj.get_descriptions(names_fasta)
	obj.cross_ref(sort_fasta,obj.bacteria_names,repeat =False)
	obj.write_fasta(obj.match_records, handle = out_handle, ref_descriptions = ref_descriptions)
	obj.align(read_fasta = out_handle)

def help():
	msg = "\n\
fasta_cross allows you to use the names from one fasta file to extract names from another. It can be used\
from command line or imported to another script to call methods from the Fasta_cross object individually.\n\n\
executing from the command line requires arguments:\n\
	-names: the handle for the file you extract names from. It can be a FASTA file or a txt file with one bacteria name per line\n\
	-sort: the handle for the file you want to cross reference using said names\n\
	-out: the handle for the output file. You will get two output files. One that is aligned and one that isn't.\n\
	-type: indicates the format used in the sequence descriptions of your -names fasta. This tells the script how to extract names using\n\
	 regular expressions. Current options are alex, genbank, and txt. This is an optional argument. The default is alex\n\
	-noref: is an optional argument. If -noref is typed into the command line, sequences from the -sort file will keep their descriptions\n\
	 otherwise, they will inherit descriptions from the -names file.\n\
	 \n\
	 example commands:\n\
	 	python3 -names enterobacterales.fa -sort BamA_GenBank.fasta -out ent_bam_crossed.fasta -type alex -noref\n"
	print(msg)



if __name__ == '__main__':
	# Default values. Override them with command line arguments
	fasta_type = 'alex'
	ref_descriptions = True # Setting to True by default because Alex is the most likely person to use this
 
	for i,argument in enumerate(argv):
		if argument == '-sort':
			sort_fasta = argv[i+1]
		if argument == '-names':
			names_fasta = argv[i+1]
		if argument == '-out':
			out_handle = argv[i+1]
		if argument == '-type':
			fasta_type = argv[i+1]
		if argument == '-noref':
			ref_descriptions = False
		if argument == 'help':
			help()
	main()


