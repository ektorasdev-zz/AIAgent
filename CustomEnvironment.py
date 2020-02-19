import gym
from gym import spaces
import numpy as np
import random

DP_RANGE = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        # Define action and observation space
        # They must be gym.spaces objects

        self.df = df
        self.total_steps = len(self.df) - 1
        self.current_step = 0
        self.obs = 0
        self.current_dp = 0

        # Actions of the format Increase DP x%, Decrease DP x%, Do Nothing.
        self.action_space = spaces.Discrete(3)

        # Observation space
        self.observation_space = spaces.Box(low=np.array(-len(df)), high=np.array(len(df)), dtype=np.float32)

    def step(self, action):
        # Execute one time step within the environment
        # self._take_action(action)
        assert self.action_space.contains(action)
        self.current_step += 1
        self.current_dp = self.df.loc[self.current_step, "DP"]

        if action == 1:
            # Increase DP %
            self.obs = 1
            if self.df.loc[self.current_step, 'NA%'] < 2.0:
                self.df.loc[self.current_step, "Amount"] = 0
                reward = 0
            elif self.df.loc[self.current_step, 'NA%'] > 8.0:
                self.df.loc[self.current_step, "Amount"] = self.current_dp + random.choice(DP_RANGE)
                reward = 1
            else:
                # Keep DP %
                self.df.loc[self.current_step, "Amount"] = self.current_dp
                self.obs = 3
                reward = self.current_dp ** 4
        elif action == 2:
            # Decrease DP %
            self.obs = 2
            if self.df.loc[self.current_step, 'NA%'] < 2.0:
                random_dp = random.choice(DP_RANGE)
                if self.current_dp - random_dp <= 0:
                    self.df.loc[self.current_step, "Amount"] = 0
                else:
                    self.df.loc[self.current_step, "Amount"] = self.current_dp - random_dp
                reward = 1
            elif self.df.loc[self.current_step, 'NA%'] > 8.0:
                self.df.loc[self.current_step, "Amount"] = self.current_dp + random.choice(DP_RANGE)
                reward = 0
            else:
                # Keep DP %
                self.df.loc[self.current_step, "Amount"] = self.current_dp
                self.obs = 3
                reward = self.current_dp ** 4
        else:
            # Keep DP %
            self.obs = 3
            if self.df.loc[self.current_step, 'NA%'] < 2.0:
                random_dp = random.choice(DP_RANGE)
                if self.current_dp - random_dp <= 0:
                    self.df.loc[self.current_step, "Amount"] = 0
                else:
                    self.df.loc[self.current_step, "Amount"] = self.current_dp - random_dp
                self.obs = 2
                reward = 0
            elif self.df.loc[self.current_step, 'NA%'] > 8.0:
                self.df.loc[self.current_step, "Amount"] = self.current_dp + random.choice(DP_RANGE)
                self.obs = 1
                reward = 0
            else:
                # Keep DP %
                self.df.loc[self.current_step, "Amount"] = self.current_dp
                reward = self.current_dp ** 4

        done = self.current_step >= self.total_steps

        return self.obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.df.loc[self.current_step, "Amount"] = 0
        self.total_steps = len(self.df) - 1
        self.obs = 0

        # Set the current step to a random point within the data frame
        self.current_step = 0

        return self.obs

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        pass
        # print(f'Step: {self.current_step}')
        # print(f'New DP: {self.df.loc[self.current_step, "Amount"]}')
