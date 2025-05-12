import pygame
from pathlib import Path
from player import Player
from mymissile import MyMissile

#初始化pygame系統
pygame.init()

parent_path = Path(__file__).parents[1]
image_path = parent_path /'assets' /'images'
icon_path = image_path /'icon.png'

#建立視窗物件，寬、高
screenHigh = 760
screenWidth = 1000
playground = [screenWidth, screenHigh]
screen = pygame.display.set_mode((screenWidth, screenHigh))
running = True
fps = 120 #更新頻率，包含畫面更新與事件更新
movingScale = 600/fps #大約600 像素/秒
clock = pygame.time.Clock() #創建一個物件來幫助追蹤時間
player = Player(playground = playground, sensitivity = movingScale)
keyCountX = 0
keyCountY = 0 #計算案件被按下的次數
#建立物件串列
Missiles = []
#建立事件編號
launchMissile = pygame.USEREVENT + 1

#Title, icon, and Background
pygame.display.set_caption("戰鬥機")
icon = pygame.image.load(icon_path) #載入圖示
pygame.display.set_icon(icon)
background = pygame.Surface(screen.get_size()) #取得視窗變數
background = background.convert() #改變像素格式，加快顯示速度
background.fill((50,50,50))

#設定無窮迴圈，讓視窗保持更新與執行
while running:
    #從pygame事件佇列中，一項一項檢查
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: #'a','A',左移
                keyCountX += 1
                player.to_the_left()

            if event.key == pygame.K_d: #'d','D',右移
                keyCountX += 1
                player.to_the_right()

            if event.key == pygame.K_s: #'s','S',下移
                keyCountY += 1
                player.to_the_bottom()

            if event.key == pygame.K_w: #'w','W',上移
                keyCountY += 1
                player.to_the_top()

            if event.key == pygame.K_SPACE:
                m_x = player._x + 20
                m_y = player._y
                Missiles.append(MyMissile(xy = (m_x, m_y), playground = playground, sensitivity = movingScale))
                m_x = player._x +80
                Missiles.append(MyMissile(playground, (m_x, m_y), movingScale)) #若為指定參數，需按照宣告順序

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                if keyCountX == 1:
                    keyCountX = 0
                    player.stop_x()
                else:
                    keyCountX -= 1
            if event.key == pygame.K_s or event.key == pygame.K_w:
                if keyCountY == 1:
                    keyCountY = 0
                    player.stop_y()
                else:
                    keyCountY -= 1

    screen.blit(background,(0, 0)) #更新背景圖片
    Missiles = [item for item in Missiles if item._available]
    for m in Missiles:
        m.update()
        screen.blit(m._image, (m._x, m._y))
    player.update() #更新player狀態
    screen.blit(player._image, (player._x, player._y)) #添加player圖片
    pygame.display.update() #更新螢幕狀態
    dt =clock.tick(fps) #每秒更新fps次

pygame.quit() #關閉繪圖視窗