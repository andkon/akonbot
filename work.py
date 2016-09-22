from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import csv
import glob
import time


def make_convo_list(filename):
	""" takes a csv. 

	puts them into a list, so it's person1-person2-person1-etc.
	returns the list when it hits 10 people or three hours
	"""

	all_messages = []
	csvFile = csv.reader(open(filename, "rb"))
	for row in csvFile:
		if csvFile.line_num == 1:
			continue
		elif csvFile.line_num == 2:
			if row[0] == "Me":
				break
		elif csvFile.line_num > 10:
			if row[0] =="Me":
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

	# now make a pretty list and return it

	final_messages = []
	for msg in all_messages:
		# now, we either append to the last message, or we add a whole new message.
		if len(final_messages) > 0:
			if msg['Name'] == final_messages[-1]['Name']:
				final_messages[-1]['Message']+= ". %s" % (msg["Message"])
			else:
				final_messages.append(msg)
		else:
			final_messages.append(msg)

	return map(lambda x: x['Message'], final_messages)

def make_a_bot():
	chatbot = ChatBot("Bud")
	chatbot.set_trainer(ListTrainer)

	# time to loop through the files in the data folder

	for filename in glob.iglob("data/*.csv"):
		print('%s' % filename)
		# create a list 
		new_list = make_convo_list(filename)
		print new_list
		if new_list is not None:
			# train it!
			chatbot.train(new_list)

	return chatbot