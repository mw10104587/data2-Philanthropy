import json, csv, sys


boardFile = open("../boards_data/allboards-affiliation.csv", "r")
reader = csv.DictReader(boardFile)


boards = {}
for bm in reader:
	if not bm["Institution"] in boards:
		boards[bm["Institution"]] = [bm["Name"]]
	else:
		boards[bm["Institution"]].append(bm["Name"])


print json.dumps(boards, indent=4)

boards_to_go = boards.keys()
boards_to_go = [key for key in boards_to_go if key != "Lincoln Center"]
print boards_to_go

for lc_bm in boards["Lincoln Center"]:
	for institution in boards_to_go:
		for un_bm in boards[institution]:
			if lc_bm == un_bm:
				print lc_bm + ": " + institution


print len(boards["Lincoln Center"])
				