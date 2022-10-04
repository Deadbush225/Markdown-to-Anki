import re

# Compromises
# - any image will be ignored

# Acronyms, ends with ;
# - thi  -> thickness
# - com  -> components
# - muo  -> made up off
# - wcf  -> where we can find
# - prop -> properties
# - itis   -> it is \the   (default)
# - 

# the implied acronyms are not a written acronym like *acrnoym*; 
# they are automatically detected like the term def

ignore_line_list = [
	"> [!source-image]"
]

acronyms_sub = {
	"thi": "thickness",
	"com": "components",
	"mofs": "made up off",
	"wcf": "where we can find",
	"prop": "properties",
	"it": "it",
	"itis": "it is the",
	"ithas": "it has",
	"has":"has",
	"ff": "fun fact",
	"pt": "parts of",
	"wh": "where == happens",
    #"implied acronyms": {
    "td": "term - definition" # term def 
}

# warning: answer is deprecated
# == is for the topic, and ~~ is for the fact, and __ is for the blanked_fact
# the first item in the list is the nonblanked question while the second item is the blanked question

#todo: the third item is fact as question, something like in the "wh"
acronyms_que = {
	"thi": ["How thick is the ==?", "The == is __ thick", ],
	"com": ["== is composed of what?", "== is made up of: \n\n __"],
	"mofs": ["== is made up off what?", "== is made up of: \n\n __"],
	"wcf": ["What we can find in the ==?", "We can find the __ in the =="],
	"prop": ["What are the properties of the ==?", "The properties of == are: \n\n __"],
	"it": ["The == is?", "== __"], 
	"itis": ["What is the ==?", "== is the __"],
	"has": ["== has?", "has __"],
	"ff": ["ff - NaN", "Fun fact: __"],
	"ithas": ["== has?", "it has __?"],
	"pt": ["What are the parts of ==?", "== have parts which are: \n\n __"], # -> the part of is in the linetopic title
	"wh" : ["Where the ~~ happens"],
    # "implied acronyms": {
    "td": ["== is defined as?", "== is defined as __"]
}

class TopicMap():
	def __init__(self):
		self.topic_map = {
			"h1" : [1, ""],
			"h2" : [2, ""],
			"h3" : [3, ""],
			"h4" : [4, ""],
			"h5" : [5, ""],
			"h6" : [6, ""],
			"h7" : [7, ""], # linetopic
			"h8" : [8, ""], # term
		}

		self._get_maplist()
		self._get_headerlist()

	def clean_heading_heirarchy(self, heading_heirarchy: str) -> str:
		header_tst = re.search(r"(#+)", heading_heirarchy)
		if header_tst:
			hash_count = heading_heirarchy.count("#")

			return f"h{hash_count}"
		elif "h" in heading_heirarchy:
			return heading_heirarchy
		# else: #  currently there is no other topic type to look out except "linetopic"
			# return "linetopic"

	def _get_maplist(self):
		self.maplist = [val[1] for val in self.topic_map.values() if val[1]]

	def _get_headerlist(self):
		# self.headerlist = [self.topic_map[val][1] for val in ["h1", "h2", "h3", "h4", "h5", "h6", "h7" ,"h8"] if self.topic_map[val][1]]
		self.headerlist = [self.topic_map[val][1] for val in self.topic_map.keys() if self.topic_map[val][1]]
		print(f"headerlist: {self.headerlist}")

	def __getitem__(self, heirarchy_index):
		if heirarchy_index == -1: # lowest header
			return self.get_lowest_header()
		# 	return self.topic_map["h7"][1]
		# elif heirarchy_index == : # lowest header
			# return self.get_second_lowest_header()
		elif heirarchy_index == 0: # second lowest header
			return self.get_highest_header()

	def get_highest_header(self):
		self._get_headerlist()
		return self.headerlist[0]

	def get_lowest_header(self):
		self._get_headerlist()
		return self.headerlist[-1]
	
	def get_topic_map_string(self, depth=2):
		self._get_maplist()

		first_index = -1*(depth + 1)

		# 			   	   depth
		#                  |   |
		# [h1, h2, h3, h4, h5, h6, h7]

		if depth + 1 < len(self.maplist):
			s = " > ".join(self.maplist)
		else:
			s = " > ".join(self.maplist[first_index:])
			
		return s

	def get_second_lowest_header(self):
		self._get_headerlist()
		return self.headerlist[-2]

	def add(self, string, heading_heirarchy: str):
		self._get_maplist()
		print(self.maplist)

		equivalent_h_h = self.clean_heading_heirarchy(heading_heirarchy)

		self.check_for_override_the_parent_header(equivalent_h_h)

		self.topic_map[equivalent_h_h][1] = string.strip()
		
	def clear_allchild_of_header(self, header: int):
		for item in self.topic_map:
			value = self.topic_map[item]
			if value[0] > header:
				self.topic_map[item][1] = ""

	def check_for_override_the_parent_header(self, equivalent_h_h):
		print(equivalent_h_h)
		if self.topic_map[equivalent_h_h][1]:
			self.clear_allchild_of_header(self.topic_map[equivalent_h_h][0])

def fact_blanker(fact):
	if re.search(r"\*.*\*", fact):
		blanked_fact = re.sub(r"(\*?\*[\w\s]+\*\*?)", "___________", fact)
		answer_that_is_blanked = re.findall(r"(\*?\*[\w\s]+\*\*?)", fact)
		return blanked_fact, answer_that_is_blanked
	else:
		return

def question_gen(acronym: str, line_topic: str, fact, blanked_fact="__", question_type=0):
	"""Generate question for the front

	Args:
		acronym (str): acronym type
		line_topic (str): lowest topic
		blanked_fact (str, optional): fact that has been blanked. Defaults to "__".
		question_type (int, optional): 0 for non-blank mode, 1 for blanked mode. Defaults to 0.

	Returns:
		list: [0] => question [1] => answer
	"""
	
	# warning: answer is deprecated
	blanked_fact = blanked_fact.strip()
	line_topic = line_topic.strip()

	question = acronyms_que[acronym][question_type]

	answer = line_topic if "~~" in question else fact # -> topic will be the answer if the quesion contains ~~
	
	return question.replace("==", line_topic).replace("__", blanked_fact).replace("~~", fact), answer
#change the way of questioning

def anki_card(topic, front, back):
	print("======================================")
	print(f"> {topic}\n")
	print(front)
	print("--------------fliped------------------")	
	print(back)
	print("======================================")