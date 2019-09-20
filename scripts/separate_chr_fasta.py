import re
import sys

inputfa = sys.argv[1]

for line in open(inputfa, 'r'):
  line = line.rstrip()
  if re.match(r"^>", line):
    try:
      target.close()
    except:
      print ("Initailized reading the reference fasta file")
    ann = line
    ann = ann.replace(">", "")
    target = open("split_scaff/" + ann, 'w')
  target.write(line + "\n")


