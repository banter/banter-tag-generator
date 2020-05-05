import stanza

# stanza.download('en')       # This downloads the English models for the neural pipeline
nlp = stanza.Pipeline('en')  # This sets up a default neural pipeline in English

topic_list = ["Cowboys lose Browns bounce back",
              "Bucs win",
              "TB12 declining?",
              "Burfict suspended",
              "Pick ems Week 5",
              "Clemson escapes",
              "Auburn vs Florida",
              "ESPN NBA top 10",
              "Breakout players",
              "CA Pass bill for college players",
              "Baseball update"]


def createListOfPeople(doc: nlp, ):
    for index, sentence in enumerate(doc.sentences):
        print(sentence.ents)
        for entitie in sentence.ents:
            if entitie.type == "PERSON":
                if entitie.text in people:
                    people[entitie.text] += 1
                else:
                    people[entitie.text] = 1


desc_tags = {}

for index, value in enumerate(topic_list):
    doc = nlp(topic_list[index])
    desc_tags[value] = doc.entities

entities = {
    "test": None,
    "type": None,
    "start_char": None,
    "end_char": None
}

people = {
}
