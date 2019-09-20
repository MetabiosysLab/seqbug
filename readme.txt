SeqBug 

  1. Introduction
This pipeline identifies the single nucleotide errors present in the genome assembly. Such errors are introduced in the assembly by genome assemblers and read error correction tools. It uses a mapping based approach to correct the errors in the genome and outputs the corrected genome assembly. 


  2. Requirement and Input:
It takes as input the reference fasta file and an alignment file in BAM format. The BAM file should be sorted. The program was developed in Python 2.7 on CentOS and is currently restricted to Unix/linux environment. It requires bam-readcount tool (https://github.com/genome/bam-readcount) in the working directory. In case the bam-readcount tool is installed at another location, the location of the tool should be changed at line 22 in scripts/SeqBug _wrapper.py. The program also requires samtools executable in the working directory. To download samtools, please use the link http://www.htslib.org/download/.

Requirements:
 -Python 2.7
 -Unix/linux environment
 -Samtools
 -bam-readcount

 
  3. Installation

      git clone https://github.com/MetabiosysLab/seqbug.git
      cd seqbug
      git clone https://github.com/genome/bam-readcount.git
      cd bam-readcount/
      cmake 
      make
      cd ..


  4. How to use
To run the pipeline, use the command below.

       python SeqBug_wrapper.py <reference.fa> <sorted BAM file>
    
This pipeline has been optimized on a mammalian genome, which was sequenced at 100X using Illumina short reads. These parameters can also be used in genomes sequenced between 30-100X coverage. Currently, the pipeline uses the following parameters:

1. read alignment mapping quality 25
2. base quality 25
3. minimum read coverage 10
4. maximum read coverage 200
5. maximum indel percent 10%

and corrects the base positions if the maximum base (max_base) at a position is atleast five times greater than the ref_base (base present in the <reference.fa>). The first and second parameters can be changed at line 22 in SeqBug_wrapper.py as:
-q <minimum mapping quality> -b <minimum base quality at a position>

The parameters 3, 4, and 5 can be changed at scripts/identify_assembly_errors.py at line 13, 14 and 15, respectively.

Please make sure that the chr name in the reference file is same as present in the bam file. Any discrepansy may lead to error.

  5. Output

The program generates two outputs-
1. Corrected genome assembly (corrected_genome.fa)
2. Per base-position statistics of corrected base (fixbases1_output/<scaffold>.bed)

The .bed file is created for all the scaffolds separated. It contains the following information:
1.  chr_id                       The chromosome id
2.  base_position                The base position corrected
3.  Max_base                     The corrected base
4.  Ref_base                     The base present in the <reference.fa> file
5.  A                            Count of base A at the base_position
6.  C                            Count of base C at the base_position
7.  G                            Count of base G at the base_position
8.  T                            Count of base T at the base_position
9.  N                            Count of base N at the base_position
10. Indel_count                  Count of indels at the base_position
11. Ref_basepercent              Percentage of Reference_base at the base_position
12. Depth                        Depth/Coverage at the base_position

Additionally, the program outputs <scaffold>_depth_info.tab for each scaffold in the fixbases1_output directory. This file provides the coverage information of all the base positions.

  4. Testing
  
There are test files available in the example folder. The file ref.fa is a reference assembly file. The file alignment_sorted.bam is alignment file. To run the test, use the command below.

        python SeqBug_wrapper.py example/ref.fa example/alignment_sorted.bam


For any query, please write to Dr. Vineet K. Sharma (vineetks@iiserb.ac.in)


