import re
import sys
import operator
import subprocess
from collections import defaultdict

correction = defaultdict(dict)
bedfile = sys.argv[1]
for line in open(bedfile, 'r'):
  line = line.rstrip()
  if (line.startswith('#') == False):
    array = line.split("\t")
    ann = ">" + array[0]
    pos = int (array[1]) - 1
    if (array[2].lower() == 'indel'):
      array[2] = 'N'
    correction[ann][pos] = array[2]

chrfile = "split_scaff/" + sys.argv[2]
chrfilesingle = chrfile + ".line"
bashCommand = "cat "+ chrfile + " | awk \'{if (substr($0,1,1)==\">\"){if (p){print \"\\n\";} print $0} else printf(\"%s\",$0);p++;}END{print \"\\n\"}\' | sed \'/^$/d\' > " + chrfilesingle
output = subprocess.check_output(['bash', '-c', bashCommand])
ann = ""
target = open("corrected_scaff/" + sys.argv[2] + ".fa", 'w')
for line in open(chrfilesingle, 'r'):
  line = line.rstrip()
  if re.match(r"^>", line):  
    if (len(ann) > 0):
      for pos in correction[ann]:
        seq[pos] = correction[ann][pos]
        corrected_seq = ''.join(seq)
      target.write(ann + "\n" + corrected_seq + "\n")
    ann = line
    seq = []
  else:
    v = [c for c in line]
    seq = seq + v

if (len(ann) > 0):
  for pos in correction[ann]:
    seq[pos] = correction[ann][pos]
  corrected_seq = ''.join(seq)
  target.write(ann + "\n" + corrected_seq + "\n")

