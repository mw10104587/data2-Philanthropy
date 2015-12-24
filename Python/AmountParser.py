# this file helps to tackle with 20 file amount data
import csv
import re
import sys

def getUpperandLowerBoundAmount(amountStr):

	amountStr = amountStr.lower()

	if amountStr == "unknown":
		return (0,0)

	# if Strings starting then we found something weird, we have to remove it. 
	if not re.search('^[^0-9$,]+', amountStr) is None:
		
		print "in this funny place"
		print amountStr
		amountStr = amountStr[amountStr.find("$"):]
		print "......."
		print amountStr

	if amountStr.find("and above") != -1:
		amountStr = amountStr.replace("and above", "")
		amountStr = amountStr.strip()
		amountStr = amountStr.replace("$", "")
		amountStr = re.sub(",", "", amountStr)
		return (int(amountStr), "-")

	if amountStr.find("and below") != -1:
		amountStr = amountStr.replace("and below", "")
		amountStr = amountStr.strip()
		amountStr = amountStr.replace("$", "")
		amountStr = re.sub(",", "", amountStr)
		return ("-", int(amountStr))
		
	if amountStr.find("-") != -1:
		lowerBound = amountStr.split("-")[0]
		upperBound = amountStr.split("-")[1]

		lowerBound = lowerBound.strip()
		lowerBound = re.sub("$", "", lowerBound)
		lowerBound = re.sub(",", "", lowerBound)
		lowerBound = re.sub("[^0-9]+", "", lowerBound)

		upperBound = upperBound.strip()
		upperBound = re.sub("$", "", upperBound)
		upperBound = re.sub(",", "", upperBound)
		upperBound = re.sub("[^0-9]+", "", upperBound)
		return (int(lowerBound), int(upperBound))

	if re.search("[^0-9$,\s]", amountStr) is None:

		amount = re.sub("[$,\s]", "", amountStr)
		return (int(amount), int(amount))

	else:

		print "= = ??????"
		print amountStr
		print "= = ??????"
		sys.exit()


# here we input the tuple and use the lower bound first unless it doesn't exist
def getDonationAmountClass(amount_tuple):
	lowerbound = amount_tuple[0]
	upperbound = amount_tuple[1]

	# just add or modify the threshold in this list
	threshold = [1000000, 750000, 500000, 250000, 249999]

	if lowerbound != "-":
		idx = 0
		while(lowerbound < threshold[idx]):
			if idx == len(threshold) - 1:
				return len(threshold)

			idx = idx + 1 
		return idx + 1

	if lowerbound == "-" and upperbound == "-":
		return len(threshold)

	if upperbound != "-":
		idx = 0
		while(upperbound < threshold[idx]):
			if idx == len(threshold) - 1:
				return len(threshold)

			idx = idx + 1 
		return idx + 1

	# 1 -> 1,000,000 + 
	# 2 -> 750,000 +
	# 3 -> 500,000 + 
	# 4 -> 250,000 + 
	# 5 -> 249,999 -


with open("../TO BE PARSED/911_memorial_merged.csv", "r") as inputFile:
	reader = csv.DictReader(inputFile)

	outputFile = open("../test-data/911_memorial-amount-fine.csv", "w")
	# amount_lb -> amount lower bound
	# amount_ub -> amount upper bound
	writer = csv.DictWriter(outputFile, fieldnames = ["Donor","Amount","Type","Institution","Year", "amount_lb", "amount_ub", "amount_class"])
	writer.writeheader()
	for donation in reader:
		amount = donation["Amount"]
		# print amount
		uplowTuple = getUpperandLowerBoundAmount(amount)
		# print uplowTuple
		# print getDonationAmountClass(uplowTuple)

		donation["amount_lb"] = uplowTuple[0]
		donation["amount_ub"] = uplowTuple[1]
		donation["amount_class"] = getDonationAmountClass(uplowTuple)
		donation["Donor"] = donation["Donor"].strip()

		writer.writerow(donation)


