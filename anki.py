import genanki
import random

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


my_note = genanki.Note( # 1. contains the fact need to memorize, can contain 1+ card/s
  model=my_model,
  fields=['JPEG File', '<img src="test.png">'])

my_deck = genanki.Deck( # 3. to import your notes into Anki, you need to add them to a "Deck"
  model_no,
  'Example')

my_deck.add_note(my_note) # 3.1 adding note to a deck

my_package = genanki.Package(my_deck) # 4. Then, create a "Package" for your "Deck" and write it to a file
my_package.media_files = ['test.png']

my_package.write_to_file('output.apkg')