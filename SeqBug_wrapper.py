
# input1 = genome assembly in fasta format
# input2 = alignment file in sorted BAM format

import sys
import subprocess

scaff = sys.argv[1]
subprocess.call('mkdir split_scaff', shell=True)
subprocess.call('python scripts/separate_chr_fasta.py '+scaff, shell=True)
bamfile = sys.argv[2]

subprocess.call('grep ' + '">" ' + scaff + ' > annot.txt', shell=True)
subprocess.call('sed "s/>//g" annot.txt > Scaffold_list.txt', shell=True)

subprocess.call('samtools index ' + bamfile, shell=True)
subprocess.call('mkdir split_bam readcount_bam fixbases1_output corrected_scaff', shell=True)

f = open("Scaffold_list.txt", 'r')
for line in f:
    line = line.rstrip()
    subprocess.call('samtools view -b ' + bamfile + ' ' + line + ' > split_bam/' + line + '.bam', shell=True)
    subprocess.call('bam-readcount/bin/bam-readcount -w 0 -q 25 -b 25 -d 400 -f ' + scaff + ' split_bam/'+ line +'.bam'+'> readcount_bam/' + line + '_readcount.txt', shell=True)
    subprocess.call('python scripts/identify_assembly_errors.py '+ line, shell=True)
    subprocess.call('python scripts/corrected_scaffolds.py '+'fixbases1_output/'+ line +'.bed '+ line, shell=True)
    subprocess.call('rm split_bam/' + line + '.bam readcount_bam/' + line + '_readcount.txt', shell=True)

# cat all the corrected scffolds
subprocess.call('cat corrected_scaff/*.fa | sed -e "s/.\{60\}/&\\n/g" > corrected_genome.fa', shell=True)
c = subprocess.check_output('cat fixbases1_output/*.bed | grep -v "#" | wc -l | cut -f1 -d" " ', shell=True)
c = str(c.rstrip())
print ("\n#########################################################")
print ("Correction completed. Cleaning files...")
subprocess.call('rm -fr split_bam/ readcount_bam/ split_scaff/ corrected_scaff/', shell=True)
subprocess.call('rm annot.txt Scaffold_list.txt ', shell=True)
print ("\nThe corrected genome assembly corrected_genome.fa has been created.")
print (c+" bases have been corrected.")
print ("The per base statistics of each of the corrected site is available in fixbases1_output directory")
print ("\n Thank you for using SeqBug. If you are using the pipeline for research, please cite us at:")
print ("    Mittal, P., Jaiswal, S.K., Vijay, N., Saxena, R. and Sharma, V.K., 2019. Comparative analysis of corrected tiger genome provides clues to their neuronal evolution. bioRxiv, p.544809.")

