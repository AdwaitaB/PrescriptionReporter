import json
import pandas as pd
import random

with open("medicineLookup.json", "r") as f:
    lookup = json.load(f)

drugToSE = pd.read_csv("drugToSE.csv")
questions = pd.read_csv("questions.csv")

class medication:
    name=""
    id=""
    commonSE=[]
    hazardSE=[]

    def __init__(self):
        pass

    def getMedication(self, search: str):
        self.name = search
        self.id = lookup[search]

        if (self.id == None):
            raise Exception("Medication not in database")
        
        self.commonSE = list(drugToSE.loc[drugToSE["DID"] == self.id].loc[drugToSE["SAFETY"] == "NORMAL"]["SEID"])
        self.hazardSE = list(drugToSE.loc[drugToSE["DID"] == self.id].loc[drugToSE["SAFETY"] == "HAZARD"]["SEID"])

        return self

    def getQuestions(self):
        output = []
        for x in self.commonSE:
            output.append(question(x, False).__dict__)
        for x in self.hazardSE:
            output.append(question(x, True).__dict__)
        for x in random.sample(list(questions.loc[~questions["SEID"].isin(self.commonSE)].loc[~questions["SEID"].isin(self.hazardSE)]["SEID"]), 5):
            output.append(question(x, "FAKE").__dict__)

        random.shuffle(output)

        return output
        


class question:
    SEID = ""
    symptomName = ""
    severe = False
    text = ""
    lowerBound = ""
    higherBound = ""

    def __init__(self, search = None, safety = False):
        if (search != None):
            self.getQuestion(search, safety)
        pass

    def getQuestion(self, search: str, safety = False):
        self.SEID = search
        questionSet = questions.loc[questions["SEID"] == self.SEID]
        if questionSet.empty:
            raise Exception("Symptom does not exist")
        self.symptomName = questionSet["NAME"].iloc[0]
        self.severe = safety
        self.text = questionSet["QUESTION"].iloc[0]
        self.lowerBound = questionSet["LOWBOUND"].iloc[0]
        self.higherBound = questionSet["HIGHBOUND"].iloc[0]

        return self


    
