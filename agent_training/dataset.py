import csv
import sys

file_path = '/Users/sumitprakash/Desktop/ArgueAI_ppo/agent_training/dataset_final.csv'
index= -1
cases = []

def case_context():
    global index
    global cases

    while not cases:
        index += 1

        if(index >= 43):
            #return 0
            index = 0
            '''print('Training completed')
            sys.exit()'''

        if (index == 34 or index == 21):
            index += 1

        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            i=0
            for row in reader:
                if(i==index):
                    data = row
                i+=1
        cases = data[3].split('|')
    
    data = cases[0]
    cases.pop(0)

    return data

def reward_prosecutor(argument):
    global index

    if (argument == index):
        reward= 10.0
        print('\n\n \t REWARDED')
    else:
        reward= -10.0
        print('\npenalized')

    return reward

def reward_defence(argument):
    global index

    if (argument == index):
        reward= 10.0
        print('\n\n \t REWARDED')
    else:
        reward= -10.0
        print('\npenalized')

    return reward