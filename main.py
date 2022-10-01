import pprint

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
		self.headerlist = [self.topic_map[val][1] for val in ["h1", "h2", "h3", "h4", "h5", "h6", "h7"] if self.topic_map[val][1]]
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

pp = pprint.PrettyPrinter(indent=4)

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
	"pt": "parts of"
}

# warning: answer is deprecated
# == is for the topic, and ~~ is for the answer, and __ is for the blanked_fact
# the first item in the list is the nonblanked question while the second item is the blanked question
acronyms_que = {
	"thi": ["How thick is the ==?", "thi - NaN"],
	"com": ["== is composed of what?", "== is made up of: \n\n __"],
	"mofs": ["== is made up off what?", "== is made up of: \n\n __"],
	"wcf": ["What we can find in the ==?", "wcf - NaN"],
	"prop": ["What are the properties of the ==?", "The properties of == are: \n\n __"],
	"it": ["What is the ==?", "== __"], 
	"itis": ["What is the ==?", "== is the __"],
	"has": ["has __", "has - NaN"],
	"ff": ["Fun fact: __", "ff - NaN"],
	"ithas": ["it has __?", "it has - NaN"],
	"pt": ["What are the parts of ==?", "== have parts which are: \n\n __"], # -> the part of is in the linetopic title
}

def fact_blanker(fact):
	if re.search(r"\*.*\*", fact):
		blanked_fact = re.sub(r"(\*?\*[\w\s]+\*\*?)", "___________", fact)
		answer_that_is_blanked = re.findall(r"(\*?\*[\w\s]+\*\*?)", fact)
		return blanked_fact, answer_that_is_blanked
	else:
		return

def question_gen(acronym: str, line_topic: str, blanked_fact="__", question_type=0):
	"""Generate question for the front

	Args:
		acronym (str): acronym type
		line_topic (str): lowest topic
		blanked_fact (str, optional): fact that has been blanked. Defaults to "__".
		question_type (int, optional): 0 for non-blank mode, 1 for blanked mode. Defaults to 0.

	Returns:
		_type_: _description_
	"""
	
	# warning: answer is deprecated
	blanked_fact = blanked_fact.strip()
	line_topic = line_topic.strip()
	
	return acronyms_que[acronym][question_type].replace("==", line_topic).replace("__", blanked_fact) #.replace("~~", answer)
#change the way of questioning


# Topic types
# - cycle -> part/step
# - term -> it is
# - disr -> (disregarded so it will be displayed as a topic) (default)
# - cont -> continuation mode; Topic provides ....

import fileinput
import re


### 1. Geosphere
test_str = """
## Subsystems of the Earth
#### 1. Geosphere 
> [!source-image]-
![[Pasted image 20220906104440.png]]
##### Consists of 3 major layers
> [!source-image]-
![[Pasted image 20220906104507.png]]
1. Core
	- com; heavy metals
	- 1.1. Outer Core
		- thi; 1400 miles thick
		- com; iron, alloy, and nickel
	- 1.1. Inner Core
		- thi; 750 miles thick
		- com; made up of primary iron

> [!source-image]-
![[Pasted image 20220906104532.png]]
2. Mantle
	- itis; thickest part, biggest volume
	- it; covers **core** and lies beneath the **crust**
	- 2.1. outermost mantle
		- wcf; asthenosphere
		- cool, strong, and hard (solid)
	- 2.2. innermost mantle
		- itis; hot, rock is not stable, soft,
		- prop; plastic, **magmatic**, viscous
"""

# make it: 
# what is the **3rd planet from the sun and the **largest** terrestrial planet
# ==Earth== planet from the sun and the **largest** terrestrial planet 


def anki_card(topic, front, back):
	print("======================================")
	print(f"> {topic}\n")
	print(front)
	print("--------------fliped------------------")	
	print(back)
	print("======================================")


with fileinput.input("Earth Subsystem.md", encoding="utf-8") as md_file:
	
	children_outlines = {}  # the key will be the brancher title : and the value will be the first childs
	# current_outline_ch = {}


	# pre outlining
	brancher_map = []
	inside_branch = False
	depth = 0
	# for line in md_file:
	for line in test_str.split("\n"):

		brancher_tst = re.search(r"(mofs|pt|scr); (.*)", line)
		if brancher_tst:
			# continue
			# pass

			# inside_branch = True

			brancher_title = brancher_tst[2]
			brancher_map.append(brancher_title)

			children_outlines[brancher_title] = []

		# current_outline = current_outline_ch if current_outline_ch else children_outlines
		# -> numbering
		linetopic_tst = re.search(r"(?:- )?((?:\d\.)+) (.+)", line)  # -> "1." & "- 1.1."
		if linetopic_tst:
			linetopic_numbering = linetopic_tst[1]
			linetopic = linetopic_tst[2]
			if inside_branch:

				if linetopic_numbering.count(".") < previous_linetopic_numbering.count("."):
					# depth -= 1
					brancher_map.pop()

				# children_outlines[brancher_title][linetopic_numbering[:-2]] = []
				children_outlines[brancher_map[-1]].append(linetopic)
				# if linetopic_numbering.count(".") > previous_linetopic_numbering.count("."):

		
			previous_linetopic_numbering = linetopic_numbering

		else:
			if brancher_map:
				indent_check = re.search(r"^(\s)- (.*)", line)
				if indent_check:
					depth = indent_check[1].replace("\t", "    ")
					fact = indent_check[2]

					children_outlines[brancher_map[-1]].append(fact)

		# brancher_tst = re.search(r"(mofs|pt|scr); (.*)", line)
		# if not brancher_tst:
		# 	continue

		# inside_branch = True

		# brancher_title = brancher_tst[1]
		# brancher_map.append(brancher_title)

		# children_outlines[brancher_title] = []

	pp.pprint(children_outlines)

	# exit()

with fileinput.input("Earth Subsystem.md", encoding="utf-8") as md_file:
	# card creation
	depth = 0

	topic_map = TopicMap()

	topic = ""
	linetopic = ""
	for line in test_str.split("\n"):
	# for line in md_file:
		
		if any((ignore in line) for ignore in ignore_line_list):
			continue

		topic_tst = re.search(r"(#+) [!*]*((?:\d\.)+\s)?(.+)(?<!\*)", line)  # -> main heading
		if topic_tst:
			# topic_numbering = topic_tst[2]
			# topic = topic_tst[3]
			hash_num = topic_tst[1]
			topic_map.add(topic_tst[3], hash_num)
			# depth += 1
			continue
		
		linetopic_tst = re.search(r"(?:- )?((?:\d\.)+) (.+)", line)  # -> "1." & "- 1.1."
		if linetopic_tst:
			# linetopic_numbering = linetopic_tst[1]
			# linetopic = linetopic_tst[2]
			topic_map.add(linetopic_tst[2], "h7")
			# depth += 1
			continue

		bullet_test = re.search(r"- ", line)
		if bullet_test:

			fact = re.search(r"^(?:\s*(-|#+)) (?:.*;)?(.*)", line)[2] # the whole fact after the dash (-)

			acronym_test = re.search(r"^(?:\s*(-|#+)) (.{1,10});\s*(.*)\s*", line)  # -> "- com;"
			if acronym_test:
				acronym = acronym_test[2]
				# line = acronym_test[2]
				answer = acronym_test[3]
				# answer_test = re.search(r".{1,10}; (.*)", line)   # -> "iron, alloy, and nickel", can also be the title of the brancher
				# answer = answer_test[1]
				
				# if answer_test:
				# question = ""
				

				# special properties
				if acronym == "pt": # -> blank no support
					brancher_title = answer
					# depth += 1
					answer = " - " + "\n - ".join(children_outlines[brancher_title])
					front = question_gen(acronym, brancher_title)

					continue

				elif acronym == "mofs":
					brancher_title = answer

					answer = " - " + "\n - ".join(children_outlines[brancher_title])

					is_blankable = fact_blanker(answer)
					if is_blankable:
						blanked_fact, answer = is_blankable
						front = question_gen(acronym, topic_map[-1], blanked_fact=blanked_fact, question_type=1)
					else:
						front = question_gen(acronym, topic_map[-1])

				# elif acronym == "ithas":
					# front = question_gen(acronym, topic_map[-1], answer, blanked_fact)
				else:
					# acronym = "itis"
					is_blankable = fact_blanker(answer)
					if is_blankable:
						blanked_fact, answer = is_blankable
						front = question_gen(acronym, topic_map[-1], blanked_fact=blanked_fact, question_type=1)
					else:
						front = question_gen(acronym, topic_map[-1])
				# front = question_gen(acronym, topic_map[-1], answer)

			# acronym = "itis"
			if re.search(r"\*.*\*", line): # emphasis check
				# blanked_fact = re.sub(r"(\*?\*[\w\s]+\*\*?)", "___________", fact)
				answer_to_the_blanked = re.findall(r"(\*?\*[\w\s]+\*\*?)", fact)
				# answer = ", ".join(blanked)

				for answer in answer_to_the_blanked:
					blanked_fact = line.replace(answer, "___________")

					front = question_gen(acronym, topic_map[-1], blanked_fact=blanked_fact)
					anki_card(topic_map.get_topic_map_string(), front, answer)

				continue
				

				# question = question_gen(acronym, blanked_fact, answer)
			# else:
				# blanked_fact = ""
				# blanked = ""
				# answer = linetopic
				# question = question_gen(acronym, fact, answer)

			# anki_card(topic_map[-2], question, answer)	
			
			anki_card(topic_map.get_topic_map_string(), front, answer)
			# else: # default acronym
				
				
				# if no emphasis, hide all

				# if there is, hide the emphasis

		



		
		
		# topic checker:
			# topic identifier


		# emphasis replacer


# --- #

# import genanki

# my_model = genanki.Model( # 2. defines the fields and cards for a type of "Note"
#   1380120064,
#   'Example',
#   fields=[ # fields acts as a parameter, and this model as a function
#     {'name': 'Object'},
#     {'name': 'Image'},
#   ],
#   templates=[
#     {
#       'name': 'Card 1',
#       'qfmt': '{{Object}}<br>{{Image}}',
#       'afmt': '{{FrontSide}}<hr id="answer">{{Image}}',
#     },
#   ])

# my_note = genanki.Note( # 1. contains the fact need to memorize, can contain 1+ card/s
#   model=my_model,
#   fields=['JPEG File', '<img src="test.png">'])

# my_deck = genanki.Deck( # 3. to import your notes into Anki, you need to add them to a "Deck"
#   2059400191,
#   'Example')

# my_deck.add_note(my_note) # 3.1 adding note to a deck

# my_package = genanki.Package(my_deck) # 4. Then, create a "Package" for your "Deck" and write it to a file
# my_package.media_files = ['test.png']

# my_package.write_to_file('output.apkg')