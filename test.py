import backend.medication as med

test = med.medication()
test.getMedication("insulin")
for x in test.getQuestions():
    print(x.__dict__)