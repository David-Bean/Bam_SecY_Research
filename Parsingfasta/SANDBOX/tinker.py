import fasta_filter as fasta_parsing

parser = fasta_parsing.Fasta_filter()
parser.cross_ref_nrs('BamA_UniProt.fasta','enterobacterales.fa','Banana_nrs')
parser.report()


