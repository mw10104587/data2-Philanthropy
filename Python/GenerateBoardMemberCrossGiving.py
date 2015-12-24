# ========================================================================================= #
#   This file generates two csv files and a json fileself.                                  #
#   Two csv files are node and edge data respectively, and the json file is a matrix for    #
#   plotting chord diagram.                                                                 #
# ========================================================================================= #

import sys, csv, json
import numpy as np

class Edge:
	def __init__(self, source_type, source_id, source_name, edge_type, target_type, target_id, target_name,weight=1):
		
		self.source_type = source_type
		self.source_id = source_id
		self.source_name = source_name

		self.edge_type = edge_type

		self.target_id = target_id
		self.target_type = target_type
		self.target_name = target_name

		self.weight = weight



	# SOURCE TYPE,Source, Source Name, EDGE TYPE,TARGET TYPE,Target, Target Name, Weight
	def getEdgeString(self):
		return self.source_type + "," + str(self.source_id) + ',"' + self.source_name.strip() + '",' + self.edge_type + "," + self.target_type + "," + str(self.target_id) + ',"' + self.target_name.strip() + '",' + str(self.weight)

	def setDonationAmount(self, amount):
		self.amount = amount

	def setBoardMemberDonorOriginalInstitution(self, institution):
		self.original_institution = institution

	def getBoardMemberDonorOriginalInstitution(self):
		return self.original_institution

	def getAmount(self):
		return self.amount

	def getSourceType(self):
		return self.source_type

	def getEdgeType(self):
		return self.edge_type

	def getTargetId(self):
		return self.target_id




if __name__ == "__main__":

	donors_file_path = sys.argv[1]
	member_file_path = sys.argv[2]
	donationClassThreshold = int(sys.argv[3])

	donors_file = open(donors_file_path, "r")
	donors = csv.DictReader(donors_file)

	member_file = open(member_file_path, "r")
	board_members = csv.DictReader(member_file)

	# assign ID for each donors
	donors = list(donors)
	donors = [d for d in donors if int(d["amount_class"]) <= donationClassThreshold ] 


	# assign ID for each board members
	board_members = list(board_members)
	
	# board is a dictionary that saves the institution name as key, and ID(for it's node) as value.
	boards = {}

	# loop through board members, and find all of their institutions, we have to plot the institution into a large node.
	for idx, b_member in enumerate(board_members):

		board_members[idx]["Type"] = "Board"
		# board member's ID starts from 31
		board_members[idx]["ID"] = 31 + idx

		currentInstitutionsCount = len(boards.keys())

		if not b_member["Institution"].lower() in boards:
			boards[b_member["Institution"].lower()] = currentInstitutionsCount + 1

	institutionsList = [{"institution": k, "ID": v} for k,v in boards.items()]
	print institutionsList


	edges = []

	# build links to board members and institutions
	for board_member in board_members:
		institution_id = boards[board_member["Institution"].lower()]
		board_member_id = board_member["ID"]

		# save an edge to edges
		# SOURCE TYPE,Source, Source Name, EDGE TYPE,TARGET TYPE,Target, Target Name, Weight
		board_member_link_institution = Edge("INSTITUTION", institution_id, board_member["Institution"], "Board Member Of", "BOARD MEMBER", board_member_id, board_member["Name"], 1)
		edges.append(board_member_link_institution)


	# find the board members that also donated money to institutions other than itselves.
	for donor in donors:
		for board_member in board_members:

			if donor["Institution"].strip().lower() == board_member["Institution"].strip().lower():
				# donates
				# print "Got one that board member donate to it's own institution"
				continue

			if donor["Name"].strip().lower() == board_member["Name"].strip().lower():

				institution_name = donor["Institution"].lower()
				institution_id = boards[institution_name]
				donor_is_board_edge = Edge("BOARD MEMBER", board_member["ID"], board_member["Name"], "Board Member Donation", "INSTITUTION", institution_id, institution_name, 5)
				if donor["amount_lb"] != "-":
  					donor_is_board_edge.setDonationAmount(donor["amount_lb"])
  				else:
  					donor_is_board_edge.setDonationAmount(donor["amount_ub"])

  				# record the board member's institution so that we can reference it when we build the matrix.
  				donor_is_board_edge.setBoardMemberDonorOriginalInstitution(board_member["Institution"].strip().lower())
				edges.append(donor_is_board_edge)


	# add edges for boards members who belongs to other affiliation
	for board_member in board_members:
		# match it's affiliation to other donors
		if board_member["Affiliation"] != "":
			affiliations = board_member["Affiliation"].split("|")
			affiliations = [aff.strip().lower() for aff in affiliations]
		else:
			continue

		# match the affiliations to donors
		for affiliation in affiliations:
			affiliation = affiliation.strip()
			if len(affiliation) == 0:
				continue
			for donor in donors:
				if affiliation == donor["Name"].strip().lower():
					# make a link that starts from board member and links to the foundation that it belongs to, 
					# also this foundation doesn't donate to the institution of his board 
					institution_name = donor["Institution"].strip().lower()
					institution_id = boards[institution_name]


					# if it's donating to it's own, then we give a smaller weight
					if institution_name == board_member["Institution"].strip().lower(): 

						print "Donation to it's own affiliation, not included"
						continue

						link_to_self_donation_affiliate = Edge("BOARD MEMBER", board_member["ID"], board_member["Name"].strip(), "Affiliate Self", "INSTITUTION", institution_id, institution_name, 2)
  						edges.append(link_to_self_donation_affiliate)
  					elif institution_name in affiliation:
  						continue
  					# this is the best part that we're trying to find
  					else:

  						# print "======================================="
  						# print donor["Name"] + " of " + board_member["Name"] + "'s Affiliation donated to " + board_member["Institution"]
  						# print "======================================="
  						# print "" 

  						link_to_other_donation_affiliate = Edge("BOARD MEMBER", board_member["ID"], board_member["Name"].strip(), "Affiliate Other", "INSTITUTION", institution_id, institution_name, 8)
  						if donor["amount_lb"] != "-":
  							link_to_other_donation_affiliate.setDonationAmount(donor["amount_lb"])
  						else:
  							link_to_other_donation_affiliate.setDonationAmount(donor["amount_ub"])

  						link_to_other_donation_affiliate.setBoardMemberDonorOriginalInstitution(board_member["Institution"].strip().lower())
  						edges.append(link_to_other_donation_affiliate)


  	# export matrix for chord graph use
  	matrix = [float(0)]*21
  	matrix = [list(matrix) for x in range(0,21)]

  	print matrix

  	donationSum = 0
  	for edge in edges:
  		# if it's board member to institution, we ski;
  		if edge.getEdgeType() == "Board Member Of":
  			print "board member of, neglected"
  			continue

  		elif edge.getEdgeType() == "Board Member Donation":
  			
  			# get board institution id
  			bm_institution_name = edge.getBoardMemberDonorOriginalInstitution()
  			bm_institution_id = int(boards[bm_institution_name])

  			print bm_institution_name + "," + str(institution_id)


  			# get donation institution id
  			institution_id = int(edge.getTargetId())

  			# get amount of donation
  			donation = int(edge.getAmount())

  			matrix[institution_id-1][bm_institution_id-1] += float(donation)
  			donationSum += donation

  		elif edge.getEdgeType() == "Affiliate Other":
  			
  			# get board institution id
  			bm_institution_name = edge.getBoardMemberDonorOriginalInstitution()
  			bm_institution_id = int(boards[bm_institution_name])

  			print bm_institution_name + "," + str(institution_id)


  			# get donation institution id
  			institution_id = int(edge.getTargetId())

  			# get amount of donation
  			donation = int(edge.getAmount())

  			matrix[institution_id-1][bm_institution_id-1] += float(donation)
  			donationSum += donation

  		else:
  			print "I don't know why I'm here."

  	# ======================================================================================== #
  	# temp usage
	# calculate the sum of board members' donation, and print it out with the institution name
	# bm_donation_sum = np.sum(np.matrix(matrix), 1).tolist()
	#
 	#  	for x in xrange(1,22):
 	#  		# print x 
 	#  		for board in institutionsList:
 	#  			if board["ID"] == x:
 	#  				print board["institution"] + "," + str(bm_donation_sum[x-1][0])
 	#
	# sys.exit()
	# ======================================================================================== #




	# At first I thought it should be useful? But I think the d3.js will take care of normalizing for us.
  	matrix = np.matrix(matrix)/float(donationSum)

  	# output the json file
  	with open("../story-use data/graph-3/matrix.json", "w") as matrixOut:
  		json.dump(matrix.tolist(), matrixOut)




	# export edges
	with open("../story-use data/graph-2/graph-2-edges-final.csv", "w") as edgeOutput:

		edgeOutput.write("SOURCE TYPE,Source,Source Name,EDGE TYPE,TARGET TYPE,Target,Target Name, Weight\n")
		for edge in edges:
			# writer.writerow(edge.toDictionary())
			edgeOutput.write(edge.getEdgeString() + "\n")


	with open("../story-use data/graph-2/graph-2-nodes-final.csv", "w") as nodeOutput:

		nodeOutput.write("TYPE,Name,ID,Size\n")
		for institution in institutionsList:
			nodeOutput.write('INSTITUTION,"' + institution["institution"] + '",' + str(institution["ID"]) + ",20" + "\n")	

		for board_member in board_members:
			nodeOutput.write('BOARD MEMBER,"' + board_member["Name"].strip() + '",' + str(board_member["ID"]) + ",4" + "\n")
				

