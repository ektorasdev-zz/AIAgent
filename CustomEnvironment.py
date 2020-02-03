import gym
from gym import spaces
import numpy as np
import random

REQUESTS = 1000000
NA = 300
MAX_SHARE_PRICE = 5000
MAX_OPEN_POSITIONS = 5
MAX_STEPS = 20000

INITIAL_ACCOUNT_BALANCE = 10000


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(CustomEnv, self).__init__()

        # Define action and observation space
        # They must be gym.spaces objects

        self.df = df
        self.reward_range = (0, REQUESTS)

        # Actions of the format Increase DP x%, Decrease DP x%, Do Nothing, etc.
        self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

        # Prices contains the OHCL values for the last five prices
        self.observation_space = spaces.Box(low=0, high=1, shape=(4, 1), dtype=np.float16)

    def _next_observation(self):
        # Get the stock data points for the last 5 days and scale to be between 0-1
        frame = np.array([
            self.df.loc[self.current_step: self.current_step + 1, 'Requests'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 1, 'NA%'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 1, 'Non Riders'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step + 1, 'DP'].values / MAX_SHARE_PRICE,
        ])

        obs = np.append(frame, [[
            self.new_dp / REQUESTS,
        ]])

        return obs

    def _take_action(self, action):
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
        # Execute one time step within the environment
        self._take_action(action)
        self.current_step += 1
        if self.current_step > len(self.df.loc[:, 'Requests'].values) - 6:
            self.current_step = 0
        delay_modifier = (self.current_step / MAX_STEPS)

        reward = self.balance * delay_modifier
        done = self.net_worth <= 0
        obs = self._next_observation()
        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.new_dp = 0

        # Set the current step to a random point within the data frame
        self.current_step = random.randint(0, len(self.df.loc[:, 'Requests'].values) - 6)

        return self._next_observation()

    def render(self, mode='human', close=False):
        # Render the environment to the screen

        print(f'Step: {self.current_step}')
        print(f'Balance: {self.new_dp}')




