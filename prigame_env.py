import gym
from gym import spaces
import numpy as np
import random

class PRIGameEnv(gym.Env):
    def __init__(self):
        super(PRIGameEnv, self).__init__()
        self.observation_space = spaces.Box(low=np.array([0, 1, -10]), 
                                            high=np.array([1, 10, 10]), 
                                            dtype=np.float32)
        self.action_space = spaces.Discrete(3)  # 0: 유지, 1: 증가, 2: 감소
        self.correct_rate = 0.5 #50%
        self.avg_response_time = 5.0 #평균 반응시간
        self.streak_count = 0 #연속 몇개맞췄는지
        self.current_difficulty = 1

    def reset(self):
        self.correct_rate = 0.5
        self.avg_response_time = 5.0
        self.streak_count = 0
        self.current_difficulty = 1
        return np.array([self.correct_rate, self.avg_response_time, self.streak_count])

    def step(self, action):
        if action == 1:
            self.current_difficulty = min(5, self.current_difficulty + 1)
        elif action == 2:
            self.current_difficulty = max(1, self.current_difficulty - 1)

        success = random.random() < (0.5 + 0.1 * (5 - self.current_difficulty))
        response_time = random.uniform(3, 7) if success else random.uniform(7, 10)

        self.correct_rate = max(0, min(1, (self.correct_rate * 0.8 + (1 if success else 0) * 0.2)))
        self.avg_response_time = max(1, min(10, (self.avg_response_time * 0.8 + response_time * 0.2)))
        self.streak_count = self.streak_count + 1 if success else self.streak_count - 1
        self.streak_count = max(-10, min(10, self.streak_count))

        reward = 0
        if 0.7 <= self.correct_rate <= 0.9:
            reward += 1
        if 4 <= self.avg_response_time <= 6:
            reward += 1
        if success:
            reward += 0.5
        if self.streak_count > 3:
            reward += 1
        elif self.streak_count < -3:
            reward -= 1

        done = False
        return np.array([self.correct_rate, self.avg_response_time, self.streak_count]), reward, done, {}
