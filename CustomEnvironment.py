import gym
from gym import spaces
import numpy as np
import random

DP_RANGE = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
SCALE_AMOUNT = 100000


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(CustomEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects

        self.df = df
        self.reward_range = (0, 10000)
        self.total_steps = len(df) - 1
        self.current_step = random.randint(0, len(self.df.loc[:, 'NA%'].values) - 6)

        # Actions of the format Increase DP x%, Decrease DP x%, Do Nothing, etc.
        self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

        # Prices contains the OHCL values for the last five prices
        self.observation_space = spaces.Box(low=0, high=1, shape=(720, ), dtype=np.float16)

    def _next_observation(self):
        # Get Requests, NA, DP for the last 5 days
        frame = np.array([
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] != 'January 20, 2020', 'NA%'].values
            / SCALE_AMOUNT,
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] != 'January 20, 2020', 'DP'].values
            / SCALE_AMOUNT,
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] != 'January 20, 2020', 'Requests'].values
            / SCALE_AMOUNT,
        ])

        # Get current Requests, NA, DP
        obs = np.append(frame, [[
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] == 'January 20, 2020', 'NA%'].values
            / SCALE_AMOUNT,
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] == 'January 20, 2020', 'DP'].values
            / SCALE_AMOUNT,
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] == 'January 20, 2020', 'Requests'].values
            / SCALE_AMOUNT,
        ]])

        return obs

    def _take_action(self, action):
        # Set the current price to a random price within the time step
        self.current_dp = random.uniform(self.df.loc[self.current_step, "DP"], self.df.loc[self.current_step, "DP"])

        action_type = action[0]
        amount = action[1]

        if action_type < 1:
            # Decrease or Hold DP Percentage
            if self.current_dp - random.choice(DP_RANGE) <= 0:
                self.df.loc[self.current_step, "Amount"] = 0
            else:
                self.df.loc[self.current_step, "Amount"] = self.current_dp - random.choice(DP_RANGE)

        elif action_type < 2:
            # Increase DP %
            self.df.loc[self.current_step, "Amount"] = self.current_dp + random.choice(DP_RANGE)

    def step(self, action):
        # Execute one time step within the environment
        self._take_action(action)
        self.current_step += 1

        if 2.0 < float(self.df.loc[self.current_step, 'NA%']) < 8.0:
            reward = 1
        else:
            reward = 0

        done = self.total_steps <= 0
        obs = self._next_observation()
        self.total_steps -= self.current_step
        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.df.loc[self.current_step, "Amount"] = 0
        self.total_steps = self.df.shape[0]

        # Set the current step to a random point within the data frame
        self.current_step = random.randint(0, len(self.df.loc[:, 'NA%'].values) - 6)

        return self._next_observation()

    def render(self, mode='human', close=False):
        # Render the environment to the screen

        print(f'Step: {self.current_step}')
        print(f'New DP: {self.df.loc[self.current_step, "Amount"]}')




