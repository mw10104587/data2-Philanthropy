# This file takes in board members data and donor list
# link them according to donation
# output an edge file


# there are five donation classes, assaigned accroding to the amount they donate.
# cmd line usage python GenerateNodeGraphData <donors-list.csv> <boards.csv> (<smallest donation class>)


import sys, csv, json

class donationLink:
	def __init__(self, id_1, name1, id_2, name2, institution, amount, amount_lb, amount_ub):

		# donors first, board members second
		self.id_1 = id_1
		self.id_2 = id_2

		# add donors name into this relation ship
		# but I wonder which one is better, whether I should just leave it as a attribute = =?
		self.name_1 = name1
		self.name_2 = name2

		self.institution = institution
		self.donation = amount
		self.amount_lb = amount_lb
		self.amount_ub = amount_ub

	def __repr__(self):
		return ( str(self.id_1) + "-> " + str(self.id_2) )


	def toDictionary(self):
		return {
			"id_1": self.id_1,
			"id_2": self.id_2,
			"Amount": self.donation,
			"amount_lb": self.amount_lb,
			"amount_ub": self.amount_ub,
			"Institution": self.institution,
			"Relation": "edge",
			"Weight": 1
		}

	def toString(self):
		# into this format
		# NODE TYPE, NODE NAME, EDGE TYPE, NODE TYPE, NODE NAME, AMOUNT, Weight, Institution

		# SOURCE TYPE,Source,EDGE TYPE,TARGET TYPE,Target,AMOUNT,Weight,Institution
		# return 'DONOR,"' + self.name_1.strip() + '",' + "Donation," + 'BOARD MEMBER,"' + self.name_2.strip() + '","' + self.donation.strip() + '",1,' + self.institution
		return 'DONOR,"' + str(self.id_1) + '",' + "Donation," + 'BOARD MEMBER,"' + str(self.id_2) + '","' + self.donation.strip() + '",1,' + self.institution


class AffiliationLink:
	def __init__(self, id_b_member, b_member_name, id_donor_affiliation, affiliation_name):
		self.source = id_b_member
		self.target = id_donor_affiliation

		self.b_member_name = b_member_name
		self.affiliation_name = affiliation_name


	def toString(self):
		# SOURCE TYPE,			Source,						EDGE TYPE,				TARGET TYPE,  Target,				AMOUNT,Weight,Institution
		return "BOARD MEMBER," + str(self.source) + "," + "Affiliation Member," + "AFFILIATION," + str(self.target) + ",-,10,-"


# same donor so only one name needed
class SameDonorLink:
	def __init__(self, id_donor_1, id_donor_2, donor_name):
		self.id_1 = id_donor_1
		self.id_2 = id_donor_2
		self.name = donor_name


	def toString(self):
		return "DONOR," + str(self.id_1) + "," + "Same Donor," + "DONOR," + str(self.id_2) + ",-,4,-"



class DonorIsBoardMemberLink:
	def __init__(self, id_donor, id_b_member, name_donor):
		self.id_donor = id_donor
		self.id_b_member = id_b_member
		self.name = name_donor

	def toString(self):
		return "DONOR," + str(self.id_donor) + ",Donor is Board Member,BOARD MEMBER," + str(self.id_b_member) + ",-,4,-"




def compareNames(name_1, name_2):

	if name_1 == name_2:
		return True


def getOutputStringWithDonorDict(donor):

	# TYPE, Name, ID, Institution, Amount, Year, amount_lb, amount_ub

	# for board member
	if not "amount_lb" in donor:
		donor["amount_lb"] = "-"

	# for board member
	if not "amount_ub" in donor:
		donor["amount_ub"] = "-"


	if not "Amount" in donor:
		amount = "-"
	else:
		amount = str(donor["Amount"])

	if (not "Year" in donor) and ("First year" in donor):
		year = str(donor["First year"])
	else:
		year = str(donor["Year"])

	if donor["Type"] == "Board":
		nodeType = "BOARD MEMBER"
	else:
		nodeType = "DONOR"
		
	return nodeType + ',"' + donor["Name"].strip() + '",' + str(donor["ID"]) + "," + donor["Institution"] + ',"' + amount.strip() + '",' + year + ',' + donor["amount_lb"] + "," + donor["amount_ub"]



if __name__ == "__main__":
	donors_file_path = sys.argv[1]
	member_file_path = sys.argv[2]

	if len(sys.argv) > 3:
		donationClassThreshold = int(sys.argv[3])

	print donationClassThreshold
	# sys.exit()


	donors_file = open(donors_file_path, "r")
	donors = csv.DictReader(donors_file)

	member_file = open(member_file_path, "r")
	board_members = csv.DictReader(member_file)

	# assign ID for each donors
	donors = list(donors)

	donors = [d for d in donors if int(d["amount_class"]) <= donationClassThreshold ] 

	for idx, donor in enumerate(donors):
		donors[idx]["ID"] = idx + 1



	# in order to add board members into the plot, we'll have to append them to the donors data.
	# so we have to shift the id for all of the board members
	shift = len(donors)


	# assign ID for each board members
	board_members = list(board_members)
	boards = {}

	for idx, b_member in enumerate(board_members):
		# board_members[idx]["id"] = "B" + str(idx)
		board_members[idx]["ID"] = idx + 1 + shift
		b_member["Type"] = "Board"

		if not b_member["Institution"].lower() in boards:
			boards[b_member["Institution"].lower()] = []
		else:
			boards[b_member["Institution"].lower()].append(b_member)


	edges = []

	# find same donor names
	for idx, donor in enumerate(donors):
		for idx_l, donor_loop in enumerate(donors):
			if donor["Name"].lower() == donor_loop["Name"].lower() and idx != idx_l:
				print "Got the same name but different transaction: " + donor["Name"]
				# id_donor_1, id_donor_2, donor_name
				edges.append(SameDonorLink(donor["ID"], donor_loop["ID"], donor["Name"]))


	for idx, donor in enumerate(donors):
		for idx_b, b_member in enumerate(board_members):
			if donor["Name"].strip().lower() == b_member["Name"].strip().lower():
				print "Got the same name of donor and board members: " + donor["Name"]
				# id_donor, id_b_member, name_donor
				edges.append(DonorIsBoardMemberLink(donor["ID"], b_member["ID"], donor["Name"]))




	donors = donors + board_members
	# print json.dumps(boards, indent=4)
	print boards.keys()


	

	for donor in donors:

		if not "Amount" in donor:
			continue
			# pass

		if donor["Amount"] == 0:
			continue

		if int(donor["amount_class"]) > donationClassThreshold:

			print donor["amount_class"] + ":" + str(donationClassThreshold)
			print "some one is in here"
			continue

		institution = donor["Institution"].lower()
		# load the file in for loop, so that we can iterate it everytime
		for b_member in boards[institution]:
			# id_1, name1, id_2, name2, institution, amount_lb, amount_ub
			# edges.append(donationLink(donor["ID"] , donor["Name"], int(b_member["ID"]) + shift, b_member["Name"] , donor["Institution"], donor["Amount"]))		
			edges.append(donationLink(donor["ID"] , donor["Name"], int(b_member["ID"]), b_member["Name"] , donor["Institution"], donor["Amount"], donor["amount_lb"], donor["amount_ub"]))



	# add edges for boards members who belongs to other affiliation
	for board_member in board_members:
		# match it's affiliation to other donors
		if board_member["Affiliation"] != "":
			affiliations = board_member["Affiliation"].split("|")
		else:
			continue

		# match the affiliations to donors
		for affiliation in affiliations:
			affiliation = affiliation.strip()
			if len(affiliation) == 0:
				continue
			for donor in donors:
				if affiliation.lower() == donor["Name"].lower():
					print "What a surprise!!!!"
					print donor["Name"]
					print "======================="
					# id_b_member, b_member_name, id_donor_affiliation, affiliation_name
					edges.append(AffiliationLink(board_member["ID"], board_member["Name"], donor["ID"], donor["Name"]))


	# print edges
	# export edges
	fieldnames = ["id_1", "id_2", "Amount", "Institution", "Relation", "Weight"]

	with open("final-edges-final.csv", "w") as edgeOutput:
		# writer = csv.DictWriter(edgeOutput, fieldnames=fieldnames)
		# writer.writeheader()

		edgeOutput.write("SOURCE TYPE,Source,EDGE TYPE,TARGET TYPE,Target,AMOUNT,Weight,Institution\n")

		for edge in edges:
			# writer.writerow(edge.toDictionary())
			edgeOutput.write(edge.toString() + "\n")


	nodeFields = [ "ID","Year","Position","Name","Amount", "Type","Institution", "id", "First year"]

	with open("final-nodes-final.csv", "w") as nodeOutput:

		nodeOutput.write("TYPE,Name,ID,Institution,Amount,Year,amount_lb,amount_ub\n")

		# writer = csv.DictWriter(nodeOutput, fieldnames=nodeFields)
		# writer.writeheader( )

		for node in donors:
			# writer.writerow()

			# board member 
			if not "amount_lb" in node:
				nodeOutput.write(getOutputStringWithDonorDict(node) + "\n")	
			else:

				if int(node["amount_class"]) > donationClassThreshold:
					continue
				else:
					nodeOutput.write(getOutputStringWithDonorDict(node) + "\n")						

			
