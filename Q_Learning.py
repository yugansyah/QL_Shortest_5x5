import random

alpha = 0.5
gamma = 0.9
Q_table = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

for i in range(24):
    for j in range(4):   
       Q_table[i][j] = random.random()


def print_Qtable(Q_table):
    print("\nState\t\tRight\t\t\tUp\t\t\tLeft\t\t\tDown")
    print("-----\t\t-----\t\t\t-----\t\t\t-----\t\t\t-----")

    for s in range(24):
        if(Q_table[s][0] >= 90):
            print(s+1, "\t", Q_table[s][0], "\t\t\t", Q_table[s][1], "\t", Q_table[s][2], "\t", Q_table[s][3])
        else:
            print(s+1, "\t", Q_table[s][0], "\t", Q_table[s][1], "\t", Q_table[s][2], "\t", Q_table[s][3])
    s += 1

    print(s+1, "\t", Q_table[s][0], "\t\t\t", Q_table[s][1], "\t\t\t", Q_table[s][2], "\t\t\t", Q_table[s][3], "\n")

def Search_Location(maze):
    for i in range(5):
        for j in range(5):
            if maze[i][j] == 1:
                return (5 * (i) + j + 1), i + 1, j + 1

def Action(mazes, Q_tables, epsilons):
    out = 0

    while out == 0:
        state, state_i, state_j = Search_Location(mazes)

        rdm = random.random()

        if epsilons <= rdm:
            max_value = max(Q_tables[state-1][0], Q_tables[state-1][1], Q_table[state-1][2], Q_table[state-1][3])
            
            for j in range(4):
                if max_value == Q_tables[state-1][j]:
                    act = j+1
        
        else:
            random_value = random.random()

            if random_value <= 0.25:
                act = 1
            elif random_value <= 0.5:
                act = 2
            elif random_value <= 0.25:
                act = 3
            else:
                act = 4

        if act == 1:
            state_j += 1
        elif act == 2:
            state_i -= 1 
        elif act == 3:
            state_j -= 1 
        else:
            state_i += 1

        if state_i == 0:
            out = 0 
        elif state_j == 0:
            out = 0
        elif state_i == 6:
            out = 0
        elif state_j == 6:
            out = 0
        else:
            out = out + 1

    new_mazes = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    new_mazes[state_i - 1][state_j - 1] = 1
    return act, new_mazes

def Routing(Q_table):
    print("Route")
    s = 1

    for i in range(1,26):
        if s==5 or s==7 or s==8 or s==14 or s==17 or s==19 or s==20 or s==22:
            print("error")
            break

        if s == 25:
            print("S", s, "Goal!")
            break
       
        print("S", s, end=" ")

        M = max(Q_table[s-1][0], Q_table[s-1][1], Q_table[s-1][2], Q_table[s-1][3])
        I = 0
        while Q_table[s-1][I] != M:
            I += 1
        I += 1

        if I == 1:
            if s%5 != 0:
                s = s+1
            else:
                print("error")
                break
        elif I == 2:
            if s > 5:
                s = s-5
            else:
                print("error")
                break
        elif I == 3:
            if s%5 != 1:
                s = s-1
            else:
                print("error")
                break
        elif I == 4:
            if s < 21:
                s = s+5
            else:
                print("error")
                break
    if i == 25:
        print("error")

def update_Qvalue(states, new_states, Q_tabless, acts, alphas, gammas, t):
    if new_states == 25:
        reward = 100
    elif t == 15:     
        reward = -50 
    elif new_states == 5:
        reward = -100 
    elif new_states == 7:
        reward = -100 
    elif new_states == 8:
        reward = -100 
    elif new_states == 14:
        reward = -100 
    elif new_states == 17:
        reward = -100 
    elif new_states == 19:
        reward = -100 
    elif new_states == 20:
        reward = -100 
    elif new_states == 22:
        reward = -100 
    else:
        reward = 0 
    
    Q_tabless[states - 1][acts - 1] = (1 - alphas) * Q_tabless[states - 1][acts - 1] + alphas * (reward + gammas * max(Q_tabless[new_states - 1][0], Q_tabless[new_states - 1][1], Q_tabless[new_states - 1][2], Q_tabless[new_states - 1][3]))
    
    return Q_tabless, new_states

print("\nQ-Table and route before learning")
print_Qtable(Q_table)
Routing(Q_table)

for Episode in range(1, 301):
    maze = [[1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    epsilon = 1 - (Episode / 301)

    for i in range(1, 16):
        state, state_i, state_j = Search_Location(maze)
        
        if state == 25:
            break
        
        actss, new_maze = Action(maze, Q_table, epsilon)

        new_state, new_state_i, new_state_j = Search_Location(new_maze)
        
        Q_table, new_state = update_Qvalue(state, new_state, Q_table, actss, alpha, gamma, i)

        maze = new_maze

print("\nQ-Table and route after learning")
print_Qtable(Q_table)
Routing(Q_table)


