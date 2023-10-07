from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO
from Bio import SearchIO
from Bio import AlignIO # <--Like SeqIO but for aligned files I guess

'''
Enterobacterales NCBI taxid: 91347
'''

'''
Takes a fasta file as input, runs protein-protein BLAST for the first sequence in the file
saves results as blastrsults.xml "blastq"

http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec123
https://biopython.org/docs/1.75/api/Bio.Blast.NCBIWWW.html
https://www.reddit.com/r/bioinformatics/comments/4ef5p8/how_to_filter_blast_results_using_biopython/
This is basically all the documentation for blastq I've been able to find so far

Should maybe a way to filter only one per species?
'''
def prot_blast(input_file,evalue):

	input_fa = SeqIO.parse(input_file,"fasta")
	input_seq = next(input_fa) # <- Next chooses the next item in an iterator
	print(f'Blasting sequence: {input_seq.id}...\nBLASTING...')

	result_handle = NCBIWWW.qblast(
		program = 'blastp',
		database = 'nr', # <--- Trying different databases. Next i'm trying uniprot (swissprot)
		sequence = input_seq.seq,
		expect = evalue,
		short_query = False,
		hitlist_size = 10,
		filter = 91347
		)

	blast_xml = result_handle.read()

	with open('BlastResults.xml','w') as save_file:
		save_file.write(blast_xml)
	print('result saved')



'''
Converts xml file to fasta
'''
def xml_fasta(results_name):
	blast = SearchIO.read('BlastResults.xml','blast-xml')
	records = []
	for hit in blast:
		records.append(hit[0].hit)
	SeqIO.write(records,results_name+'.fa','fasta')
	print(f'{len(records)} hits found!')



