import re
import sys
import operator

inputreadcount = sys.argv[1]+"_readcount.txt"
target1 = open("fixbases1_output/" + sys.argv[1] + ".bed", 'w')
target2 = open("fixbases1_output/" + sys.argv[1] + "_depth_info.tab", 'w')

target1.write("#chr_id\tbase_position\tMaxbase\tReference_base\tA\tC\tG\tT\tN\tIndel_count\tReference_basepercent\tDepth\n")
target2.write("#chr_id\tbase_position\tDepth\tIndelcount\n")

#Defining the criteria used for correction
minreadcoverage = 10
maxreadcoverage = 200
maxindelpercent = 10

for line in open("readcount_bam/"+inputreadcount, 'r'):
  line = line.rstrip()
  array = line.split("\t")
  chrid = array[0]				#chromosome ID
  position = array[1]				#base position
  reference_base = array[2].upper()		#base present in scaffold
  depth = int(array[3])				#depth/coverage at the position
  indelpercent = 0
  indelcount = 0
  #Indel count/percent calculation
  if (len(array) >= 11):
    for i in range(10, len(array), 1):
      indel = array[i].split(":")
      indelcount = int (indel[1]) + indelcount
    indelpercent = int (indelcount) * 100 / int (depth)
  
  if((int (depth) >= minreadcoverage) and (indelpercent <= maxindelpercent) and (int (depth) <= maxreadcoverage)):
    A = array[5].split(":")
    C = array[6].split(":")
    G = array[7].split(":")
    T = array[8].split(":")
    N = array[9].split(":")
    count = {'A' : int(A[1]), 'C' : int(C[1]), 'G' : int(G[1]), 'T' : int(T[1]), 'N' : int(N[1]), 'indel' : int(indelcount)}
    maxbase = max(count, key=count.get)
    maxbasecount = int(count[maxbase])
    maxbasepercent = int (maxbasecount) * 0.2
    reference_basepercent = int (count[reference_base]) * 100 / int (depth)
    if ((int (count[reference_base]) <= maxbasepercent) and (maxbase != 'indel')):
      target1.write(chrid + "\t" + position + "\t" + maxbase + "\t" + reference_base + "\t" + A[1] + "\t" + C[1] + "\t" + G[1] + "\t" + T[1] + "\t" + N[1] + "\t" + str(indelcount) + "\t" + str(reference_basepercent) + "\t" + str(depth) + "\n")
  
  target2.write(chrid + "\t" + position + "\t" + str(depth) + "\t" + str(indelcount) + "\n")

target1.close()
target2.close()
