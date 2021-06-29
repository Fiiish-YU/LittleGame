# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 14:24:09 2020

@author: xun
"""
#图片重读
from PyQt5.QtGui import *

img = QImage()
img.load("C:/Users/xun/Documents/mypython/fighting_plane/images/game_begin.png")
img.save("C:/Users/xun/Documents/mypython/fighting_plane/images/game_begin.png")