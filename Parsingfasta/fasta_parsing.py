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
'''









import re
from sys import argv

# Extracting copying names from Alex's fasta to a names file
with open('enterobacterales.fa') as read_file:
	bacteria_names = []
	for line in read_file.readlines():
		if line[0] == '>':
			match = re.search(r"\[.*\]",str(line)).group()
			match = match[1:-1]
			bacteria_names.append(match)
	with open('enterobacterales_names.txt','w') as write_file:
		write_file.write('\n'.join(bacteria_names))


'''
Filtering UniProt fasta with Alex's names (from the list, not the file)

'''
with open('SecY_Enterobacteriales.fasta') as read_file:
	with open('Cross_referenced.fasta','w') as write_file:
		match = False
		count = 0
		for line in read_file.readlines():
			if line[0] == '>':
				for name in bacteria_names:
					if re.search(name,line):
						count += 1
						match = True
						write_file.write(line)
						break
					else:
						match = False
			else:
				if match == True:
					write_file.write(line)
	
		print(count,'matches')



'''
A version of the cross-referencer that only allows 1 instance per species
'''
with open('SecY_Enterobacteriales.fasta') as read_file:
	with open('Cross_referenced_no_repeated_species.fasta','w') as write_file:
		match = False
		count = 0
		found_species = []
		for line in read_file.readlines():
			if line[0] == '>':
				for name in bacteria_names:
					if re.search(name,line) and found_species.count(name) == 0:
						count += 1
						match = True
						write_file.write(line)
						found_species.append(name)
						break
					else:
						match = False
			else:
				if match == True:
					write_file.write(line)
	
		print(count,'matches filtering repeat species')