'''
This file is primarily for storing the questions and options for the COVID-19 Self-Assessment
The COVID.py file will access this file to obtain the questions
'''


test_questions = {
    'Do you feel any of the following Symptoms?': [
        'Fever or chills' , 
        'Dry Coughs', 
        'Shortness of Breath or Difficulty Breathing', 
        'Fatigue', 
        'Muscle or Body Aches', 
        'Headaches',
        'New loss of taste or smell',
        'Sore Throat',
        'Congestion or Runny Nose',
        'Nausea or Vomiting',
        'Diarrhea',
    ],
    'Do you have any of the following emergency warning signs?' : [
        'Trouble breathing',
        'Persistent pain or pressure on chest',
        'New Confusion',
        'Inability to awake or to stay awake',
        'Bluish Lips or Face'
    ],
    'Have you been in Contact with another positive-tested person in the past 14 days?' : [
        'Yes',
        'No'
    ]
}

only_questions = [
    'Do you feel any of the following Symptoms?', 
    'Do you have any of the following emergency warning signs?',
    'Have you been in Contact with another positive-tested person in the past 14 days?'
]

contact_question = 'Have you been in Contact with another positive-tested person in the past 14 days?'
moderate_check = 'Do you feel any of the following Symptoms?'
extreme_check = 'Do you have any of the following emergency warning signs?'