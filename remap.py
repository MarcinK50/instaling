import json
f = open('words.json')
words = json.load(f)
final_dict = {}

for word in words:
    try:
        final_dict[word['questionId']] = word['answer']
    except:
        final_dict[word['questionId']] = ""

with open("remaped_words.json", "w") as outfile: 
    json.dump(final_dict, outfile)