import pprint
from helpers import *

pp = pprint.PrettyPrinter(indent=4)

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

# make it: 
# what is the **3rd planet from the sun and the **largest** terrestrial planet
# ==Earth== planet from the sun and the **largest** terrestrial planet 

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
			
			# [implied acronym] - td
			inline_term_def_test = re.search(r"(?:-\s)?(.+)[ ]+-[ ]+(.+)", fact)
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



			else:
				acronym_test = re.search(r"^(?:\s*(-|#+)) (.{1,10});\s*(.*)\s*", line)  # -> "- com;"
				if acronym_test:
					acronym = acronym_test[2]
					# line = acronym_test[2]
					fact = acronym_test[3]
					# answer_test = re.search(r".{1,10}; (.*)", line)   # -> "iron, alloy, and nickel", can also be the title of the brancher
					# answer = answer_test[1]
					
					# if answer_test:
					# question = ""
					

					# special properties
					if acronym == "pt": # -> blank no support
						brancher_title = fact
						# depth += 1
						answer = " - " + "\n - ".join(children_outlines[brancher_title])
						front = question_gen(acronym, brancher_title)

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
			
			anki_card(topic_map.get_topic_map_string(), front, answer)
			# front = None
			# answer = None
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