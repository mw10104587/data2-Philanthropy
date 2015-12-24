# -*- coding: utf-8 -*-
import csv, json
import sys
import re



def refineDonorNamesForCooper(donor):
	donor = re.sub('[^a-z0-9A-Z\s_]', "", donor)
	return donor
# 
def refineAmountCellFor911(text):
	text = text.replace("level", "")
	text = text.replace(" LEVEL", "")
	text = text.replace("¡X", "-")
	text = text.replace("¡X", "-")

	# for large donation amount, they show the range by using
	# ¡X
	# for small donation amount, they show the range by using
	# -

	if text.count("$") > 1:
		text = re.sub('¡X', "-", text)
		# use regex to replace stuff.
		text = re.sub('[^0-9,$XMILON-]', "", text)
		text = text.replace("X", "-")

	return text


def refineAmountCellForCooper(text):
	text = text.replace("¡V", "-")
	text = re.sub("[^a-z0-9A-Z-$,\s]", "-", text)
	text = text.replace("V", "")

	return text


def refineAmountCellForNYPL(text):
	text = text.replace("Donors of ", "")
	text = re.sub("[()]", "", text)
	text = text.replace(" to ", "-")

	return text.rstrip()


# def refineAmountCellForNYTransit(text):
	# text = 


if __name__ == '__main__':

	if len(sys.argv) < 5:
		print "incorrect input format"
		print "Correct Format:<CSV FILE> <par|stack|stack-with-fundtype> <Year> <Institution> (fund type)"

	elif sys.argv[2] == "stack":

		csvFile = sys.argv[1]

		year = sys.argv[3]
		institution = sys.argv[4]
		donationType = ""

		if len(sys.argv) > 5:
			donationType = sys.argv[5]

		# list to output into the final csv
		outputList = []
		fieldNames = ["Year", "Donor", "Amount", "Type", "Institution"]

		thisRowIsAmount = False
		currentAmount = ""

		with open(csvFile, "rU") as inFile:
			donorsOrAmounts = csv.reader(inFile)
			for donorOrAmount in donorsOrAmounts:

				if not isinstance(donorOrAmount, basestring):
					if len(donorOrAmount) > 0:
						donorOrAmount = donorOrAmount[0]
					else:
						donorOrAmount = ""

				if thisRowIsAmount:
					# update the current amount value
					# currentAmount = refineAmountCellForCooper(donorOrAmount)	

					currentAmount = donorOrAmount
					thisRowIsAmount = False
					continue

				# if this row is an empty row, than the next one is an amount row 
				if donorOrAmount == "":
					thisRowIsAmount = True
					continue

				# if it comes here, it means it's just a name.
				print donorOrAmount + currentAmount

				# special case that we need to process for the Cooper data
				donorOrAmount = refineDonorNamesForCooper(donorOrAmount)

				thisDonorValueList = [year, donorOrAmount, currentAmount, donationType, institution]
				outputList.append(dict(zip(fieldNames, thisDonorValueList)))

			# print json.dumps(outputList, indent=4)

			with open(csvFile.replace(".csv", "-parsed.csv"), "w") as outFile:
				writer = csv.DictWriter(outFile, fieldnames = fieldNames)
				writer.writeheader()
				for donor in outputList:
					writer.writerow(donor)

	elif sys.argv[2] == "par":
		# if par|stack == par

		csvFile = sys.argv[1]
		year = sys.argv[3]
		institution = sys.argv[4]
		donationType = ""

		if len(sys.argv) > 5:
			donationType = sys.argv[5]

		# list to output into the final csv
		outputList = []
		fieldNames = ["Year", "Donor", "Amount", "Type", "Institution"]

		currentAmount = ""

		with open(csvFile, "rU") as inFile:
			donorsOrAmounts = csv.reader(inFile)
			for donorOrAmount in donorsOrAmounts:

				# if both columns are empty, we skip
				if donorOrAmount[0] == "" and donorOrAmount[1] == "":
					continue

				if not donorOrAmount[0] == "":
					# update the current amount value
					# currentAmount = refineAmountCellForCooper(donorOrAmount)
					currentAmount = refineAmountCellForNYPL(donorOrAmount[0])

				# special case that we need to process for the Cooper data
				# donorOrAmount = refineDonorNamesForCooper(donorOrAmount)
				donorName = donorOrAmount[1]
				print donorName + "-> " + currentAmount

				thisDonorValueList = [year, donorName, currentAmount, donationType, institution]
				outputList.append(dict(zip(fieldNames, thisDonorValueList)))

			# print json.dumps(outputList, indent=4)

			with open(csvFile.replace(".csv", "-parsed.csv"), "w") as outFile:
				writer = csv.DictWriter(outFile, fieldnames = fieldNames)
				writer.writeheader()
				for donor in outputList:
					writer.writerow(donor)

	else:
		# sys.args[2] == "stack-with-fundtype"

		csvFile = sys.argv[1]

		year = sys.argv[3]
		institution = sys.argv[4]

		# list to output into the final csv
		outputList = []
		fieldNames = ["Year", "Donor", "Amount", "Type", "Institution"]

		thisRowIsAmount = False
		currentAmount = ""
		currentFundType = ""

		with open(csvFile, "r") as inFile:
			donorsOrAmounts = csv.reader(inFile)
			for donorOrAmount in donorsOrAmounts:

				# if not isinstance(donorOrAmount, basestring):
				# 	if len(donorOrAmount) > 0:
				# 		donorOrAmount = donorOrAmount[0]
				# 	else:
				# 		donorOrAmount = ""


				if thisRowIsAmount:
					# update the current amount value
					# currentAmount = refineAmountCellForCooper(donorOrAmount)
					currentAmount = donorOrAmount[0]
					currentFundType = donorOrAmount[1]
					thisRowIsAmount = False
					continue

				# if this row is an empty row, than the next one is an amount row 
				if donorOrAmount[0] == "" and donorOrAmount[1] == "":
					thisRowIsAmount = True
					continue

				# if it comes here, it means it's just a name.
				print donorOrAmount[0] + "---" + currentAmount

				# special case that we need to process for the Cooper data
				# donorOrAmount[0] = donorOrAmount[0]

				thisDonorValueList = [year, donorOrAmount[0], currentAmount, currentFundType, institution]
				outputList.append(dict(zip(fieldNames, thisDonorValueList)))

			# print json.dumps(outputList, indent=4)

			with open(csvFile.replace(".csv", "-parsed.csv"), "w") as outFile:
				writer = csv.DictWriter(outFile, fieldnames = fieldNames)
				writer.writeheader()
				for donor in outputList:
					writer.writerow(donor)
