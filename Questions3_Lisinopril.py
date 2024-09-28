
#Med 3- Lisinopril

def ask_questions():
    # Define questions and their respective normal ranges or yes/no outcomes
    questions = [
        {"question": "On a scale of 0-10, how would you rate the severity of dizziness? (0 being extremely low, 10 being high)", "type": "scale", "normal_range": (0, 10)},
        {"question": "Are you experiencing diarrhoea?(yes/no)", "type": "yesno", "normal": "no"},
        {"question": "Are you experiencing severe chest pain? (yes/no)", "type": "yesno", "normal": "no"},
        {"question": "Are you experiencing severe cough? (yes/no)", "type": "yesno", "normal": "no"},
        {"question": "Does your skin or/and your eyes feel yellow? (yes/no)", "type": "yesno", "normal": "no"},
        {"question": "Is there swelling on your face, throat, tongue, lips, eyes, hands, feet, ankles, or lower legs? (yes/no)", "type": "yesno", "normal": "no"},
        {"question": "On a scale of 0-10, how would bad is your energy level? (0 being no issues, 10 being higher issues)", "type": "scale", "normal_range": (5, 10)},

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
    
    print("Please answer the following after you have taken your Lisinopril medication:")
    # Calculate the final score and decide on the action
    if critical_flag or score >= len(questions) * 2:  # Threshold to alert the doctor
        print("Alert: The patient's responses indicate they should see a doctor.")
    else:
        print("The patient's responses indicate normal reactions to the medication.")

ask_questions()
