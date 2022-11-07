from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Ball, Box, Door, Key
from minigrid.minigrid_env import MiniGridEnv
from minigrid.utils import rendering
from minigrid.core.constants import OBJECT_TO_IDX, TILE_PIXELS
from minigrid.core.world_object import Wall, WorldObj
import numpy as np
import random
import math
from minigrid.utils import window as w
from random import sample as s
import numpy as np

class Frame(MiniGridEnv):
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
        # No explicit mission in this environment
        self.mission = ""


    def render_frame_series(self):#(240,240,3)
        series = []
        cue = self.render_frame(stage = 'cue')
        delay = self.render_frame(stage = 'delay')
        test = self.render_frame(stage = 'test')
        self.delay_fram_number = random.randint(1,5)
        series.append(cue)
        for frame in range(self.delay_fram_number):
            series.append(delay)
        series.append(test)
        series_arr = np.asarray(series)
        print(self.delay_fram_number)
        print(series_arr.shape) #(3, 240, 240, 3)
        # print(cue.shape)
        # window = w.Window('whateevr') 
        # window.show_img(cue)
        # window.show()
        # #window.close()
        # window = w.Window('whateevr')
        # window.show_img(delay)
        # window.show()
        # window.close()
        # window = w.Window('whateevr')
        # window.show_img(test)
        # window.show()
        # window.close()
        

    def render_frame(self, tile_size = 60, objects = None, stage = 'cue') -> np.ndarray:
        """
        Render this grid at a given scale
        :param r: target renderer object
        :param tile_size: tile size in pixels
        :param objects: potential shapes to put into grid
        """
        #print(stage)
        # Compute the total grid size
        width_px = self.width * tile_size
        height_px = self.height * tile_size

        img = np.zeros(shape=(height_px, width_px, 3), dtype=np.uint8)
        img = rendering.fill_coords(img, rendering.point_in_rect(0, width_px, 0,height_px), (255, 255, 255))

        # Render the grid
        subdivs = 3
        if stage == 'cue':
            self.cue_coord = (random.randint(0,3), random.randint(0,3))
            self.false_test_shape, self.cue_shape = s(['square','circle','triangle'], 2)
        elif stage == 'test':   
            self.false_test_coord = (random.randint(0,3), random.randint(0,3))
            # self.false_test_shape = self.random_shape()
            self.true_test_coord = (random.randint(0,3), random.randint(0,3))
            # self.true_test_shape = self.cue_shape
            while (self.false_test_coord == self.true_test_coord): #generates a different coord than the actual coord of the cue
                self.false_coord = (random.randint(0,3), random.randint(0,3))
            # while(self.true_test_shape == self.false_test_shape):
            #     self.false_shape = self.random_shape()

        

        for j in range(0, self.height):
            for i in range(0, self.width):
                #cell = self.grid.get(i, j)
                tile_img = np.zeros(shape=(tile_size * subdivs, tile_size * subdivs, 3), dtype=np.uint8)
                #colors each tile white
                rendering.fill_coords(tile_img, rendering.point_in_rect(0, tile_size, 0, tile_size), (255, 255, 255))
                if stage == 'cue' and self.cue_coord == (i,j):
                    self.render_shape(self.cue_shape, tile_img)
                if stage == 'test':
                    if self.false_test_coord == (i,j):
                        self.render_shape(self.false_test_shape,tile_img)
                    if self.true_test_coord == (i,j):
                        self.render_shape(self.cue_shape,tile_img)
                
                    

                    
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
    
    def random_color(self):
        color_list = [(255,0,0),(255,255,0),(0,255,0),(0,255,255)]
        color_key = random.randint(0,3)
        return color_list[color_key]
    
    def random_shape(self):
        shape_list = ['square','triangle','circle']
        shape_key = random.randint(0,2)
        return shape_list[shape_key]
    
    def render_shape(self,shape,img):
        if shape == 'square':
            width = random.uniform(0.4, 0.8) #assume a reasonable range of width
            xmin = random.uniform(0.05,(1-width-0.07))
            ymin = random.uniform(0.05,(1-width-0.07))
            rendering.fill_coords(img, rendering.point_in_rect(xmin, xmin+width, ymin, ymin+width), self.random_color())
        elif shape == 'triangle': #assume equilateral triangle
            length = random.uniform(0.3, 0.7) #assume a reasonable range of length
            cx = random.uniform(0.07+length/2 , 1-0.07-length/2)
            cy = random.uniform(0.07, 1-0.07-length*(math.cos(math.pi / 6)))
            ax = cx - length/2
            ay = cy + length*(math.cos(math.pi / 6))
            bx = ax+length
            by = ay
            #print((ax,ay),(bx,by),(cx,cy))
            rendering.fill_coords(img, rendering.point_in_triangle((ax,ay),(bx,by),(cx,cy)), self.random_color())
        else: #is a circle
            radius = random.uniform(0.3, 0.7) / 2
            centerx = random.uniform(radius+0.07,(1-radius-0.07))
            centery = random.uniform(radius+0.07,(1-radius-0.07))
            #print(centerx, centery,radius)
            rendering.fill_coords(img, rendering.point_in_circle(cx=centerx, cy=centery, r=radius), self.random_color())