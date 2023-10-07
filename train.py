import gym
import numpy as np
from Prosecutor_final import Agent as prosecutor_agent
from Defence_final import Agent as defence_agent
from utils import plot_learning_curve
import os
from sentence_transformers import SentenceTransformer
import corpus_data 

#from env_final import *
from env_ArgueAI import *

model_sbert = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
def Tokenize(state,model = model_sbert):
        # Tokenize the prompt with bert
        sentence= state
        embeddings = model.encode(sentence)
        embeddings=torch.tensor(embeddings)
        embeddings=embeddings.view(1,-1)
        return embeddings

if __name__ == '__main__':
    #env = gym.make('CartPole-v0')
    env = CourtRoomEnvironment()
    N = 80
    batch_size = 64
    n_epochs = 20
    alpha = 0.0002
    prosecutor = prosecutor_agent(n_actions=len(env.prosecutor_action_space), batch_size=batch_size, 
                    alpha=alpha, n_epochs=n_epochs, 
                    input_dims=384*3) # s-bert embedding size = 384
    defence = defence_agent(n_actions=len(env.defence_action_space), batch_size=batch_size, 
                    alpha=alpha, n_epochs=n_epochs, 
                    input_dims=384*4) # s-bert embedding size = 384
    
    try:
        prosecutor.load_models()
        defence.load_models()
    except:
        print('No saved model found. Starting from scratch')
    
    n_games = 300

    figure_file = 'plots/ArgueAI.png'

    best_score = 10 # Changable parameter
    score_history = []

    learn_iters = 0
    avg_score = 0
    n_steps_prosecutor = 0
    n_steps_defence = 0

    file_path= 'memory/n_episodes.txt'
    if os.path.exists(file_path):
    # If the file exists, read the value from it
        with open(file_path, "r") as file:
            n_episodes = int(file.read())
    else:
        # If the file doesn't exist, initialize the variable
        n_episodes = 0

    while True:
        try:
            observation = env.reset()
            done = False
            score = 0
            prosecutor_flag= False
            defence_flag= False

            for j in range(300):
                if not prosecutor_flag:
                    prosecutor_action, prosecutor_prob, prosecutor_val = prosecutor.choose_action(observation)
                
                if not defence_flag:
                    defence_action, defence_prob, defence_val = defence.choose_action(torch.cat(observation,Tokenize(corpus_data.content_rule_list[prosecutor_action]),dim=0))
                # conditioning defence on n-1th observation and the argument by prosecutor 
                observation, prosecutor_reward, defence_reward, prosecutor_done, defence_done, done = env.step(observation[:384],prosecutor_action, defence_action)

                #n_steps += 1
                #score += prosecutor_reward + defence_reward

                if not prosecutor_flag:
                    n_steps_prosecutor += 1
                    score += prosecutor_reward
                    prosecutor.remember(observation, prosecutor_action, prosecutor_prob, prosecutor_val, prosecutor_reward, prosecutor_done)
                
                if prosecutor_done:
                    prosecutor_flag= True
                
                if not defence_flag:
                    n_steps_defence += 1
                    score += defence_reward
                    defence.remember(observation, defence_action, defence_prob, defence_val, defence_reward, defence_done)
                
                if defence_done:
                    defence_flag= True
                
                if n_steps_prosecutor % N == 0:
                    prosecutor.learn()
                    #defence.learn()
                    learn_iters += 1

                if n_steps_defence % N == 0:
                    defence.learn()
                    #defence.learn()
                    learn_iters += 1
                
                if prosecutor_flag and defence_flag:
                    print(score)
                    with open('score3.txt', "a") as file:
                        file.write(str(score)+'\n')
                    break

                #observation = observation_
            score_history.append(score)
            avg_score = np.mean(score_history[-100:])

            n_episodes += 1

            #if avg_score >= best_score:
                #best_score = avg_score
            prosecutor.learn()
            defence.learn()
            
            prosecutor.save_models()
            defence.save_models()

            #print('episode', i, 'score %.1f' % score, 'avg score %.1f' % avg_score, 'time_steps', n_steps, 'learning_steps', learn_iters)
            pass

        except KeyboardInterrupt:
            # Save n_episodes value 
            with open(file_path, "w") as file:
                file.write(str(n_episodes))
            
            x = [i+1 for i in range(len(score_history))]
            plot_learning_curve(x, score_history, figure_file)

            break