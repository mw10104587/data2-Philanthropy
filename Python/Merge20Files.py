import os, csv, json


# a file for merging 20 csv files


destdir = '../data'

files = [ f for f in os.listdir(destdir) if os.path.isfile(os.path.join(destdir,f)) ]

keys = []


fieldnames = ["Donor", "Amount", "Type", "Institution", "Year", "Amount class", "Fund", "Project", "Name", "orig_order"]
outputFile = open("../test-data/merge-20.csv", "w")
writer = csv.DictWriter(outputFile, fieldnames = fieldnames)
writer.writeheader()

for csvFileName in files:

	# print csvFile
	if csvFileName == "toy.xlsx" or csvFileName == ".DS_Store":
		continue
	else:
		print csvFileName

	csvFile = open(destdir + "/" + csvFileName, "rU")
	reader = csv.DictReader(csvFile)

	for idx, row in enumerate(reader):
			
		# for key in row:
		# 	if not key in keys:
		# 		keys.append(key)

		writer.writerow(row)


# print json.dumps(keys)