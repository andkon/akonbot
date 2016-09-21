from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import csv
import glob
import time

def make_convo_list(filename):
	""" takes a csv. 
	appends messages from the same person together. 
	puts them into a list, so it's person1-person2-person1-etc.
	returns the list when it hits 10 people or three hours
	"""

	all_messages = []
	csvFile = csv.reader(open(filename, "rb"))
	for row in csvFile:
		if csvFile.line_num == 1:
			continue
		elif csvFile.line_num == 10:
			break

		di = {}
		di["Name"]=row[0]
		di["Message"]=row[2]
		# make the datetime
		raw_dt = row[3]

		dt = time.strptime(raw_dt, "%b %d, %Y, %I:%M:%S %p")

		di["Date"]=dt
		# now append
		all_messages.append(di)

	import pdb; pdb.set_trace()
	# now check if this stuff is valid:
	if di["Name"][0] == "Me":
		# k good. but possibly we should change this.
		# now... append the messages from me
		pass
	else:
		return None


def make_a_bot():
	chatbot = ChatBot("Bud")
	chatbot.set_trainer(ListTrainer)

	# time to loop through the files in the data folder

	for filename in glob.iglob("data/*.csv"):
		print('%s' % filename)
		# create a list 
		new_list = make_convo_list(filename)
		if new_list is not None:
			# train it!
			chatbot.train(new_list)

	return chatbot