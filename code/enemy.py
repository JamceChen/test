from pathlib import Path
from typing import Union
import pygame
from pygame.surface import Surface, SurfaceType
from gameobject import GameObject
import math
import random

#玩家類別
class Enemy(GameObject):
    #建構式，playground 為必要參數
    def __init__(self, playground, xy = None, sensitivity = 1, scale_factor = 0.2):
        GameObject.__init__(self, playground)
        self._moveScale = 0.5 * sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__enemy_path = __parent_path /'assets' /'images' /'enemy0.png'
        self._image = pygame.image.load(self.__enemy_path)

        # 縮放圖片
        original_width = self._image.get_rect().width
        original_height = self._image.get_rect().height
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self._image = pygame.transform.smoothscale(
            self._image, 
            (new_width, new_height)
        )
        self._image = pygame.transform.flip(self._image, False, True)  # 垂直翻轉（180 度）

        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w)/2
            self._y = 3 * self._playground[1]/4
        
        else:
            self._x = xy[0]#貼圖位置
            self._y = xy[1]
        
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2
        self._radius = 0.3 * math.hypot(
            self._image.get_rect().w, 
            self._image.get_rect().h
        ) #碰撞半徑
        
        # 隨機初始水平速度方向
        self._vx = random.choice([-1, 1]) * 2  # 水平速度，每次update移動2像素
        self._vy = 1  # 垂直速度，每次update移動1像素

        self._objectBound = (
            10, 
            self._playground[0] - (self._image.get_rect().w + 10), 
            10, 
            self._playground[1] - (self._image.get_rect().h + 10)
        )
    
    def update(self):
        GameObject.update(self)
        #自己往下移動
        self._y += self._vy
        #左右自動移動
        self._x += self._vx

        #邊界檢查&反彈
        if self._x <= self._objectBound[0]: #碰到左邊界
            self._x = self._objectBound[0] #修正位置，避免卡在邊界
            self._vx = -self._vx #水平反彈
        
        elif self._x >= self._objectBound[1]: #碰到右邊界
            self._x = self._objectBound[1] #修正位置，變免卡在邊界
            self._vx = -self._vx #水平反彈
        
        #如果敵人超出下邊界，設為不可用
        if self._y > self._objectBound[3]:
            self._available = False
        
        #更新中心點
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2
    
    #碰撞偵測(與其他物件)
    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                self._collided = True
                self._available = False
                m._collided = True