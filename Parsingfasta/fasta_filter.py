
import re
from sys import argv


class Fasta_filter():
	def __init__(self,sort_fasta = None,read_fasta = None ,write_handle = None):
		
		self.read_fasta = read_fasta
		self.sort_fasta = sort_fasta
		self.write_handle = write_handle
		self.bacteria_names=[]
		self.unique_species=[]
		self.match_species = []

	def extract_names(self,read_fasta = None):
		read_file = open(read_fasta,'r')

		for line in read_file.readlines():
			if line[0] == '>':

				try:
					match = re.search(r'OS=[A-Za-z]* [a-z]*',line).group()
					match = match[3::]
					# print('match: '+match)
					self.bacteria_names.append(match)
				except:
					print("Doesn't Match Species Name RegEx:",line)
					continue

				# For Alex's fasta from genbank
				# match = re.search(r'\[.*\]',line).group()
				# match = match[1:-1]
				# self.bacteria_names.append(match)


		read_file.close()

	def write_names(self,read_fasta,names_handle = None):

		if len(self.bacteria_names) == 0:
			self.extract_names(read_fasta)
		if names_handle == None:
			names_handle = 'names_from_'+read_fasta+'.txt'

		with open(names_handle,'w') as names_file:
			names_file.write('\n'.join(self.bacteria_names))


	def cross_ref_nrs(self,sort_fasta = None,read_fasta = None,write_handle = None):

		if self.read_fasta != None:
			read_fasta = self.read_fasta
		if self.sort_fasta != None:
			sort_fasta = self.sort_fasta
		if self.write_handle != None:
			write_handle = self.write_handle
			write_handle = write_handle.split('.')
			write_handle = f'{write_handle[0]}_nrs.{write_handle[1]}'
		if self.write_handle == None and write_handle == None:
			write_handle = 'crossref_nrs_'+sort_fasta

		sort_file = open(sort_fasta,'r')
		write_file = open(write_handle,'w')

		match = False

		if self.bacteria_names == []:
			self.extract_names(read_fasta)

		for line in sort_file.readlines():

			if line[0] == '>':
				for name in self.bacteria_names:
					if re.search(name,line) and self.unique_species.count(name) == 0:
						match = True
						write_file.write(line)
						self.unique_species.append(name)
						break
					else: match = False
			else:
				if match == True:
					write_file.write(line)

		sort_file.close()
		write_file.close()


	def cross_ref(self,sort_fasta = None, read_fasta = None, write_handle = None):

		if self.read_fasta != None:
			read_fasta = self.read_fasta
		if self.sort_fasta != None:
			sort_fasta = self.sort_fasta
		if self.write_handle != None:
			write_handle = self.write_handle
			write_handle = write_handle.split('.')
			write_handle = f'{write_handle[0]}_rs.{write_handle[1]}'
		if self.write_handle == None and write_handle == None:
			write_handle = 'crossref_rs_'+sort_fasta

		sort_file = open(sort_fasta,'r')
		write_file = open(write_handle,'w')
		match = False
		if self.bacteria_names == []:
			self.extract_names(read_fasta)

		for line in sort_file.readlines():
			if line[0] == '>':
				for name in self.bacteria_names:
					if re.search(name,line):
						match = True
						write_file.write(line)
						self.match_species.append(name)
						break
					else: match = False
			else:
				if match == True:
					write_file.write(line)


	def report(self):

		set_species = {s for s in self.match_species}

		print(f'\n\n{len(self.match_species)} sequences from species of interest found in {self.sort_fasta} (len match_species)')
		print(f'{len(self.unique_species)} unique species')
		print(f'{len(set_species)} (set comp from match_species)')
		

def main(sort_fasta,read_fasta,write_handle):

	sort_fasta = argv[1] # The fasta to be sorted through
	read_fasta = argv[2] # The fasta to extract names of species of interest from
	try:
		write_handle = argv[3] # The export file name
	except:
		write_handle = None

	parser_obj = Fasta_filter(sort_fasta,read_fasta,write_handle)
	parser_obj.cross_ref()
	parser_obj.cross_ref_nrs()
	parser_obj.write_names(read_fasta)
	parser_obj.report()


if __name__ == '__main__':
	

	main(sort_fasta,read_fasta,write_handle)


