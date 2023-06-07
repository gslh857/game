import pygame
import random as rn
from pygame import mixer
colours = [[0,255,255],[190,83,120],[0,255,0],[190,190,190],[238,130,238],[255,165,0],[184,94,0],[250,235,0],[189,190,57],[160,32,240]]


class Shape:
    x = 0
    y = 0

    shapes = [[[2, 6, 10, 14], [8, 9, 10, 11]],
        [[5, 6, 10, 11], [2, 6, 5, 9]],
        [[2, 3, 5, 6], [1, 5, 6, 10]],
        [[2, 3, 6, 10], [1, 5, 6, 7], [3, 7, 11, 10], [5, 6, 7, 11]],
        [[5, 6, 10, 14], [1, 2, 3, 5], [1, 5, 9, 10], [9, 10, 11, 7]],
        [[2, 5, 6, 7], [2, 5, 6, 10], [5, 6, 7, 10], [2, 6, 7, 10]],
        [[0, 1, 5, 4]]
    ]


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.figure = rn.randint(0, len(self.shapes) - 1)
        self.color = rn.randint(1, len(colours) - 1)
        self.rot = 0

    def image(self):
        return self.shapes[self.figure][self.rot]



