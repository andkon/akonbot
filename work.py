from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import csv
import glob
import time

def tidy_up_messages(message_list, i, final_messages):
	""" 
	appends messages from the same person together. 
	"""

	# first, we see if we've reached the end of the message list
	try:
		msg = message_list[i]
	except IndexError:
		# all done here. loop through and make a normal ass list
		return map(lambda x: x['Message'], final_messages)

	# now, we either append to the last message, or we add a whole new message.
	if len(final_messages) > 0:
		if msg['Name'] == final_messages[-1]['Name']:
			final_messages[-1]['Message']+= ". %s" % (msg["Message"])
		else:
			final_messages.append(msg)
	elif (len(message_list) - 1) == i:
		return map(lambda x: x['Message'], final_messages)
	else:
		final_messages.append(msg)

	import pdb; pdb.set_trace()
	i+=1
	tidy_up_messages(message_list, i, final_messages)

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
		elif csvFile.line_num > 10:
			# here, if there's an app 
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

	# now check if this stuff is valid:

	return tidy_up_messages(all_messages, 0, [])



def make_a_bot():
	chatbot = ChatBot("Bud")
	chatbot.set_trainer(ListTrainer)

	# time to loop through the files in the data folder

	for filename in glob.iglob("data/*.csv"):
		print('%s' % filename)
		# create a list 
		new_list = make_convo_list(filename)
		import pdb; pdb.set_trace()
		print new_list
		if new_list is not None:
			# train it!
			chatbot.train(new_list)

	return chatbot