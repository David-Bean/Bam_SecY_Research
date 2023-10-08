# from Bio import SeqIO
# with open('enterobacterales.fa') as handle:
# 	seq_obj = SeqIO.parse(handle,'fasta')
# 	for record in seq_obj:
# 		print (record.id)

# with open('SecY_Enterobacteriales.fasta') as handle:
# 	seq_obj = SeqIO.parse(handle,'fasta')
# 	for record in seq_obj:
# 		print(record.id)

# Can't Get SeqIO to do what I want...
# I want to reformat my fasta to look like Alex's, and then only keep Enterobacteriales from his fasta






'''
Feed this script fasta files downloaded from UniProt and it will filter out any species names not
present in Alex's enterobacterales.fa file

note: Have not yet combed over results to make sure this script does not make any mistakes
'''


import re
from sys import argv

extract_names_fasta = argv[1]
filter_fasta = argv[2]
'''
Extracting copying names from Alex's fasta to a names file. Only works for names between brackets
like [Escherichia coli], but could probably be tweaked to grab name from any fasta file.
(only wrote this function because I couldn't figure out how to make SeqIO do this)
'''


names_handle = 'names_'+extract_names_fasta+'.txt'
bacteria_names = []
found_species = []
match_spc_cnt = 0

def extract_names(fasta):
	with open(fasta,'r') as read_file:

		for line in read_file.readlines():
			if line[0] == '>':
				match = re.search(r"\[.*\]",str(line)).group()
				match = match[1:-1]
				bacteria_names.append(match)
		
		with open(names_handle,'w') as write_file:
			write_file.write('\n'.join(bacteria_names))
	# print(len(bacteria_names))



'''
Filtering UniProt fasta with Alex's names (from the list, not the file)
'''
def cross_ref(fasta):
	global match_spc_cnt
	with open(fasta,'r') as read_file:
		with open('crossreferenced.fasta','w') as write_file:
			match = False
			for line in read_file.readlines():
				if line[0] == '>':
					for name in bacteria_names:
						if re.search(name,line):
							match_spc_cnt += 1
							match = True
							write_file.write(line)
							break
						else:
							match = False
				else:
					if match == True:
						write_file.write(line)
		


'''
A version of the cross-referencer that only allows 1 instance per species
nrs: 'no repeat species'
'''

def cross_ref_nrs(fasta):
	with open(fasta,'r') as read_file:
		with open('crossreferenced_nrs.fasta','w') as write_file:
			match = False
			
			for line in read_file.readlines():
				if line[0] == '>':
					for name in bacteria_names:
						if re.search(name,line) and found_species.count(name) == 0:
							match = True
							write_file.write(line)
							found_species.append(name)
							break
						else:
							match = False
				else:
					if match == True:
						write_file.write(line)


if __name__ == '__main__':

	extract_names(extract_names_fasta)
	cross_ref(filter_fasta)
	cross_ref_nrs(filter_fasta)

	print(f'{match_spc_cnt} shared species in fastas')
	bacteria_names_set = {s for s in bacteria_names}
	print(f'{len(bacteria_names)} total bacteria names in {extract_names_fasta}\n{len(bacteria_names_set)} unique bacteria names in {extract_names_fasta}')
	print(f'{len(found_species)} shared species in {extract_names_fasta} and {filter_fasta}')

# Hmm... 120 unique names in name file, but can't ever beat 105 matches. I wonder if 15 if those bacteria aren't in enterobacterales
# yes, even when I run this script with BamA. Either my code is bugged or UniProt thinks some of Alex's bacteria arent' enterobacterales
