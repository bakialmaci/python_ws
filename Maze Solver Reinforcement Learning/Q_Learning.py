import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import inf
from copy import deepcopy

# (for visualisation) rounds number to four digits
def round_to_4(i):
    return round(i, 3) if abs(i) < 1 else round(i, 4-int(np.floor(np.log10(abs(i)))+1))

# expand (Q or R) agent-matrix by adding a new state
def Mat_expand(m,var): 
    m = np.vstack([m,[var]*len(m)]) 
    m = np.column_stack([m,[var]*len(m)])
    return m

#initialize static animation: maze walls + goal
def init():
    for i in range(Size+1): # maze outer walls
        plt.plot([0,Size],[i,i],'b:', lw = .5)
        plt.plot([i,i],[0,Size], 'b:', lw = .5)
    plt.plot([0,Size,Size,0,0],[Size,Size,0,0,Size], 'b', lw = 2) 
    for i in range(Size-1): # maze inner walls
        for j in range(Size):
            if Wall_hor[i][j] == 0:
                plt.plot([j,j+1],[i+1,i+1], 'b', lw = 2)
    for i in range(Size):
        for j in range(Size-1):
            if Wall_ver[i][j] == 0:
                plt.plot([j+1,j+1],[i,i+1], 'b', lw = 2)
    plt.plot([Goal_xy[0]+.5],[Goal_xy[1]+.5], 'r*', ms = 15) # goal
    plt.text(0,Size+0.2,'Episode', fontsize = 9) # episode_text
    return [ag] + q_up + q_down + q_left + q_right + [ep]

#update dynamic animation: ag - agent, q_ - q-values, ep - episode
def update(frame):
    k = 0
    for i in range(Size):
        for j in range(Size):
            q_up[k].set_text(frame[1]['up'][i][j])
            q_down[k].set_text(frame[1]['down'][i][j])
            q_left[k].set_text(frame[1]['left'][i][j])
            q_right[k].set_text(frame[1]['right'][i][j])
            k += 1
    ep.set_text(frame[2])
    ag.set_data(frame[0][0]+.5, frame[0][1]+.5)
    return [ag] + q_up + q_down + q_left + q_right + [ep]  

# ----------------------------constants/variables--------------------------   
# Learning constants
gamma = 0.8 # discout rate
alpha = 0.2 # learning rate
epsilon = 0.1 #random direction chance (greedy)

# Reward constants
R_const_goal = 100
R_const_wall = -10
R_const_step = -0.05

# general constants
Size = 5 # maze size
Size_text = 7 # (for vizualisation) adjust text size to avoid overlap 
delay = 10 #between steps in ms
max_episodes = 100 #number of episodes

# maze generation
random.seed(10) # to change the maze    
Wall_hor = [[random.choice([0,1,1]) for i in range(Size)] for j in range(Size-1)] # randomize maze walls
Wall_ver = [[random.choice([0,1,1]) for i in range(Size-1)] for j in range(Size)] # randomize maze walls
#dictionary of 2D maze-matrices of (1=allowed, 0=not allowed) moves 
Moves = {'up':Wall_hor + [[0]*Size],'down':[[0]*Size] + Wall_hor, 
         'left':[[0] + Wall_ver[i] for i in range(Size)],
         'right':[Wall_ver[i] + [0] for i in range(Size)]}

# Variables in the xy-coordinates of the maze
Agent_start_xy = [0,2] # starting position of the agent (min = 0, max = Size-1)
Goal_xy = [Size-1,Size-1] # position of the goal (min = 0, max = Size-1)

State_xy = np.ones((Size,Size))*[-inf] # Number of the state as discovered
State_xy[tuple(Agent_start_xy)] = 1 # The first state
Visited_xy = [Agent_start_xy] # Visited cells of the maze

Reward_xy = np.ones((Size,Size))*(R_const_step) # maze-defined matrix of the rewards: step penalty
Reward_xy[tuple(Goal_xy)] += R_const_goal # maze-defined matrix of the rewards: goal reward

Q_xy = {i:np.zeros((Size,Size)) for i in ['up', 'down', 'left', 'right']} # maze-defined matrix of Q

Plot_update = [[Agent_start_xy, Q_xy, 1]] #  List with exploration data for the animation

# Variables in the agent-coordinates
R = np.array([-inf]) # reward matrix
Q = np.array([0], dtype=np.float32) # q-matrix
R = Mat_expand(R,-inf) # expand R-matrix
Q = Mat_expand(Q,0) # expand Q-matrix

Move_dict = {'up':[0,1],'down':[0,-1],'left':[-1,0],'right':[1,0]} # 0-Up,1-Down,2-Left,3-Right

# ----------------------------maze exploration--------------------------   
for episode in range(max_episodes):
    s = 1 # current state
    Agent_xy = Agent_start_xy
    while Agent_xy != Goal_xy:
        
        if random.random() < epsilon: #randomize the direction
            
            direction = np.random.choice(['up','down','left','right'])
            
        else:
            
            d = {i:Q_xy[i][tuple(Agent_xy)] for i in ['up','down','left','right']}
            direction = max(d, key=d.get)
            
        Agent_xy_new = [i+j for i,j in zip(Agent_xy,Move_dict[direction])] # new agent coordinates
        
        if Moves[direction][Agent_xy[1]][Agent_xy[0]] == 1: # move is allowed

            if Agent_xy_new not in Visited_xy: # not visited cell before (in any episodes)
                R = Mat_expand(R,-inf) # expand R-matrix
                Q = Mat_expand(Q,0) # expand Q-matrix
                Visited_xy += [Agent_xy_new] # mark as visited
                State_xy[tuple(Agent_xy_new)] = np.max(State_xy) + 1  # assigne new state to new xy position                
            
            # Update Q-agent
            s_new = int(State_xy[tuple(Agent_xy_new)])
            R[s,s_new] = Reward_xy[tuple(Agent_xy_new)]
            q_max = max(filter(lambda x: x != 0, Q[s_new])) if sum(Q[s_new]) != 0 else 0 # calculate q_max
            Q[s,s_new] += alpha*(R[s,s_new] + gamma*q_max - Q[s,s_new]) # MAIN learning equation
            
        else:  # move is not allowed
            
            Agent_xy_new = Agent_xy
            s_new = 0
            R[s,s_new] = R_const_wall #hit the wall
            Q[s,s_new] += alpha*(R[s,s_new] - Q[s,s_new]) ######################### GENERALIZE!!!!!
        
        # replace q-value in q-vizualisation matrix
        Q_xy[direction][tuple(Agent_xy)] = round_to_4(Q[s,s_new])
        
        # Update plot
        Plot_update.append([])
        Plot_update[-1].append(Agent_xy_new) # update agent coordinates
        Plot_update[-1].append(deepcopy(Q_xy)) # update q-visualization matrix
        Plot_update[-1].append(episode+1) # update episode-visualization
        
        # Update variables
        Agent_xy = Agent_xy_new # update for next iteration
        if s_new != 0: s = s_new # update for next iteration

# ----------------------------animation--------------------------        
fig, ax = plt.subplots()
ax = plt.axes(xlim=(-.2, Size+.2), ylim=(-.2, Size+.2)) # Axes limit
plt.axis('off') # Remove all axes
plt.rc('font', size=Size_text) # Change text font

ag, = plt.plot([Agent_start_xy[0]+.5],[Agent_start_xy[1]+.5], 'yo', ms = 8, animated=True) # agent
q_up = [ax.annotate('',xy=(i+.4, j+.83)) for i in range(Size) for j in range(Size)] # q-values
q_down = [ax.annotate('',xy=(i+.4, j+.05)) for i in range(Size) for j in range(Size)]
q_left = [ax.annotate('',xy=(i+.03, j+.45)) for i in range(Size) for j in range(Size)]
q_right = [ax.annotate('',xy=(i+.67, j+.45)) for i in range(Size) for j in range(Size)]
ep = ax.annotate('',xy=(0,Size+.05)) # episode

ani = FuncAnimation(fig, update, frames = Plot_update, 
                    init_func=init, interval = delay, blit=True)

plt.show()