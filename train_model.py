from stable_baselines3 import DQN
from prigame_env import PRIGameEnv

# PRIGame 환경 생성
env = PRIGameEnv()

# DQN 모델 생성
model = DQN("MlpPolicy", env, verbose=1, learning_rate=1e-3, buffer_size=10000)

# 모델 학습
print("Starting Training...")
model.learn(total_timesteps=50000)
print("Training Finished!")

# 모델 저장
model.save("prigame_dqn_model")
