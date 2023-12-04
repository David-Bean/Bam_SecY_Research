import fasta_cross as fb 

blasta = fb.Fasta_cross()
blasta.get_names('enterobacterales.fa','fasta_uniprot')
blasta.cross_ref('BamA_UniProt.fasta',blasta.bacteria_names,repeat =False)
blasta.write_fasta(blasta.match_records,'EGG.fasta')
blasta.align('EGG.fasta')


