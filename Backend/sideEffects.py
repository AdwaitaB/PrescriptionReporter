#python-3.10.12

import json
import pandas as pd

with open("medicineLookup.json", "r") as f:
    lookup = json.load(f)

sideEffects = pd.read_csv("RawData/ChSe-Decagon_monopharmacy.csv")

def getMedicationCode(name : str):
    return lookup.get(name)
    
def getSideEffects(code : str):
    return list(sideEffects.loc[sideEffects["# STITCH"] == code]["Side Effect Name"])

