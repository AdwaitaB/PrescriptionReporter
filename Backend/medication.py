import json
import pandas as pd

with open("medicineLookup.json", "r") as f:
    lookup = json.load(f)

drugToSE = pd.read_csv("drugToSE.csv")
questions = pd.read_csv("questions.csv")

class medication:
    name=""
    id=""
    commonSE=[]
    hazardSE=[]

    def __init__():
        pass

    def getMedication(self, search: str):
        self.name = search
        self.id = lookup[search]

        if (self.id == None):
            raise Exception("Medication not in database")
        
        self.commonSE = list(drugToSE.loc[drugToSE["DID"] == self.id and drugToSE["SAFETY"] == "NORMAL"]["SEID"])
        self.hazardSE = list(drugToSE.loc[drugToSE["DID"] == self.id and drugToSE["SAFETY"] == "DANGER"]["SEID"])

    def getQuestions(self):
        output = []
        for x in self.commonSE:
            output.append(question().getQuestion(x, False))
        for x in self.hazardSE:
            output.append(question().getQuestion(x, True))
        


class question:
    SEID = ""
    symptomName = ""
    severe = False
    text = ""
    lowerBound = ""
    higherBound = ""

    def __init__():
        pass

    def getQuestion(self, search: str, safety = False):
        self.SEID = search
        questionSet = questions.loc[questions["SEID"] == self.SEID]
        if not questionSet:
            raise Exception("Symptom does not exist")
        self.symptomName = questionSet["NAME"]
        self.severe = safety
        self.text = questionSet["QUESTION"]
        self.lowerBound = questionSet["LOWBOUND"]
        self.higherBound = questionSet["HIGHBOUND"]


    
