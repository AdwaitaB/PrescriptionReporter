import json
import pandas as pd

with open("medicineLookup.json", "r") as f:
    lookup = json.load(f)

drugToSE = pd.read_csv("drugToSE.csv")

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
        