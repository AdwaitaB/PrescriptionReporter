
#Med 2: Clonidine
def ask_questions():
    # Define questions and their respective normal ranges or yes/no outcomes
    questions = [

        {"question": "On a scale of 0-10, how would you rate the severity of dizziness? (0 being none, 10 being severe)",  "type": "scale", "normal_range": (0, 5)},
        {"question": "Are you experiencing a dry mouth? (yes/no)", "type": "yesno", "normal": "no"},
        {"question": "Do you feel constipated? (yes/no)", "type": "yesno", "normal": "no"},
        {"question": "On a scale of 0-10, how irritable do you feel?", "type": "scale", "normal_range": "0,3"},
        {"question": "One a scale of 0-10, what level of difficulty in breathing are you facing? (0 being none, 10 being severe)", "type": "scale", "normal_range": (0, 3)},
        {"question": "Do you have any signs of allergic reaction: hives, swelling of face/lips/tongue/throat?(yes/no)", "type": "yesno", "normal": "no"},
        {"question": "On a scale of 0-10, how much pain do you feel in your chest? (0 being no pain, 10 being severe)", "type": "scale", "normal_range": (0, 2)},
       
    ]
    
    score = 0
    critical_flag = False
    
    for q in questions:
        if q["type"] == "yesno":
            answer = input(q["question"] + " ").strip().lower()
            if answer != q["normal"]:
                score += 3  # Higher score for critical symptoms
                critical_flag = True
            else:
                score += 1  # Lower score for normal response
        elif q["type"] == "scale":
            answer = int(input(q["question"] + " "))
            if q["normal_range"][0] <= answer <= q["normal_range"][1]:
                score += 1  # Lower score for normal range
            else:
                score += 3  # Higher score for abnormal response
                critical_flag = True
    
    
    # Calculate the final score and decide on the action
    if critical_flag or score >= len(questions) * 2:  # Threshold to alert the doctor
        print("Alert: The patient's responses indicate they should see a doctor.")
    else:
        print("The patient's responses indicate normal reactions to the medication.")
        
print("Please answer the following after you have taken your Clonidine medication:")
ask_questions()
