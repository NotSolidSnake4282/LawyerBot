import collections
import copy
import sys, traceback
import settings
from bs4 import BeautifulSoup
from terminaltables import AsciiTable

class MessageTooLongException(Exception):
	pass

class Message:
	def __init__(self, message='', message_limit=1500):
		self.message_limit = message_limit
		if len(message) > self.message_limit :
			raise MessageTooLongException("Message can't be more than 2000")
		self.message = message

	def add_message(self, message):
		if len("%s\n\n%s" % (self.message, message)) > self.message_limit :
			raise MessageTooLongException("Message can't be more than 2000")
		self.message = "%s\n\n%s" % (self.message, message)

	def append_message(self, message):
		if len("%s %s" % (self.message, message)) > self.message_limit :
			raise MessageTooLongException("Message can't be more than 2000")
		if len(self.message) == 0:
			self.message = message
		else:
			self.message = "%s %s" % (self.message, message)

	def __repr__(self):
		return self.message

	def __str__(self):
		return self.message

class TableMessage:
	def __init__(self,title, table=[], message_limit=1500):
		self.message_limit = message_limit
		if(len(AsciiTable(table).table)) + len(title) > self.message_limit:
			raise MessageTooLongException("Message can't be more than %s" % self.message_limit)
		self.table = table
		self.title = title

	def add_row(self, row):
		temp_table = self.table
		temp_table.append(row)
		if len(AsciiTable(temp_table).table) + len(self.title) > self.message_limit:
			raise MessageTooLongException("Message can't be more than %s" % self.message_limit)
		self.table.append(row)

	@property
	def message(self):
		return "%s\n%s" % (self.title, AsciiTable(self.table).table)
 
# def multi_target_summary_processor():
# 	with open(settings.MULTI_TARGET_SUMMARY) as f:


def bane_processor(bane):
	return [
		{	
			'title':'Name',
			'content':bane['name'],
			'sequence':1
		},
		{
			'title':"Tags",
			'content':",".join(bane['tags']),
			'sequence':2
		},
		{
			'title':"Power Levels",
			'content':str(bane['power']),
			'sequence':3
		},
		{
			'title':"Attacks",
			'content':"\n".join(bane['attack']),
			'sequence':4
		},
		{
			'title':"Invocation Time",
			'content':bane['invocationTime'],
			'sequence':5,
		},
		{
			'title':"Duration",
			'content':bane['duration'],
			'sequence':6
		},
		{
			'title':"Description",
			'content':BeautifulSoup(bane['description'], 'html.parser').text,
			'sequence':7,
		},
		{
			'title':"Effect",
			'content':BeautifulSoup(bane['effect'], 'html.parser').text,
			'sequence':8
		},

		{	
			'title':"Special",
			'content':None if 'special' not in bane else BeautifulSoup(bane['special'], 'html.parser').text,
			'sequence':9
		}
	]

def boon_processor(boon):
	return [
		{	
			'title':'Name',
			'content':boon['name'],
			'sequence':1
		},
		{
			'title':"Tags",
			'content':",".join(boon['tags']),
			'sequence':2
		},
		{
			'title':"Power Levels",
			'content':str(boon['power']),
			'sequence':3
		},
		{
			'title':"Attribute",
			'content':"\n".join(boon['attribute']),
			'sequence':4
		},
		{
			'title':"Invocation Time",
			'content':boon['invocationTime'],
			'sequence':5,
		},
		{
			'title':"Duration",
			'content':boon['duration'],
			'sequence':6
		},
		{
			'title':"Description",
			'content':BeautifulSoup(boon['description'], 'html.parser').text,
			'sequence':7,
		},
		{
			'title':"Effect",
			'content':BeautifulSoup(boon['effect'], 'html.parser').text,
			'sequence':8
		},

		{	
			'title':"Special",
			'content':None if 'special' not in boon else BeautifulSoup(boon['special'], 'html.parser').text,
			'sequence':9
		}
	]

def feat_processor(feat):
	prerequisites = []
	try:
		ordered = collections.OrderedDict(sorted(feat['prerequisites'].items()))
		for tier in ordered:
			tp = []
			tier_preq = ordered[tier]
			for key in tier_preq:
				if key == 'Other':
					for string in tier_preq['Other']:
						tp.append(string)
				if key == 'Feat':
					for string in tier_preq['Feat']:
						tp.append(string)
				if key == 'Attribute':
					for attribute in tier_preq['Attribute']:
						kkey = list(attribute.keys())[0]
						# print (kkey)
						# print (attribute[kkey])
						tp.append("%s %s" % (kkey, attribute[kkey]))
				if key == 'any':
					tp.append("Any of")
					for kkey in tier_preq['any']:
						if kkey == 'Other':
							for string in tier_preq['any']['Other']:
								tp.append(string)
						if kkey == 'Feat':
							for string in tier_preq['any']['Feat']:
								tp.append(string)
						if kkey == 'Attribute':
							for attribute in tier_preq['any']['Attribute']:
								kkkey = list(attribute.keys())[0]
								# print (kkkey)
								# print (attribute[kkkey])
								tp.append("%s %s" % (kkkey, attribute[kkkey]))
			prerequisites.append(("%s : %s " % (tier, ",".join(tp))).replace('Any of,', 'Any of :'))
	except:
		 traceback.print_exc(file=sys.stdout)
		 prerequisites = ["Unable to parse prerequisites because my coder is dumb"]


	prerequisites = "\n".join(prerequisites)

	return [
		{	
			'title':'Name',
			'content':feat['name'],
			'sequence':1
		},
		{
			'title':'Prerequisites',
			'content':prerequisites,
			'sequence':2
		},
		{
			'title':"Tags",
			'content':",".join(feat['tags']) if feat['tags'] else None,
			'sequence':3
		},
		{
			'title':"Cost",
			'content':str(feat['cost']),
			'sequence':4
		},
		{
			'title':"Description",
			'content':BeautifulSoup(feat['description'], 'html.parser').text,
			'sequence':5,
		},
		{
			'title':"Effect",
			'content':BeautifulSoup(feat['effect'], 'html.parser').text,
			'sequence':6
		},

		{	
			'title':"Special",
			'content':None if 'special' not in feat else BeautifulSoup(feat['special'], 'html.parser').text,
			'sequence':7
		}

	]

def message_processor(items):
	messages = []
	message = Message()
	items = sorted(items, key=lambda item:item['sequence'])
	for item in items:
		content = '%s\n%s' % (item['title'], item['content'])
		try:
			message.add_message(content)
		except MessageTooLongException:
			messages.append(copy.deepcopy(message))
			try:
				message = Message(content)
			except MessageTooLongException:
				content = content.split(".")
				message = Message()
				for sentence in content:
					try:
						message.append_message('%s.' % sentence)
					except MessageTooLongException:
						messages.append(copy.deepcopy(message))
						message = Message(sentence)

	messages.append(message)
	return messages

def table_message_processor(table, title):
	messages = []
	try:
		messages.append(TableMessage(title, table))
		return messages
	except MessageTooLongException:
		pass
	message = TableMessage(title)
	for row in table:
		try:
			message.add_row(row)
		except MessageTooLongException:
			messages.append(copy.deepcopy(message))
			message = TableMessage(title)
			print (row)
			message.add_row(row)
	messages.append(message)
	return messages


def search(dictionary, substr):
    for key in dictionary:
        if substr.lower() in key.lower():
            return((dictionary[key]))
    return None