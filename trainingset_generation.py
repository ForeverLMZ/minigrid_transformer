from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Ball, Box, Door, Key
from minigrid.minigrid_env import MiniGridEnv
from minigrid.utils import rendering
from minigrid.core.constants import OBJECT_TO_IDX, TILE_PIXELS
from minigrid.core.world_object import Wall, WorldObj
import numpy as np


class Task(MiniGridEnv):
    """
    Environment with multiple rooms and random objects.
    This environment has no specific goals or rewards.
    """

    def __init__(self, max_steps=100, **kwargs):
        mission_space = MissionSpace(mission_func=self._gen_mission)
        super().__init__(
            mission_space=mission_space,
            width=4,
            height=4,
            max_steps=max_steps,
            render_mode = "rgb_array",
            **kwargs
        )

    @staticmethod
    def _gen_mission():
        return ""

    def _gen_grid(self, width = 4, height = 4):
        # Create the grid
        self.grid = Grid(width, height)

        # # Place random objects in the world
        # types = ["key", "ball", "box"]
        # for i in range(0, 12):
        #     objType = self._rand_elem(types)
        #     objColor = self._rand_elem(COLOR_NAMES)
        #     if objType == "key":
        #         obj = Key(objColor)
        #     elif objType == "ball":
        #         obj = Ball(objColor)
        #     elif objType == "box":
        #         obj = Box(objColor)
        #     else:
        #         raise ValueError(
        #             "{} object type given. Object type can only be of values key, ball and box.".format(
        #                 objType
        #             )
        #         )
        #     self.place_obj(obj)

        # No explicit mission in this environment
        self.mission = ""

    def render(self, tile_size = 60, objects = None) -> np.ndarray:
        """
        Render this grid at a given scale
        :param r: target renderer object
        :param tile_size: tile size in pixels
        :param objects: potential shapes to put into grid
        """

        # Compute the total grid size
        width_px = self.width * tile_size
        height_px = self.height * tile_size

        img = np.zeros(shape=(height_px, width_px, 3), dtype=np.uint8)
        img = rendering.fill_coords(img, rendering.point_in_rect(0, width_px, 0,height_px), (255, 255, 255))

        # Render the grid
        subdivs = 3
        for j in range(0, self.height):
            for i in range(0, self.width):
                cell = self.grid.get(i, j)
                tile_img = np.zeros(shape=(tile_size * subdivs, tile_size * subdivs, 3), dtype=np.uint8)
                rendering.fill_coords(tile_img, rendering.point_in_rect(0, width_px, 0,height_px), (255, 255, 255))

                # Draw the grid lines (top and left edges)
                rendering.fill_coords(tile_img, rendering.point_in_rect(0, 0.031, 0, 1), (100, 100, 100))
                rendering.fill_coords(tile_img, rendering.point_in_rect(0, 1, 0, 0.031), (100, 100, 100))
                tile_img = rendering.downsample(tile_img, 3)
                ymin = j * tile_size
                ymax = (j + 1) * tile_size
                xmin = i * tile_size
                xmax = (i + 1) * tile_size
                img[ymin:ymax, xmin:xmax, :] = tile_img
                

        return img

    def render_tile(
        cls,
        obj = None,
        highlight: bool = False,
        tile_size: int = TILE_PIXELS,
        subdivs: int = 3,
    ) -> np.ndarray:
        """
        Render a tile and cache the result
        """

        img = np.zeros(
            shape=(tile_size * subdivs, tile_size * subdivs, 3), dtype=np.uint8
        )

        # Draw the grid lines (top and left edges)
        rendering.fill_coords(img, rendering.point_in_rect(0, 0.031, 0, 1), (100, 100, 100))
        rendering.fill_coords(img, rendering.point_in_rect(0, 1, 0, 0.031), (100, 100, 100))

        if obj is not None:
            obj.render(img)


        # Downsample the image to perform supersampling/anti-aliasing
        img = rendering.downsample(img, subdivs)

        return img
