import gym
from gym import spaces
import numpy as np
import random

DP_RANGE = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(CustomEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects

        self.df = df
        self.reward_range = (0, 10000)

        # Actions of the format Increase DP x%, Decrease DP x%, Do Nothing, etc.
        self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

        # Prices contains the OHCL values for the last five prices
        self.observation_space = spaces.Box(low=0, high=1, shape=(720, ), dtype=np.float16)

    def _next_observation(self):
        print('mpike 3')
        # Get Requests, NA, DP for the last 5 days
        frame = np.array([
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] != 'January 20, 2020', 'NA%'].values,
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] != 'January 20, 2020', 'DP'].values,
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] != 'January 20, 2020', 'Requests'].values,
        ])

        # Get current Requests, NA, DP
        obs = np.append(frame, [[
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] == 'January 20, 2020', 'NA%'].values,
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] == 'January 20, 2020', 'DP'].values,
            self.df.loc[self.df['Month, Day, Year of Request Created Local'] == 'January 20, 2020', 'Requests'].values,
        ]])

        return obs

    def _take_action(self, action):
        print('mpike 4')
        # Set the current price to a random price within the time step
        self.current_dp = random.uniform(self.df.loc[self.current_step, "Requests"], self.df.loc[self.current_step, "NA%"])

        action_type = action[0]
        amount = action[1]

        print('Action type: ', action_type)
        print('Amount: ', amount)

        if action_type < 1:
            # Buy amount % of balance in shares
            self.new_dp = self.current_dp + 25

        elif action_type < 2:
            # Sell amount % of shares held
            if self.current_dp <= 0:
                self.new_dp = 0
            else:
                self.new_dp = self.current_dp - 25

    def step(self, action):
        print('mpike 5')
        # Execute one time step within the environment
        self._take_action(action)
        self.current_step += 1
        if self.current_step > len(self.df.loc[:, 'Requests'].values) - 6:
            self.current_step = 0
        delay_modifier = (self.current_step / 10000)

        reward = self.balance * delay_modifier
        done = self.net_worth <= 0
        obs = self._next_observation()
        print('Observation: ', obs)
        return obs, reward, done, {}

    def reset(self):
        print('mpike 6')
        # Reset the state of the environment to an initial state
        self.new_dp = 0

        # Set the current step to a random point within the data frame
        self.current_step = random.randint(0, len(self.df.loc[:, 'Requests'].values) - 6)

        return self._next_observation()

    def render(self, mode='human', close=False):
        # Render the environment to the screen

        print(f'Step: {self.current_step}')
        print(f'Balance: {self.new_dp}')




