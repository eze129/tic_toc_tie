import numpy as np
from collections import defaultdict
from tictactoe import *

class MonteCarloTreeSearchNode(object):
    def __init__(self, state: TicTacToeGameState, parent=None):
        self._number_of_visits = 0.
        self._results = defaultdict(int)#一个字典
        self.state = state
        self.parent = parent
        self.children = []

    @property
    def untried_actions(self):
        if not hasattr(self, '_untried_actions'):
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        #next_to_move为1表示为ai，那么wins为最终result为1的值，当next_to_move=-1，表示这一步为玩家的操作，那么result应该取-1表示ai输
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self.untried_actions.pop()# 列表的末尾返回一个元素
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result

    def backpropagate(self, result):
        self._number_of_visits += 1.#搜索过的节点数
        self._results[result] += 1.#reskut=-1/1/0    记录向下随机选择，赢得可能性
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / (c.n)) + c_param * np.sqrt((2 * np.log(self.n) / (c.n)))
            for c in self.children
        ]

        # choices_weights = [c.q for c in self.children]

        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]
