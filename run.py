import numpy as np
from mcts.nodes import *
from mcts.search import MonteCarloTreeSearch
from tictactoe import TicTacToeGameState

count_win = 0
count_tie = 0

def init():
    state = np.zeros((3, 3))
    initial_board_state = TicTacToeGameState(state=state, next_to_move=1)
    root = MonteCarloTreeSearchNode(state=initial_board_state, parent=None)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(1000)
    c_state = best_node.state
    c_board = c_state.board
    return c_state,c_board


def graphics(board):
    for i in range(3):
        print("")
        print("{0:3}".format(i).center(8)+"|", end='')
        for j in range(3):
            if c_board[i][j] == 0:
                print('_'.center(8), end='')
            if c_board[i][j] == 1:
                print('X'.center(8), end='')
            if c_board[i][j] == -1:
                print('O'.center(8), end='')
    print("")
    print("______________________________")


def get_action(state):
    try:
        location = input("Your move: ")
        if isinstance(location, str):
            location = [int(n, 10) for n in location.split(",")]#将n转化为10进制整数
        if len(location) != 2:
            return 
        x = location[0]
        y = location[1]
        move = TicTacToeMove(x, y, -1)#-1表示为玩家的输入
    except Exception as e:
        move = -1
    if move == -1 or not state.is_move_legal(move):
        print("invalid move,please input again!")
        move = get_action(state)
    return move

def random_action(state):
    random_array = np.random.randint(0,3,size = 2)
    x = random_array[0]
    y = random_array[1]
    print(x,y)
    move = TicTacToeMove(x,y,-1)
    while not state.is_move_legal(move):
        random_array = np.random.randint(0,3,size = 2)
        x = random_array[0]
        y = random_array[1]
        move = TicTacToeMove(x,y,-1)
    print(f"random input:({x},{y})")
    return move

def judge(state):
    if state.is_game_over():
        if state.game_result == 1.0:
            print("You lose!")
        if state.game_result == 0.0:
            print("Tie!")
        if state.game_result == -1.0:
            print("You Win!")
        return 1
    else:
        return -1
    
def judge_random(state):
    global count_tie
    global count_win
    if state.is_game_over():
        if state.game_result == 1.0:
            print("You lose!")
        if state.game_result == 0.0:
            print("Tie!")
            count_tie+=1
            print(count_tie)

        if state.game_result == -1.0:
            print("You Win!")
            count_win+=1
        return 1
    else:
        return -1
c_state,c_board=init()
#初始化棋盘，c_board为二维数组，值为-1，0，1分别代表玩家，空和ai

graphics(c_board)

actor = "random"
n = 10   # 随机和mcts下棋次数
best_action_n = 5  #mcst模拟轮数
if actor == "random":
    for i in range(n+1):
        while True:
            move1 = random_action(c_state)
            c_state = c_state.move(move1)
            c_board = c_state.board
            graphics(c_board)

            if judge_random(c_state)==1:#随机情况下需要多判断一次，对随机的行为判断是否获胜判断玩家是否获胜
                break
            
            #MCTS搜索下一步的落子
            board_state = TicTacToeGameState(state=c_board, next_to_move=1)
            root = MonteCarloTreeSearchNode(state=board_state, parent=None)
            mcts = MonteCarloTreeSearch(root)
            best_node = mcts.best_action(best_action_n)
            c_state = best_node.state
            c_board = c_state.board
            graphics(c_board)
            if judge_random(c_state)==1:
                break
            elif judge_random(c_state)==-1:
                continue
        c_state,c_board=init()
        #初始化棋盘，c_board为二维数组，值为-1，0，1分别代表玩家，空和ai
        graphics(c_board)
    print("best_action_epoch:",best_action_n,"simulate_count",n,"win ratio:",float(count_win)/n,"tie ratio:",float(count_tie)/n)
else :
    while True:
        move1 = get_action(c_state)
        c_state = c_state.move(move1)
        c_board = c_state.board
        graphics(c_board)
        if judge(c_state)==1:#判断玩家是否获胜
            break
        #MCTS搜索下一步的落子
        board_state = TicTacToeGameState(state=c_board, next_to_move=1)
        root = MonteCarloTreeSearchNode(state=board_state, parent=None)
        mcts = MonteCarloTreeSearch(root)
        best_node = mcts.best_action(1000)
        c_state = best_node.state
        c_board = c_state.board
        graphics(c_board)

        if judge(c_state)==1:
            break
        elif judge(c_state)==-1:
            continue

# while True:

#     if actor == "player":
#         move1 = get_action(c_state)
#     else :
#         move1 = random_action(c_state)
#     c_state = c_state.move(move1)
#     c_board = c_state.board
#     graphics(c_board)

#     if judge(c_state)==1:#判断玩家是否获胜
#         break
    
#     #MCTS搜索下一步的落子
#     board_state = TicTacToeGameState(state=c_board, next_to_move=1)
#     root = MonteCarloTreeSearchNode(state=board_state, parent=None)
#     mcts = MonteCarloTreeSearch(root)
#     best_node = mcts.best_action(100)
#     c_state = best_node.state
#     c_board = c_state.board
#     graphics(c_board)

#     if judge(c_state)==1:
#         break
#     elif judge(c_state)==-1:
#         continue

