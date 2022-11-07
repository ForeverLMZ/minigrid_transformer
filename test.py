
from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Ball, Box, Door, Key
from minigrid.minigrid_env import MiniGridEnv
from minigrid.envs import playground
import trainingset_generation

from minigrid.utils import window
window = window.Window('whateevr')
env = trainingset_generation.Frame()
img = env.render_frame_series()
