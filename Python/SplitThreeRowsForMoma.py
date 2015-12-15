import csv, sys, json

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print "incorrect input format"
		print "Correct Format:<CSV FILE>"

	else:

		csvFile = sys.argv[1]
		with open(csvFile, "r") as inFile:
			threeColumns = csv.reader(inFile)
			

			mainColumn = []
			# three buffers to save each column for a page,
			# get's cleaned after running through every page.
			cols = [[],[], []]

			for three in threeColumns:
				# print three
				if three[0].isdigit():
					print three[0]
					mainColumn = mainColumn + cols[0] + cols[1] + cols[2]
					cols = [[], [], []]

				elif three[1].isdigit():
					print three[1]
					mainColumn = mainColumn + cols[0] + cols[1] + cols[2]
					cols = [[], [], []]


				elif three[0] == "" and three[1] == "" and three[2] == "":
					continue

				else:
					for i, element in enumerate(three):
						if element != "":
							cols[i].append(element)


			print mainColumn
			with open(csvFile.replace(".csv", "-splited.csv"), "w") as oF:
				# writer = csv.writer(oF)
				# writer.writerow()
				for cell in mainColumn:
					# writer.writerow(cell)
					oF.write( '"' + cell + '"\n')