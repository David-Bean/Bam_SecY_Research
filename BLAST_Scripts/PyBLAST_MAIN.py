from sys import argv
import blast_stuff as bs

input_file = argv[1] # takes a fasta file
evalue = argv[2] # Evalue. Quality? I guess? smaller is lower quality
results_name = argv[3]  # Name of results file

"""
Example input:
python3 PyBLAST_MAIN.py EcoliSecy.fa 10 ecoli_blast

returns ecoli_blast.fa
"""

if __name__ == '__main__':
	bs.prot_blast(input_file,evalue)
	bs.xml_fasta(results_name)






	