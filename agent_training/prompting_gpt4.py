import g4f
import random

context=""

def generate_case():
    global context

    #content=["traffic", "crime", "environment", "family", "cybersecurity"]
    #select_content=content[random.randint(0,4)]
    select_content="traffic"
    prompt="Generate a 1 or 2 line case scenario where a person violates any of the " + select_content + " rule. \nGive a case after exploring all variety of cases that can be possible, dont just always give one of the most common ones \nGive only the case in double quotes and nothing else. Strictly NOT a single word extra. \nGive only one case, NOT multiple."#\nExplore the depth and every aspect of the field and give case"

    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.GetGpt, messages=[
                                     {"role": "user", "content": prompt}])#, stream=True)
    context= str(response)

    return context


def reward_prosecutor(prompt):
    print('Prosecutor: ', prompt)
    print(' ')
    #print(context)

    prompt= "\"" + prompt + "\" \n" + "is the above rule applies to the traffic case " + context + "\n" + "Answer in one word. 'Yes' or 'no' only. No extra word."#\nBe precise and accurate upto a decent level"

    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.GetGpt, messages=[
                                     {"role": "user", "content": prompt}])#, stream=True)
    print(response)
    
    if "yes" in (str(response)).lower():
        reward=10.0
        print('REWARDED \n')
    else:
        reward=-10.0
        print('penalized \n')

    return reward

def reward_defence(prompt):
    print('Defence: ', prompt)
    print('')
    #print(context)

    #prompt="Assume a court scenario \nBen is accused in the case: "+ context + "\nStephen is a lawyer, trying to defend Ben in this case. Now Ben is thinking what to say. Can saying "+ "\"" + prompt + "\" save Ben?\nAssuming everything said is true \nBe lineant.\nSay 'Yes' or 'No' only. No extra word. Not a single extra. " #"\" \n" + "can this statement be told in a court by the defence lawyer to save the accused in the case " + context + " ?\n" + "Answer in one word. 'Yes' or 'no' only. No extra word. \nBe lineant."
    prompt= "\"" + prompt + "\" \n" + "is the above statement relates to the statement " + context + "\n" + "Answer in one word. 'Yes' or 'no' only. No extra word.\nBe lineant"

    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.GetGpt, messages=[
                                     {"role": "user", "content": prompt}])#, stream=True)
    
    if "yes" in (str(response)).lower():
        reward=10.0
        print('REWARDED \n')
    else:
        reward=-10.0
        print('penalized \n')

    return reward