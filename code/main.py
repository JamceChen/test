import pygame
from pathlib import Path
from player import Player
from mymissile import MyMissile
from enemy import Enemy
import random

#初始化pygame系統
pygame.init()

parent_path = Path(__file__).parents[1]
image_path = parent_path /'assets' /'images'
icon_path = image_path /'icon.png'
background_path = image_path /'background.png'
gameover_path = image_path /'gameover.png'

#建立視窗物件，寬、高、參數
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
Enemies = []
#建立事件編號
launchMissile = pygame.USEREVENT + 1
spawnEnemy = pygame.USEREVENT + 2

#Title, icon, and Background
pygame.display.set_caption("戰鬥機")
icon = pygame.image.load(icon_path) #載入圖示
pygame.display.set_icon(icon)
background = pygame.image.load(background_path).convert()
gameover = pygame.image.load(gameover_path).convert()

# 設定字體
font = pygame.font.Font(None, 36)  # None 使用預設字體，36 是字體大小

# 設定敵人生成計時器
pygame.time.set_timer(spawnEnemy, 1000)  # 每1秒生成一個敵人

#設定無窮迴圈，讓視窗保持更新與執行
while running:
    #從pygame事件佇列中，一項一項檢查
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 如果玩家死亡，只處理退出事件
        if player._hp <= 0:
            continue

        #飛彈連續發射設定
        if event.type == launchMissile:
            m_x = player._x - 100
            m_y = player._y
            Missiles.append(
                MyMissile(
                    xy = (m_x, m_y), 
                    playground = playground, 
                    sensitivity = movingScale
                )
            )
            m_x = player._x - 10
            Missiles.append(
                MyMissile(
                    xy = (m_x, m_y), 
                    playground = playground, 
                    sensitivity = movingScale
                )
            )

        # 敵人生成事件
        if event.type == spawnEnemy:
            enemy_x = random.randint(0, screenWidth - 50)  # 敵人寬度50
            Enemies.append(
                Enemy(
                    playground = playground, 
                    xy = (enemy_x, -50),
                    sensitivity = movingScale
                )
            )

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

            #飛彈普通發射設定
            if event.key == pygame.K_SPACE:
                m_x = player._x - 100
                m_y = player._y 
                Missiles.append(
                    MyMissile(
                        xy = (m_x, m_y), 
                        playground = playground, 
                        sensitivity = movingScale
                    )
                )
                m_x =player._x - 10
                Missiles.append(
                    MyMissile(
                        xy = (m_x, m_y), 
                        playground = playground, 
                        sensitivity = movingScale
                    )
                ) #若為指定參數，需按照宣告順序
                pygame.time.set_timer(launchMissile, 400) #之後每400ms發射一組

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
            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(launchMissile, 0) #停止發射

    screen.blit(background, (0, 0)) #更新背景圖片
    Missiles = [item for item in Missiles if item._available]
    Enemies = [item for item in Enemies if item._available]
    
    # 如果玩家還活著，繼續遊戲
    if player._hp > 0:
        #繪製子彈
        for m in Missiles:
            m.update()
            screen.blit(m._image, (m._x, m._y))
            # 檢測子彈與敵人的碰撞
            m.collision_detect(Enemies)
        
        #繪製敵人
        for e in Enemies:
            e.update()
            screen.blit(e._image, (e._x, e._y))
            # 檢測敵人與玩家的碰撞
            player.collision_detect([e])
        
        #繪製玩家
        player.update() #更新player狀態
        screen.blit(player._image, (player._x, player._y))
        
        # 顯示血量
        hp_text = font.render(f"HP: {player._hp}", True, (255, 255, 255))
        screen.blit(hp_text, (10, 10))
    else:
        # 顯示遊戲結束畫面
        screen.blit(gameover, (screenWidth//2 - gameover.get_width()//2, 
                             screenHigh//2 - gameover.get_height()//2))
    
    pygame.display.update() #更新螢幕狀態
    dt =clock.tick(fps) #每秒更新fps次

pygame.quit() #關閉繪圖視窗