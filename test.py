
from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Ball, Box, Door, Key
from minigrid.minigrid_env import MiniGridEnv
from minigrid.envs import playground
import trainingset_generation
import numpy as np
import os

#env._gen_grid()
trial_list = []
BASE_PATH = 'D:\GitHub\minigrid_transformer\data'
for trial in range(1024):
    env = trainingset_generation.Frame()
    x,y = env.render_frame_series()
    trial_list.append((x,y))
np.save(os.path.join(BASE_PATH, 'training_set.npy'),trial_list, allow_pickle=True)
# arr = np.load(os.path.join(BASE_PATH, 'training_set.npy'), allow_pickle=True)
