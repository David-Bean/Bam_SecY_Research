import fasta_parsingSANDBOX as fasta_parsing

parser = fasta_parsing.Fasta_parser()
parser.extract_names('enterobacterales.fa')
parser.cross_ref_nrs('BamA_UniProt.fasta','enterobacterales.fa','cross_ref')