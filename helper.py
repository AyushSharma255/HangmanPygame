import os
import json
import requests
from random import choice

class GameHelper:
    # assets
    base = os.path.dirname(__file__)
    assets = os.path.join(base, "assets")

    # text
    text = os.path.join(assets, "text")
    dictionary = os.path.join(text, "sowpods.txt")

    # image
    image = os.path.join(assets, "image")

    @classmethod
    def getWord(cls):
        wordsList = list(open(cls.dictionary))

        return choice(wordsList)

    @staticmethod
    def defineWord(word):
        try:
            req = requests.get(
                f"https://od-api.oxforddictionaries.com:443/api/v2/entries/en-gb/{word.lower()}",
                headers={
                    "app_id": "6dc81302",
                    "app_key": "d6ce4b76d936715148be5ca71309280b"
                }
            )

            wordJSON = req.json()
            wordDefinition = wordJSON["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
        except (KeyError, json.decoder.JSONDecodeError):
            wordDefinition = "A word in the sowpods dictionary."

        return wordDefinition
