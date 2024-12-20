import numpy as np
import random

class QLearningAgent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.995, exploration_rate=0.999, exploration_decay=0.999):
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = {}

    def choose_action(self, state):
        state_key = tuple(state.flatten())
        if random.random() < self.exploration_rate:
            return random.choice(self.actions)
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def learn(self, state, action, reward, next_state):
        state_key = tuple(state.flatten())
        next_state_key = tuple(next_state.flatten())

        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {action: 0.0 for action in self.actions}

        old_value = self.q_table[state_key][action]
        next_max = max(self.q_table[next_state_key].values())
        self.q_table[state_key][action] = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)

        self.exploration_rate = max(0.01, self.exploration_rate * self.exploration_decay)