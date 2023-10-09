import re
from sys import argv

class Fasta_parser():
	def __init__(self,sort_fasta = None,read_fasta = None ,write_handle = 'crossrefferenced.fasta'):
		self.read_fasta = read_fasta
		self.sort_fasta = sort_fasta
		self.write_handle = write_handle

		self.bacteria_names=[]
		self.unique_species=[]
		self.match_species = []

	def extract_names(self):
		names_handle = 'names_from_'+self.read_fasta+'.txt'
		read_file = open(self.read_fasta,'r')
		name_file = open(names_handle,'w')

		for line in read_file.readlines():
			if line[0] == '>':
				match = re.search(r'\[.*\]',line).group()
				match = match[1:-1]
				self.bacteria_names.append(match)
		name_file.write('\n'.join(self.bacteria_names))
		read_file.close()
		name_file.close()

	def cross_ref_nrs(self):

		nrs_handle = 'nrs_'+self.write_handle
		sort_file = open(self.sort_fasta,'r')
		crossed_file = open(nrs_handle,'w')
		match = False

		for line in sort_file.readlines():
			if line[0] == '>':
				for name in self.bacteria_names:
					if re.search(name,line) and self.unique_species.count(name) == 0:
						match = True
						crossed_file.write(line)
						self.unique_species.append(name)
						break
					else: match = False
			else:
				if match == True:
					crossed_file.write(line)

		sort_file.close()
		crossed_file.close()


	def cross_ref(self):
		sort_file = open(self.sort_fasta,'r')
		crossed_file = open(self.write_handle,'w')
		match = False

		for line in sort_file.readlines():
			if line[0] == '>':
				for name in self.bacteria_names:
					if re.search(name,line):
						match = True
						crossed_file.write(line)
						self.match_species.append(name)
						break
					else: match = False
			else:
				if match == True:
					crossed_file.write(line)

	def report(self):

		set_species = {s for s in self.match_species}

		print(f'\n\n{len(self.match_species)} sequences from species of interest found in {self.sort_fasta} (len match_species)')
		print(f'{len(self.unique_species)} unique species')
		print(f'{len(set_species)} (set comp from match_species)')
		


def main(sort_fasta,read_fasta,write_handle):
	parser_obj = Fasta_parser(sort_fasta,read_fasta,write_handle)
	parser_obj.extract_names()
	parser_obj.cross_ref()
	parser_obj.cross_ref_nrs()
	parser_obj.report()



if __name__ == '__main__':
	sort_fasta = argv[1] # The fasta to be sorted through
	read_fasta = argv[2] # The fasta to extract names of species of interest from
	write_handle = argv[3] # Name of the new fasta

	main(sort_fasta,read_fasta,write_handle)

