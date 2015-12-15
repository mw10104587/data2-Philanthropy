import re


path = "../TO BE PARSED/MoMA2013-14AnnualListing - selected.csv"
with open(path, "r") as inFile:
	with open(path.replace("selected.csv", "wrapped.csv"), "w") as oF:
		for line in inFile:
			if line.find(",") != -1:
				line = '"' + line.replace("\n", "") + '"'
				print line
				oF.write(line + "\n")
			else:
				print line.replace("\n", "")
				oF.write(line)
