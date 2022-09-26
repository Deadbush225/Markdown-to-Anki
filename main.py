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

ignore_line_list = [
	"> [!source-image]"
]

acronyms_sub = {
	"thi": "thickness",
	"com": "components",
	"muo": "made up off",
	"wcf": "where we can find",
	"prop": "properties",
	"itis": "it is the",
	"pt": "parts of"
}

# == is for the topic, and ~~ is for the answer
acronyms_que = {
	"thi": "How thick is the ==?",
	"com": "== is composed of what?",
	"muo": "== is made up off what?",
	"wcf": "What we can find in the ==?",
	"prop": "What are the properties of the ==?",
	"itis": "What is the ==?",
	"pt": "What are the parts/type of ==?"
}

def question_gen(acronym: str, line_topic: str, answer: str):
	return acronyms_que[acronym].replace("==", line_topic) #. replace("~~", answer)

# Topic types
# - cycle -> part/step
# - term -> it is
# - disr -> (disregarded so it will be displayed as a topic) (default)

import fileinput
import re


test_str = """
### 1. Geosphere
2. Mantle
	- thickest part, biggest volume
	- covers the **core** and lies beneath the **crust**
	- pt; Parts of Mantle <- acts as a brancher/splitter
		- 2.1. outermost mantle
			- wcf; asthenosphere
			- cool, strong, and hard (solid)
			- pt; Parts of Mantle <- acts as a brancher/splitter
				- 2.1.1. asthenosphere
					- wcf; lava
				- 2.1.2. lavanosphere
					- wcf; magma
		- 2.2. innermost mantle
			- itis; hot, rock is not stable, soft,
			- prop; plastic, **magmatic**, viscous
"""

def anki_card(topic, front, back):
	print("======================================")
	print(f"> {topic}\n")
	print(front)
	print("--------------fliped------------------")	
	print(back)
	print("======================================")


with fileinput.input("Earth Subsystem.md", encoding="utf-8") as md_file:
	
	children_outlines = {}  # the key will be the brancher title : and the value will be the first childs
	
	# pre outlining
	for line in md_file:
	
		

		linetopic_tst = re.search(r"(?:- )?((?:\d\.)+) (.+)", line)  # -> "1." & "- 1.1."
		if linetopic_tst:
			linetopic_numbering = linetopic_tst[1]
			linetopic = linetopic_tst[2]
			if inside_branch:
				children_outlines[brancher_title].append(linetopic_tst[0])

		brancher_tst = re.search(r"pt; (.*)", line)
		if not brancher_tst:
			continue

		# inside_branch = True
		current_branch_linetopic_numbering = linetopic_numbering

		brancher_title = brancher_tst[1]

		children_outlines[brancher_title] = []
	

	depth = 0

	for line in test_str.split("\n"):
	# for line in md_file:
		
		if any((ignore in line) for ignore in ignore_line_list):
			continue

		topic_tst = re.search(r"#+ [!*]*((?:\d\.)+\s)?(.+)(?<!\*)", line)  # -> main heading
		if topic_tst:
			topic_numbering = topic_tst[1]
			topic = topic_tst[2]
			depth += 1
			continue
		
		linetopic_tst = re.search(r"(?:- )?((?:\d\.)+) (.+)", line)  # -> "1." & "- 1.1."
		if linetopic_tst:
			linetopic_numbering = linetopic_tst[1]
			linetopic = linetopic_tst[2]
			depth += 1
			continue

		bullet_test = re.search(r"- ", line)
		if bullet_test:
			acronym_test = re.search(r"- (.{1,10});", line)  # -> "- com;"
			if acronym_test:
				acronym = acronym_test[1]
				answer_test = re.search(r"- .{1,10}; (.*)", line)   # -> "iron, alloy, and nickel", can also be the title of the brancher
				answer = answer_test[1]
				
				if answer_test:

					# special properties
					if acronym == "pt":
						brancher_title = answer
						depth += 1


					else:
						front = question_gen(acronym, linetopic, answer)
				
					anki_card(topic, front, answer)
			else: # default acronym
				fact = re.search(r"- (.*)", line)[1]

				acronym = "itis"
				if re.search(r"\*.*\*", line): # emphasis check
					blanked_fact = re.sub(r"(\*?\*[\w\s]+\*\*?)", "___________", fact)
					blanked = re.findall(r"(\*?\*[\w\s]+\*\*?)", fact)
					answer = ", ".join(blanked)
					question = question_gen(acronym, blanked_fact, answer)
				else:
					# blanked_fact = ""
					# blanked = ""
					answer = linetopic
					question = question_gen(acronym, fact, answer)

				anki_card(topic, question, answer)

					

					

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