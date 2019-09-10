import subprocess
import time
for glacier in ["e", "c", "9"]:
	#for coverage in ["hi", "a", "d", "nd", "dtm"]:
	for coverage in ["dtm"]:
		intersect_cmd = "python ogrintersect.py -s {s} -c {c} -url b -out j".format(s=glacier, c=coverage)
		print("running command: {c}".format(c=intersect_cmd))
		time.sleep(5)
		subprocess.call(intersect_cmd, shell=True)

	intersect_cmd = "python ogrintersect.py -s {s} -c sr -url a -out c".format(s=glacier)
