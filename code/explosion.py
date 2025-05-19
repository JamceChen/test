from gameobject import GameObject
import random
from pathlib import Path
import pygame

#爆炸類別
class Explosion(GameObject):

    explosion_effect = []

    #建構式
    def __init__(self, xy = None, scale_factor = 0.8):
        GameObject.__init__(self)
        if xy is None:
            self._x = -100
            self._y = random.randint(10, self._playground[0] - 100)
        
        else:
            self._x = xy[0]
            self._y = xy[1]

        if Explosion.explosion_effect:
            pass
            
        #建立爆炸效果圖片序列
        else:
            __parent_path = Path(__file__).parents[1]
            for i in range(9):
                icon_path = __parent_path / 'assets' / 'images' / f'expl{i}.png'
                img = pygame.image.load(icon_path)
                # 縮放圖片
                original_width = img.get_rect().width
                original_height = img.get_rect().height
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                img = pygame.transform.smoothscale(img, (new_width, new_height))
                Explosion.explosion_effect.append(img)
        
        self.__image_index = 0
        self._image = Explosion.explosion_effect[self.__image_index]
        self.__fps_count = 0
    
    def update(self):
        self.__fps_count += 1
        if self.__fps_count >= 12:  # 加快動畫速度
            self.__image_index += 1
            if self.__image_index >= 8:
                self._available = False

            else:
                self._image = Explosion.explosion_effect[self.__image_index]
                self.__fps_count = 0
