# This file takes in board members data and donor list
# link them according to donation
# output an edge file

# cmd line usage python GenerateNodeGraphData <donors-list.csv> <boards.csv>


import sys, csv, json

class donationLink:
	def __init__(self, id_1, name1, id_2, name2, institution, min_donation, donation_range = 0):

		# donors first, board members second
		self.id_1 = id_1
		self.id_2 = id_2

		# add donors name into this relation ship
		# but I wonder which one is better, whether I should just leave it as a attribute = =?
		self.name_1 = name1
		self.name_2 = name2

		self.institution = institution
		self.donation = min_donation
		if donation_range != 0:
			self.donation_range = donation_range

	def __repr__(self):
		return ( str(self.id_1) + "-> " + str(self.id_2) )


	def toDictionary(self):
		return {
			"id_1": self.id_1,
			"id_2": self.id_2,
			"Amount": self.donation,
			"Institution": self.institution,
			"Relation": "edge",
			"Weight": 1
		}

	def toString(self):
		# into this format
		# NODE TYPE, NODE NAME, EDGE TYPE, NODE TYPE, NODE NAME, AMOUNT, Weight, Institution

		# return 'DONOR,"' + self.name_1.strip() + '",' + "Donation," + 'BOARD MEMBER,"' + self.name_2.strip() + '","' + self.donation.strip() + '",1,' + self.institution
		return 'DONOR,"' + str(self.id_1) + '",' + "Donation," + 'BOARD MEMBER,"' + str(self.id_2) + '","' + self.donation.strip() + '",1,' + self.institution

def compareNames(name_1, name_2):

	if name_1 == name_2:
		return True


def getOutputStringWithDonorDict(donor):

	# TYPE, Name, ID, Institution, Amount, Year

	if not "Amount" in donor:
		amount = "-"
	else:
		amount = str(donor["Amount"])

	if not "Year" in donor and "First year" in donor:
		year = str(donor["First year"])
	else:
		year = str(donor["Year"])

	if donor["Type"] == "Board":
		nodeType = "BOARD MEMBER"
	else:
		nodeType = "DONOR"
		
	return nodeType + ',"' + donor["Name"].strip() + '",' + str(donor["ID"]) + "," + donor["Institution"] + ',"' + amount.strip() + '",' + year



if __name__ == "__main__":
	donors_file_path = sys.argv[1]
	member_file_path = sys.argv[2]

	donors_file = open(donors_file_path, "r")
	donors = csv.DictReader(donors_file)

	# make donors unique function is missing here.
	# 
	# 
	#############################################

	member_file = open(member_file_path, "r")
	board_members = csv.DictReader(member_file)

	# assign ID for each donors
	donors = list(donors)
	# for idx, donor in enumerate(donors):
		# donors[idx]["id"] = "D" + str(idx)



	# in order to add board members into the plot, we'll have to append them to the donors data.
	# so we have to shift the id for all of the board members
	shift = len(donors)


	# assign ID for each board members
	board_members = list(board_members)
	boards = {}

	for idx, b_member in enumerate(board_members):
		# board_members[idx]["id"] = "B" + str(idx)
		board_members[idx]["ID"] = int(board_members[idx]["ID"]) + shift

		if not b_member["Institution"].lower() in boards:
			boards[b_member["Institution"].lower()] = []
		else:
			boards[b_member["Institution"].lower()].append(b_member)

	donors = donors + board_members
	# print json.dumps(boards, indent=4)
	print boards.keys()



	



	edges = []

	for donor in donors:

		if not "Amount" in donor:
			continue
			# pass

		if donor["Amount"] == 0:
			continue

		institution = donor["Institution"].lower()



		# load the file in for loop, so that we can iterate it everytime
		for b_member in boards[institution]:

			# link donor to board members
			# institution = donor["Institution"]

			# get board members' name 

			print "==================="
			print b_member
			print b_member["ID"]
			print "==================="
			edges.append(donationLink(donor["ID"] , donor["Name"],int(b_member["ID"]) + shift, b_member["Name"] , donor["Institution"], donor["Amount"]))


	# print edges
	# export edges
	fieldnames = ["id_1", "id_2", "Amount", "Institution", "Relation", "Weight"]

	with open("final-edges.csv", "w") as edgeOutput:
		# writer = csv.DictWriter(edgeOutput, fieldnames=fieldnames)
		# writer.writeheader()

		edgeOutput.write("SOURCE TYPE,Source,EDGE TYPE,TARGET TYPE,Target,AMOUNT,Weight,Institution\n")

		for edge in edges:
			# writer.writerow(edge.toDictionary())
			edgeOutput.write(edge.toString() + "\n")


	nodeFields = [ "ID","Year","Position","Name","Amount", "Type","Institution", "id", "First year"]

	with open("final-nodes.csv", "w") as nodeOutput:

		nodeOutput.write("TYPE,Name,ID,Institution,Amount,Year\n")

		# writer = csv.DictWriter(nodeOutput, fieldnames=nodeFields)
		# writer.writeheader( )

		for node in donors:
			# writer.writerow()
			nodeOutput.write(getOutputStringWithDonorDict(node) + "\n")
