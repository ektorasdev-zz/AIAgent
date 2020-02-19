from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
import pandas as pd
from CustomEnvironment import CustomEnv
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

df = pd.read_csv('Sheet12.csv')
data = pd.DataFrame(df, columns=['City Name', 'Service type', 'Stage', 'Action', 'Day', 'From Time',
                                 'To Time', 'Amount', 'Passenger Location', 'Route Metric',
                                 'Month, Day, Year of Request Created Local', 'DP', 'Requests',
                                 'NA%', 'Non Riders'])
data = data.sort_values('Month, Day, Year of Request Created Local')

# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: CustomEnv(data)])
model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=20000)
obs = env.reset()

for i in range(2000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()

data.to_csv('New_file.csv', index=False)








