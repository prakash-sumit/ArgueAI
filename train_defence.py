import gym
import numpy as np
from Prosecutor_final import Agent as prosecutor_agent
from Defence_final import Agent as defence_agent
from utils import plot_learning_curve
import os

from env_final import *

if __name__ == '__main__':
    #env = gym.make('CartPole-v0')
    env = CourtRoomEnvironment()
    N = 80
    batch_size = 64
    n_epochs = 20
    alpha = 0.0002
    prosecutor = prosecutor_agent(n_actions=len(env.prosecutor_action_space), batch_size=batch_size, 
                    alpha=alpha, n_epochs=n_epochs, 
                    input_dims=384) # s-bert embedding size = 384
    defence = defence_agent(n_actions=len(env.defence_action_space), batch_size=batch_size, 
                    alpha=alpha, n_epochs=n_epochs, 
                    input_dims=384) # s-bert embedding size = 384
    
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
            for j in range(300):
                prosecutor_action, prosecutor_prob, prosecutor_val = prosecutor.choose_action(observation)
                defence_action, defence_prob, defence_val = defence.choose_action(observation)
                
                prosecutor_reward, defence_reward, prosecutor_done, defence_done, done = env.step(prosecutor_action, defence_action)

                n_steps_prosecutor += 1

                #score += prosecutor_reward #+ defence_reward

                prosecutor.remember(observation, prosecutor_action, prosecutor_prob, prosecutor_val, prosecutor_reward, prosecutor_done)
                #defence.remember(observation, defence_action, defence_prob, defence_val, defence_reward, defence_done)

                if n_steps_prosecutor % N == 0:
                    prosecutor.learn()
                    #defence.learn()
                    learn_iters += 1

                if prosecutor_reward >= 10:
                    while True:
                        defence.remember(observation, defence_action, defence_prob, defence_val, defence_reward, defence_done)
                        score += defence_reward
                        n_steps_defence += 1
                        if done:
                            print(score)
                            with open('score2.txt', "a") as file:
                                file.write(str(score)+'\n')
                            break
                        else:
                            defence_action, defence_prob, defence_val = defence.choose_action(observation)
                            prosecutor_reward, defence_reward, prosecutor_done, defence_done, done = env.step(prosecutor_action, defence_action)

                    if n_steps_defence % N == 0:
                        defence.learn()
                
                if done:
                    '''print(score)
                    with open('score2.txt', "a") as file:
                        file.write(str(score)+'\n')'''
                    break

                #observation = observation_
            score_history.append(score)
            avg_score = np.mean(score_history[-100:])

            n_episodes += 1

            #if avg_score >= best_score:
                #best_score = avg_score
            prosecutor.save_models()
            defence.save_models()
            #defence.save_models()

            #print('episode', i, 'score %.1f' % score, 'avg score %.1f' % avg_score, 'time_steps', n_steps, 'learning_steps', learn_iters)
            pass

        except KeyboardInterrupt:
            # Save n_episodes value 
            with open(file_path, "w") as file:
                file.write(str(n_episodes))
            
            x = [i+1 for i in range(len(score_history))]
            plot_learning_curve(x, score_history, figure_file)

            break