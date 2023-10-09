
'''

This is my FASTA parser. It's an exercise in working with classes in Python. It's a work
in progress.


Can be run from commandline using system arguments in the following format:

python3 fasta_parsing.py [sort_fasta: FASTA to be sorted through] [read_fasta: FASTA to extract species names] [write_handle: Output file handle]

This command will:
1) Write a FASTA composed of all seqeunces from the sort_fasta that contain a species name present in the read_fasta
2) Write a second fasta like the first, except that only the first sequence from a given species is written (nrs means no repeat species)
3) write a file containing all species names found in the read_fasta file
4) prints a short report to terminal describing unique species found


This parser can also be imported into another script to make a Fasta_parser object like so:

import fasta_parsing
parser_obj = fasta_parsing.Fasta_parser()

with the parser_obj, the above functionalities can be used independantly

parser_obj.cross_ref_nrs(sort_fasta,read_fasta,write_handle(optional))
parser_obj.cross_ref(sort_fasta,read_fasta,write_handle(optional))
parser_obj.write_names(read_fasta,names_handle(optional))

to do: currently only searches for names in brackets using the following RegEx: \[.*\]
This only works for Alex's fasta format (he got them from GenBank). Could be tweaked to read other formats

'''
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


	'''
	extract_names reads a fasta and saves any species names it finds to the self.bacteria_names list. Currently it uses RegEx to find characters inside brackets.
	This can be tweaked to find names from any fasta format, but for now it works with the fasta Alex sent me
	'''

	def extract_names(self,read_fasta = None):
		read_file = open(read_fasta,'r')

		for line in read_file.readlines():
			if line[0] == '>':
				match = re.search(r'\[.*\]',line).group()
				match = match[1:-1]
				self.bacteria_names.append(match)

		read_file.close()

	'''
	write_names extracts names from a fasta with the extract_names method (if bacteria_bames is empty), and then saves that list to a file.
	One name per line.
	If bacteria_names is not empty, it will just use whatever is in that list
	'''
	def write_names(self,read_fasta,names_handle = None):

		if len(self.bacteria_names) == 0:
			self.extract_names(read_fasta)
		if names_handle == None:
			names_handle = 'names_from_'+read_fasta+'.txt'

		with open(names_handle,'w') as names_file:
			names_file.write('\n'.join(self.bacteria_names))

	'''
	cross_ref_nrs: cross reference, no repeat species. It takes
		1) a fasta to be sorted through
		2) a fasta containing the names of species of interest (which will be used to build bacteria_names list)
		3) an optional argument for the export file name
	'''
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

	'''
	cross_ref is just like cross_ref_nrs except that it allows for repeated species, if you want to see all of the subspecies in your
	export file
	'''

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

	'''
	report doesn't great as a method. It really only works if both cross_ref and
	cross_ref_nrs have been executed.
	'''

	def report(self):

		set_species = {s for s in self.match_species}

		print(f'\n\n{len(self.match_species)} sequences from species of interest found in {self.sort_fasta} (len match_species)')
		print(f'{len(self.unique_species)} unique species')
		print(f'{len(set_species)} (set comp from match_species)')
		
'''
main function allows this to be executed from the command line, or for a parser object to be
imported to be importe to another script as a variable.

If executed from the command line, it will run every functionality of the class
'''
def main(sort_fasta,read_fasta,write_handle):
	parser_obj = Fasta_filter(sort_fasta,read_fasta,write_handle)
	parser_obj.cross_ref()
	parser_obj.cross_ref_nrs()
	parser_obj.write_names(read_fasta)
	parser_obj.report()


if __name__ == '__main__':
	sort_fasta = argv[1] # The fasta to be sorted through
	read_fasta = argv[2] # The fasta to extract names of species of interest from
	try:
		write_handle = argv[3] # The export file name
	except:
		write_handle = None

	main(sort_fasta,read_fasta,write_handle)


