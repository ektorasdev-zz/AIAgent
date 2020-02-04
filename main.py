import datetime as dt
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
import pandas as pd
from CustomEnvironment import CustomEnv

df = pd.read_csv('Sheet12.csv')
df = pd.DataFrame(df, columns=['City Name', 'Service type', 'Stage', 'Action', 'Day', 'From Time',
                               'To Time', 'Amount', 'Passenger Location', 'Route Metric',
                               'Month, Day, Year of Request Created Local', 'DP', 'Requests',
                               'NA%', 'Non Riders'])
df = df.sort_values('Month, Day, Year of Request Created Local')

# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: CustomEnv(df)])
model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=20000)
obs = env.reset()

for i in range(2000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
