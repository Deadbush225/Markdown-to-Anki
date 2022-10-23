import pprint
from helpers import *

pp = pprint.PrettyPrinter()

# Topic types
# - cycle -> part/step
# - term -> it is
# - disr -> (disregarded so it will be displayed as a topic) (default)
# - cont -> continuation mode; Topic provides ....

import fileinput
import re

### 1. Geosphere
test_str = """
##### **Layers of Atmosphere**
> [!source-image]+
![[Pasted image 20220906105712.png]]

###### 1. Troposphere
> [!source-image]-
![[Pasted image 20220906105715.png]]
- thi; **10** km
- wh; Formation of weather
- Jet stream - fast flowing narrow, meandering air currents
- Tropopause - border to stratosphere
"""

import genanki
import random

def anki_card(topic, front, back):
	global my_model
	global my_deck

	print("======================================")
	print(f"> {topic}\n")
	print(front)
	print("--------------fliped------------------")	
	print(back)
	print("======================================")

	my_note = genanki.Note( # 1. contains the fact need to memorize, can contain 1+ card/s
	model=my_model,
	fields=[front, back])

	my_deck.add_note(my_note) # 3.1 adding note to a deck

def initializeAnkiDeck():
	global my_model
	global my_deck

	model_no = random.randrange(1 << 30, 1 << 31)

	my_model = genanki.Model( # 2. defines the fields and cards for a type of "Note"
	model_no,
	'Example',
	fields=[ # fields acts as a parameter, and this model as a function
		{'name': 'Question'},
		{'name': 'Answer'},
	],
	templates=[
		{
		'name': 'Card 1',
		'qfmt': '{{Question}}<br>',
		'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
		},
	])


	my_deck = genanki.Deck( # 3. to import your notes into Anki, you need to add them to a "Deck"
	model_no,
	'Example')

# make it: 
# what is the **3rd planet from the sun and the **largest** terrestrial planet
# ==Earth== planet from the sun and the **largest** terrestrial planet 

mdfile = r"D:\Obsidian Vault\School Notes\Introduction to Philosophy\A. Intro to Philosophy.md"

with open(mdfile, encoding="utf-8") as md_file:
	
	children_outlines = {}  # the key will be the brancher title : and the value will be the first childs
	# current_outline_ch = {}

	md_file = md_file.readlines()

	# pre outlining
	brancher_map = []
	inside_branch = False
	depth = 0
	line_no = 0
	# for line in test_str.split("\n"):
	for line in md_file:
		line_no += 1

		brancher_tst = re.search(r"(.*) (mofs|pt|kd|cyc|st); (.*)", line) #acronym
		if brancher_tst:
			if brancher_tst[2]:
				# continue
				# pass

				# inside_branch = True

				# -> scope detector
				start_line_no = line_no

				scope_to_find = brancher_tst[1]
				brancher_title = brancher_tst[3]
				brancher_map.append(brancher_title)

				starting_scope = Topic(brancher_title, scope_to_find)

				children_outlines[brancher_title] = []

				done = False
				phantom_line_no = line_no
				while not done:

					# need to check if it is a member of the topic heirarchy
					topic_test = re.search(r"^([ 	]*[#\-\d.]+ )(.*)", md_file[phantom_line_no])
					
					if topic_test:
						possible_end_scope = Topic(topic_test[2], topic_test[1])

						if starting_scope <= possible_end_scope:
							done = True
							end_line_no = phantom_line_no - 1

					if not phantom_line_no + 1 == len(md_file):
						phantom_line_no += 1
					else:
						done = True
						end_line_no = phantom_line_no
					# and if it is, compare it to the starting scope. If it is lower that [sc], ignore, else if it is higher make it the ending scope

					# if md_file[phantom_line_no].startswith(scope_to_find + " "):# test for the end scope:
					# 	done = True
					# 	end_line_no = phantom_line_no - 1 # don't include the endline
						# save end line no then, return the str or range


				# -> first children detector
				first_children_found = False
				for i in range(start_line_no, end_line_no+1):
					line = md_file[i]
					
					if not first_children_found:
						children_test = re.search(r"^([	 ]*[#\-\d]+ )(.*)", line)
						
						if children_test:
							first_children = children_test[1] # -> "### " or "- "
							first_children_top = children_test[2]
							first_children_found = True
							first_children_topic = Topic(first_children_top, first_children)

						else:
							continue
						#todo: use case if children_test is not found
					
					topic_test = re.search(r"^([ 	]*[#\-\d]+ )(.*)", line)

					if topic_test:
						possible_first_child_topic = Topic(topic_test[2], topic_test[1])
					# if line.startswith(first_children):
						if first_children_topic == possible_first_child_topic:
							children_outlines[brancher_title].append(line)
						elif first_children_topic < possible_first_child_topic:
							break
				

		# current_outline = current_outline_ch if current_outline_ch else children_outlines
		# -> numbering
		# linetopic_tst = re.search(r"(?:- )?((?:\d\.)+) (.+)", line)  # -> "1." & "- 1.1."
		# if linetopic_tst:
		# 	linetopic_numbering = linetopic_tst[1]
		# 	linetopic = linetopic_tst[2]
		# 	if inside_branch:

		# 		if linetopic_numbering.count(".") < previous_linetopic_numbering.count("."):
		# 			# depth -= 1
		# 			brancher_map.pop()

		# 		# children_outlines[brancher_title][linetopic_numbering[:-2]] = []
		# 		children_outlines[brancher_map[-1]].append(linetopic)
		# 		# if linetopic_numbering.count(".") > previous_linetopic_numbering.count("."):

		
		# 	previous_linetopic_numbering = linetopic_numbering

		# else:
		# 	if brancher_map:				

		# 		indent_check = re.search(r"^(\s*)- (.*)", line)
		# 		if indent_check:
		# 			previous_depth = indent_check[1].replace("\t", "    ")
		# 			fact = indent_check[2]

		# 			children_outlines[brancher_map[-1]].append(fact)
		# ->



		# brancher_tst = re.search(r"(mofs|pt|scr); (.*)", line)
		# if not brancher_tst:
		# 	continue

		# inside_branch = True

		# brancher_title = brancher_tst[1]
		# brancher_map.append(brancher_title)

		# children_outlines[brancher_title] = []

	pp.pprint(children_outlines)

	# exit()

initializeAnkiDeck()

with fileinput.input(mdfile, encoding="utf-8") as md_file:
	# card creation
	depth = 0

	topic_map = TopicMap()

	topic = ""
	linetopic = ""
	# for line in test_str.split("\n"):
	for line in md_file:
		
		if any((ignore in line) for ignore in ignore_line_list):
			continue

		callout_topic_tst = re.search(r"^(?:\s*> \[!(info)\]).\s*(.*)", line)
		if callout_topic_tst:
			topic_map.add(callout_topic_tst[2] if callout_topic_tst[2] else callout_topic_tst[1], "h7")
			continue

		topic_tst = re.search(r"(#+) [!*]*((?:\d\.)+\s)?(.+)(?<!\*)", line)  # -> main heading
		if topic_tst:
			# topic_numbering = topic_tst[2]
			# topic = topic_tst[3]
			hash_num = topic_tst[1]
			topic_map.add(topic_tst[3], hash_num)
			# depth += 1

			
			# continue
		
		linetopic_tst = re.search(r"^\s*(?:- )?(?:\*\*)?((?:\d\.)+)?(?:\*\*)(.+)(?:\*\*)", line)  # -> "1." & "- 1.1."
		if linetopic_tst:
			# linetopic_numbering = linetopic_tst[1]
			# linetopic = linetopic_tst[2]
			topic_map.add(linetopic_tst[2], "h7")
			# depth += 1
			continue

		bullet_test = re.search(r"^(\s*-\s*)", line)
		if bullet_test:

			fact = re.search(r"^(\s*>)?(?:\s*(-|#+)) (?:.*;)?(.*)", line)[3] # the whole fact after the dash (-)
			
			# [implied acronym] - td
			inline_term_def_test = re.search(r"^(?:-\s+)?(.+)[ ]+-[ ]+(.+)", fact)
			if inline_term_def_test:
				topic_map.add(inline_term_def_test[1], "h8") # need to add as a topic because, because it will be used as a last topic below

				term = inline_term_def_test[1]
				fact_def = inline_term_def_test[2]
				
				# question_type = 0 # CLass is near, just check if fact as the question is available, else make one
									# it is gonna be difficult if you just asked what is **term** so try to ask both (q: fact, a: term) and (q: term, a: fact)
				
				is_blankable = fact_blanker(fact_def)
				if is_blankable:
					blanked_fact, answer = is_blankable
					front, answer = question_gen("td", topic_map[-1], fact, blanked_fact=blanked_fact, question_type=1)
				else:
					front, answer = question_gen("td", topic_map[-1], fact)
				
				topic_map.clear_allchild_of_header_including_the_header("h8")

			# -> else:
		acronym_test = re.search(r"^(?:[	 ]*(-|#+))\s+(.{1,10});\s*(.*)\s*", line)  # -> "- com;"
		if acronym_test:
			acronym = acronym_test[2]
			# line = acronym_test[2]
			fact = acronym_test[3]
			# answer_test = re.search(r".{1,10}; (.*)", line)   # -> "iron, alloy, and nickel", can also be the title of the brancher
			# answer = answer_test[1]
			
			# if answer_test:
			# question = ""
			

			# special properties
			if acronym in ["pt", "kd", "cyc", "st"]: # -> blank no support
				brancher_title = fact
				if bullet_test:
					topic_map.add(brancher_title, "h7")
				# depth += 1
				prop_answer = "\n -> " + "\n -> ".join(children_outlines[brancher_title])
				front, answer = question_gen(acronym, brancher_title, fact, proposed_answer=prop_answer)
				# continue

			elif acronym == "mofs":
				brancher_title = fact

				fact = " - " + "\n - ".join(children_outlines[brancher_title])

				is_blankable = fact_blanker(fact)
				if is_blankable:
					blanked_fact, answer = is_blankable
					front, answer = question_gen(acronym, topic_map[-1], fact, blanked_fact=blanked_fact, question_type=1)
				else:
					front, answer = question_gen(acronym, topic_map[-1], fact)

			# elif acronym == "ithas":
				# front = question_gen(acronym, topic_map[-1], answer, blanked_fact)
			else:
				# acronym = "itis"
				is_blankable = fact_blanker(fact)
				if is_blankable:
					blanked_fact, answer = is_blankable
					front, answer = question_gen(acronym, topic_map[-1], fact, blanked_fact=blanked_fact, question_type=1)
				else:
					front, answer = question_gen(acronym, topic_map[-1], fact)
			# front = question_gen(acronym, topic_map[-1], answer)
		else:
			if "fact" in globals():
				is_blankable = fact_blanker(fact)
				if is_blankable:
					blanked_fact, answer = is_blankable
					front, answer = question_gen("itis", topic_map[-1], fact, blanked_fact=blanked_fact, question_type=1)
				else:
					front, answer = question_gen("itis", topic_map[-1], fact)
			# acronym = "itis"
			#->
			# if re.search(r"\*.*\*", line): # emphasis check
			# 	# blanked_fact = re.sub(r"(\*?\*[\w\s]+\*\*?)", "___________", fact)
			# 	answer_to_the_blanked = re.findall(r"(\*?\*[\w\s]+\*\*?)", fact)
			# 	# answer = ", ".join(blanked)

			# 	for answer in answer_to_the_blanked:
			# 		blanked_fact = line.replace(answer, "___________")

			# 		front = question_gen(acronym, topic_map[-1], blanked_fact=blanked_fact)
			# 		anki_card(topic_map.get_topic_map_string(), front, answer)

			# 	continue
			#->
				

				# question = question_gen(acronym, blanked_fact, answer)
			# else:
				# blanked_fact = ""
				# blanked = ""
				# answer = linetopic
				# question = question_gen(acronym, fact, answer)

			# anki_card(topic_map[-2], question, answer)	
		if ("front" in globals()) and ("answer" in globals()):
			anki_card(topic_map.get_topic_map_string(), front, answer)
		else:
			print(f"Ignoring line no: {md_file._filelineno}")
			# front = None
			# answer = None
			# else: # default acronym
				
				
				# if no emphasis, hide all

				# if there is, hide the emphasis

		



		
		
		# topic checker:
			# topic identifier


		# emphasis replacer


# --- #

my_package = genanki.Package(my_deck) # 4. Then, create a "Package" for your "Deck" and write it to a file
my_package.media_files = ['test.png']

my_package.write_to_file('output.apkg')