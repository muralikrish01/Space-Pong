import pygame
import math
import random
import time
import sys

#Initialization
#-------------------
pygame.init()

#Colors
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
blue  = (0,0,255)
lightblue = (86,167,233)
red = (255,0,0)
brightgreen = (70,247,51)
turquoiseblue = (53,235,244)

#Resoultion
display_width = 800
display_height = 600

center_x = int(display_width/2)
center_y = int(display_height/2)
screenCenter = (center_x,center_y)
linethickness = 10

##gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)
pygame.display.set_caption('Space Pong')

#Sounds
PongPaddleSound = pygame.mixer.Sound("Assets\PongPaddle.wav")
PongEdgeSound = pygame.mixer.Sound("Assets\PongEdge.wav")

pygame.mixer.music.load("Assets\Sugar.mp3")
pygame.mixer.music.set_volume(1.0)

SFXEnabled = True
musicEnabled = True

#Time
clock = pygame.time.Clock()
FPS = 250
playtime = 0

#Fonts
normalFont = 'freesansbold.ttf'
realFont = 'Assets\MEGALOKG.TTF'
font = realFont
scoreText = pygame.font.Font(font,40)
flashText =  pygame.font.Font(font,80)
logoText = pygame.font.Font(font,100)
buttonText = pygame.font.Font(font,25)

#Game Settings
win_score = 11
speed = 2
ddaExploitON = False

#Confirm Quit
def confirmQuit():
    pygame.quit()
    sys.exit()

#Toggle Music
def toggleMusic():
    global musicEnabled
    if musicEnabled:
        pygame.mixer.music.pause()
        musicEnabled = False
    else:
        pygame.mixer.music.unpause()
        musicEnabled = True

#Toggle SFX
def toggleSFX():
    global SFXEnabled
    if SFXEnabled:
        SFXEnabled = False
    else:
        SFXEnabled = True

#Toggle SpeedX
def toggleSpeedX():
    global speed
    if speed == 1:
        speed = 2
    elif speed==2:
        speed = 4
    elif speed==4:
        speed = 1

#Toggle Win Score
def toggleWinScore():
    global win_score
    if win_score == 5:
        win_score = 11
    elif win_score == 11:
        win_score = 21
    elif win_score == 21:
        win_score = 5

#Flash Screen
def FlashScreen():
    gameDisplay.fill(black)
    TextSurf = flashText.render('Play Hard!!', True,red)
    TextRect = TextSurf.get_rect()
    TextRect.center = (display_width/2,display_height/2)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.flip()
    time.sleep(2)
        

#Settings Menu
def settingsMenu():
    lock = False
    global speed
    global win_score
    backPressed = False
    mouseButtonState = (0,0,0)
    bWidth = 270
    bHeight = 70
    musicb_posy = 100
    offset = 20
    color = white
    changeColor = blue
    mousePos = pygame.mouse.get_pos()
    speedState ='2X'
    time.sleep(1)
    while not backPressed:
        gameDisplay.fill(white)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
        
        #Draw Music Toggle Button
        musicb = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(musicb,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(musicb,white,((0,0),(bWidth,bHeight)),5)
        musicbRect = musicb.get_rect()
        musicbRect.center = ((display_width/2),musicb_posy)
        
        if (mousePos[0] > musicbRect.left and mousePos[0] < musicbRect.right) and (mousePos[1] > musicbRect.top and mousePos[1] < musicbRect.bottom):
            musicbHover = True
            if pygame.mouse.get_pressed()[0]:
                if not lock:
                    toggleMusic()
                    lock = True
            else:
                lock = False
                
        else:
            musicbHover = False
            
        if musicbHover:
            color = changeColor
        else:
            color = white
        
        if musicEnabled:
            musicState = 'Hit the beat'
        else:
            musicState = 'My ear hurts'
        TextSurf = buttonText.render('Music: %s'%(musicState), True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        musicb.blit(TextSurf, TextRect)
        
        gameDisplay.blit(musicb,musicbRect)
        #Draw SFX Toggle Button
        SFXb_posy = musicb_posy + bHeight + offset
        SFXb = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(SFXb,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(SFXb,white,((0,0),(bWidth,bHeight)),5)
        SFXbRect = SFXb.get_rect()
        SFXbRect.center = ((display_width/2),SFXb_posy)
        
        if (mousePos[0] > SFXbRect.left and mousePos[0] < SFXbRect.right) and (mousePos[1] > SFXbRect.top and mousePos[1] < SFXbRect.bottom):
            SFXbHover = True
            if pygame.mouse.get_pressed()[0]:
                if not lock:
                    toggleSFX()
                    lock = True
            else:
                lock = False
                
        else:
            SFXbHover = False
            
        if SFXbHover:
            color = changeColor
        else:
            color = white
        
        if SFXEnabled:
            SFXState = 'On'
        else:
            SFXState = 'Off'
        TextSurf = buttonText.render('SFX: %s'%(SFXState), True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        SFXb.blit(TextSurf, TextRect)
        
        gameDisplay.blit(SFXb,SFXbRect)
        #Draw Speed Multiplier Button
        speedXb_posy = SFXb_posy + bHeight + offset
        speedXb = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(speedXb,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(speedXb,white,((0,0),(bWidth,bHeight)),5)
        speedXbRect = speedXb.get_rect()
        speedXbRect.center = ((display_width/2),speedXb_posy)
        
        if (mousePos[0] > speedXbRect.left and mousePos[0] < speedXbRect.right) and (mousePos[1] > speedXbRect.top and mousePos[1] < speedXbRect.bottom):
            speedXbHover = True
            if pygame.mouse.get_pressed()[0]:
                if not lock:
                    lock = True
                    toggleSpeedX()

            else:
                lock = False
        else:
            speedXbHover = False
            
        if speedXbHover:
            color = changeColor
        else:
            color = white

        if speed == 1:
            speedState = 'Baby mode'
        elif speed == 2:
            speedState = 'I can play'
        elif speed == 4:
            speedState = 'Bring it on!'
        
        TextSurf = buttonText.render('Speed: %s'%(speedState), True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        speedXb.blit(TextSurf, TextRect)
        
        gameDisplay.blit(speedXb,speedXbRect)
        #Draw Win Score Button
        winscoreb_posy = speedXb_posy + bHeight + offset
        winscoreb = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(winscoreb,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(winscoreb,white,((0,0),(bWidth,bHeight)),5)
        winscorebRect = winscoreb.get_rect()
        winscorebRect.center = ((display_width/2),winscoreb_posy)
        
        if (mousePos[0] > winscorebRect.left and mousePos[0] < winscorebRect.right) and (mousePos[1] > winscorebRect.top and mousePos[1] < winscorebRect.bottom):
            winscorebHover = True
            if pygame.mouse.get_pressed()[0]:
                if not lock:
                    lock = True
                    toggleWinScore()

            else:
                lock = False
        else:
            winscorebHover = False
            
        if winscorebHover:
            color = changeColor
        else:
            color = white

        if win_score == 5:
            winScoreState = '5'
        elif win_score == 11:
            winScoreState = '11'
        elif win_score == 21:
            winScoreState = '21'
        
        TextSurf = buttonText.render('Win Score: %s'%(winScoreState), True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        winscoreb.blit(TextSurf, TextRect)
        
        gameDisplay.blit(winscoreb,winscorebRect)
        #Draw Back Button
        backb_posy = display_height - bHeight - offset
        backb = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(backb,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(backb,white,((0,0),(bWidth,bHeight)),5)
        backbRect = backb.get_rect()
        backbRect.center = ((display_width/2),backb_posy)
        
        if (mousePos[0] > backbRect.left and mousePos[0] < backbRect.right) and (mousePos[1] > backbRect.top and mousePos[1] < backbRect.bottom):
            backbHover = True
            if pygame.mouse.get_pressed()[0]:
                if not lock:
                    startMenu()
                    lock = True
            else:
                lock = False
                
        else:
            backbHover = False
            
        if backbHover:
            color = changeColor
        else:
            color = white
        
        
        TextSurf = buttonText.render('Back', True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        backb.blit(TextSurf, TextRect)
        
        gameDisplay.blit(backb,backbRect)


        pygame.display.flip()
       
#Start Menu
def startMenu():
    global insideGameLoop
    insideGameLoop = False
    time.sleep(1)
    bWidth = 250
    bHeight = 70
    startb_posy = 250
    offset = 25
    color = white
    changeColor = blue
    gameExit = False
    mousePos = pygame.mouse.get_pos()
    mouseButtonState = (0,0,0)
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
            
        gameDisplay.fill(white)
        
        #Draw Game Logo
        TextSurf = logoText.render('SPACE PONG', True, black)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((display_width/2),100)
        gameDisplay.blit(TextSurf, TextRect)
        TextSurf = scoreText.render('AI version!',True,blue)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((display_width/2),160)
        gameDisplay.blit(TextSurf, TextRect)
        
        #Draw Start Button
    
        startb = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(startb,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(startb,white,((0,0),(bWidth,bHeight)),5)
        
        startRect = startb.get_rect()
        startRect.center = ((display_width/2),startb_posy)
        
        if (mousePos[0] > startRect.left and mousePos[0] < startRect.right) and (mousePos[1] > startRect.top and mousePos[1] < startRect.bottom):
            startHover = True
            if pygame.mouse.get_pressed()[0]:
                gameLoop()
        else:
            startHover = False
            
        if startHover:
            color = changeColor
        else:
            color = white
        
        
        TextSurf = buttonText.render('Start', True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        startb.blit(TextSurf, TextRect)
        
        gameDisplay.blit(startb,startRect)
        
        #Draw Settings Button
        settingsb_posy = startb_posy + bHeight + offset
        settings = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(settings,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(settings,white,((0,0),(bWidth,bHeight)),5)
        settingsRect = settings.get_rect()
        settingsRect.center = ((display_width/2),settingsb_posy)
        gameDisplay.blit(settings,settingsRect)

        if (mousePos[0] > settingsRect.left and mousePos[0] < settingsRect.right) and (mousePos[1] > settingsRect.top and mousePos[1] < settingsRect.bottom):
            settingsHover = True
            if pygame.mouse.get_pressed()[0]:
                settingsMenu()
        else:
            settingsHover = False
            
        if settingsHover:
            color = changeColor
        else:
            color = white
        
        TextSurf = buttonText.render('Settings', True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        settings.blit(TextSurf, TextRect)

        gameDisplay.blit(settings,settingsRect)
        
        #Draw Draw Quit Button
        quitb_posy = settingsb_posy + bHeight + offset
        quitb = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(quitb,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(quitb,white,((0,0),(bWidth,bHeight)),5)
        quitbRect = quitb.get_rect()
        quitbRect.center = ((display_width/2),quitb_posy)
        gameDisplay.blit(quitb,quitbRect)

        if (mousePos[0] > quitbRect.left and mousePos[0] < quitbRect.right) and (mousePos[1] > quitbRect.top and mousePos[1] < quitbRect.bottom):
            quitbHover = True
            if pygame.mouse.get_pressed()[0]:
                confirmQuit()
        else:
            quitbHover = False
            
        if quitbHover:
            color = changeColor
        else:
            color = white

        TextSurf = buttonText.render('Quit', True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        quitb.blit(TextSurf, TextRect)

        gameDisplay.blit(quitb,quitbRect)
        color = white
        
        pygame.display.flip()
        if gameExit:
            pygame.quit()
            quit()

#Pause Menu
def pauseMenu():
    pause = True
    pauseScreen = pygame.Surface((display_width,display_height))
    pauseScreen.set_alpha(200)
    pauseScreen.fill(black)
    lock = False
    #Paused Text
    smallText = pygame.font.Font(font,50)
    TextSurf = smallText.render('Taking a Break', True, green)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(50))
    gameDisplay.blit(pauseScreen,pauseScreen.get_rect())
    gameDisplay.blit(TextSurf, TextRect)
    
    bWidth = 350
    bHeight = 70
    mainMenub_posy = 250
    offset = 25
    color = white
    changeColor = blue
    mousePos = pygame.mouse.get_pos()
    mouseButtonState = (0,0,0)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitConfirm()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
        
        #Go Back to Main Menu Text
        
        mainMenub = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(mainMenub,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(mainMenub,white,((0,0),(bWidth,bHeight)),5)
        mainMenubRect = mainMenub.get_rect()
        mainMenubRect.center = ((display_width/2),mainMenub_posy)
        
        if (mousePos[0] > mainMenubRect.left and mousePos[0] < mainMenubRect.right) and (mousePos[1] > mainMenubRect.top and mousePos[1] < mainMenubRect.bottom):
            mainMenubHover = True
            if pygame.mouse.get_pressed()[0]:
                if not lock:
                    startMenu()
                    lock = True
            else:
                lock = False
        else:
            mainMenubHover = False
            
        if mainMenubHover:
            color = changeColor
        else:
            color = white
        
        
        TextSurf = buttonText.render('Go Back to Main Menu', True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        mainMenub.blit(TextSurf, TextRect)
        
        gameDisplay.blit(mainMenub,mainMenubRect)
        #Draw Music Toggle Button
        musicb_posy = mainMenub_posy + bHeight + offset
        musicb = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(musicb,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(musicb,white,((0,0),(bWidth,bHeight)),5)
        musicbRect = musicb.get_rect()
        musicbRect.center = ((display_width/2),musicb_posy)
        
        if (mousePos[0] > musicbRect.left and mousePos[0] < musicbRect.right) and (mousePos[1] > musicbRect.top and mousePos[1] < musicbRect.bottom):
            musicbHover = True
            if pygame.mouse.get_pressed()[0]:
                if not lock:
                    toggleMusic()
                    lock = True
            else:
                lock = False
                
        else:
            musicbHover = False
            
        if musicbHover:
            color = changeColor
        else:
            color = white
        
        if musicEnabled:
            musicState = 'Hit the beat'
        else:
            musicState = 'My ear hurts'
        TextSurf = buttonText.render('Music: %s'%(musicState), True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        musicb.blit(TextSurf, TextRect)
        
        gameDisplay.blit(musicb,musicbRect)
        #Draw SFX Toggle Button
        SFXb_posy = musicb_posy + bHeight + offset
        SFXb = pygame.Surface((bWidth,bHeight))
        pygame.draw.rect(SFXb,red,((0,0),(bWidth,bHeight)))
        pygame.draw.rect(SFXb,white,((0,0),(bWidth,bHeight)),5)
        SFXbRect = SFXb.get_rect()
        SFXbRect.center = ((display_width/2),SFXb_posy)
        
        if (mousePos[0] > SFXbRect.left and mousePos[0] < SFXbRect.right) and (mousePos[1] > SFXbRect.top and mousePos[1] < SFXbRect.bottom):
            SFXbHover = True
            if pygame.mouse.get_pressed()[0]:
                if not lock:
                    toggleSFX()
                    lock = True
            else:
                lock = False
                
        else:
            SFXbHover = False
            
        if SFXbHover:
            color = changeColor
        else:
            color = white
        
        if SFXEnabled:
            SFXState = 'On'
        else:
            SFXState = 'Off'
        TextSurf = buttonText.render('SFX: %s'%(SFXState), True, color)
        TextRect = TextSurf.get_rect()
        TextRect.center = (bWidth/2,bHeight/2)
        SFXb.blit(TextSurf, TextRect)
        
        gameDisplay.blit(SFXb,SFXbRect)
        pygame.display.flip()
        
#Game Over
def gameOver(player):
    global score1
    global score2
    gameDisplay.fill(black)
    TextSurf = scoreText.render('%s'%(player), True, white)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.flip()
    score1 = 0
    score2 = 0
    time.sleep(3)
    startMenu()
    

#Player Creation
def playerCreate():
    global paddle_width
    paddle_width = 10
    global paddle_height
    paddle_height = 100

    paddle_color = white
    
    global player1
    player1 = pygame.Surface((paddle_width,paddle_height))
    pygame.draw.rect(player1,paddle_color,[0,0,paddle_width,paddle_height])
    player1 = player1.convert()
    global player2
    player2 = pygame.Surface((paddle_width,paddle_height))
    pygame.draw.rect(player2,paddle_color,[0,0,paddle_width,paddle_height])
    player2 = player2.convert()
    
    offset = 20
    

    global x1
    x1 = linethickness*2 + offset
    global x2
    x2 = display_width - linethickness*2 - offset - paddle_width
        
    global y1
    y1 = display_height/2 - paddle_height/2
    global y2
    y2 = display_height/2 - paddle_height/2

    global score1
    score1 = 0
    global score2
    score2 = 0

    global count
    count = 0

    global count2
    count2 = 0

#Ball Creation
def ballCreate():
    global directionX
    global directionY
    if ddaExploitON:
        directionY = [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    else:
        directionY = [1,-1]
    directionX = [1,-1]
    global radius
    global diameter
    global ballX
    global ballY
    global ball_dirX
    global ball_dirY
    global ball
    radius = 8
    diameter = radius*2
    ballX = int(display_width/2) - int(linethickness/1.5)
    ballY = int(display_height/2)
    ball_dirX = random.choice(directionX)
    ball_dirY = random.choice(directionY)
    ball = pygame.Surface((diameter,diameter))
    ball.fill(lightblue)
    ball.set_colorkey(lightblue)
    pygame.draw.circle(ball,brightgreen,(radius, radius),radius)

#Process Player Input
#--------------------
def processPlayerInput():
    global y1_change
    global y2_change
    global gameExit
    global pause
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                y1_change = -5
            if event.key == pygame.K_s:
                y1_change = 5
            if event.key == pygame.K_UP:
                y2_change = -5
            if event.key == pygame.K_DOWN:
                y2_change = 5
            if event.key == pygame.K_ESCAPE:
                pause = True
                pause = pauseMenu()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                y1_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y2_change = 0
                

#Play Sound
#----------
def playPaddleSound():
    if SFXEnabled:
        pygame.mixer.Sound.play(PongPaddleSound)

def playEdgeSound():
    if SFXEnabled:
        pygame.mixer.Sound.play(PongEdgeSound)

def playMusic():
    if musicEnabled and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)
        

#Game Logic
#----------
def changePos(player,x,y,y_change):
    if y < 0 + linethickness:
        return linethickness
    elif y + paddle_height > display_height - linethickness:
        return display_height - paddle_height - linethickness
    else:
        y += y_change
        return y

def changeAIPos(player,x,y):
    awake = [True, False, False, True,True,True,False,False]
    AIAwake = random.choice(awake)
    mood = [-1,0,1,1,1,1,0,1,1,1,1,-1,1,1,1,1,1]
    AIMood = random.choice(mood)
    AIMood = 1
    if y < 0 + linethickness:
        return linethickness
    elif y + paddle_height > display_height - linethickness:
        return display_height - paddle_height - linethickness
    else:
        if (y + paddle_height/2 > ballY + radius) and (ballX >= display_width/2 +50):
            y -= 0.65*speed*AIMood
            if (y < 0 + linethickness) and AIAwake:
                return linethickness
            else:
                return y
        elif (y + paddle_height/2 < ballY + radius)  and (ballX >= display_width/2 + 50):
            y += 0.65*speed*AIMood
            if (y + paddle_height > display_height - linethickness) and AIAwake:
                return display_height - paddle_height - linethickness
            else:
                return y
        else:
            return y
    
def checkBoundaryCollision(ballDirX,ballDirY):
    if ballY <= (linethickness) or (ballY + diameter) >= (display_height - linethickness):
        ballDirY = ballDirY * -1
        playEdgeSound()
    return ballDirX, ballDirY

def checkPaddleCollision(x,y,ballDirX,ballDirY):    
##    if ballX == x + paddle_width and ballDirX < 0:
    if ballX == x + paddle_width and ballDirX < 0:
        if ballY + diameter > y and ballY < y + paddle_height:
            ballDirX = ballDirX * -1
            playPaddleSound()
##    if ballX + diameter == x and ballDirX > 0:
    if ballX + diameter == x and ballDirX > 0:
        if ballY + diameter > y and ballY < y + paddle_height: 
            ballDirX = ballDirX * -1
            playPaddleSound()
    return ballDirX,ballDirY

def checkScoreEarned():
    global ballX
    global ballY
    global count
    global count2
    global score1
    global score2
    global ball_dirX
    global ball_dirY
    if (linethickness*2) > ballX and ball_dirX < 0:
        score2 += 1
        if score2 == win_score:
            gameOver('CPU Player Won')
            
        ballX = int(display_width/2) - int(linethickness)
        ballY = int(display_height/2) - int(linethickness/2)
        count = FPS*2
        count2 = FPS*2
        ball_dirX = random.choice(directionX)
        ball_dirY = random.choice(directionY)
    elif display_width - (linethickness*2) < ballX + diameter and ball_dirX > 0:
        score1 += 1
        if score1 == win_score:
            gameOver('Player 1 Won')
        ballX = int(display_width/2) - int(linethickness)
        ballY = int(display_height/2) - int(linethickness/2)
        count = FPS*2
        count2 = FPS*2
        ball_dirX = random.choice(directionX)
        ball_dirY = random.choice(directionY)
    
    

#Render Frame
#------------
def drawBall():
    gameDisplay.blit(ball,(ballX,ballY))

def moveBall(ballDirX,ballDirY):
    global ballX
    global ballY
    global count
    if count == 0:
        ballX += ballDirX * speed
        ballY += ballDirY * speed
    else:
        count -= 1

def drawPaddle(player,x,y):
    gameDisplay.blit(player,(x,y))

def scoreDisplay():
    global scoreText
    resultSurf = scoreText.render('Player 1   %s' %(score1), True, white)
    resultRect = resultSurf.get_rect()
    resultRect.topright = (display_width/2 - 10, linethickness*2 +5)
    gameDisplay.blit(resultSurf, resultRect)

    resultSurf = scoreText.render('%s   CPU Player' %(score2), True, white)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (display_width/2 + 10, linethickness*2 +5)
    gameDisplay.blit(resultSurf, resultRect)

def frameUpdate():
    global count2
    gameDisplay.fill(black)
    pygame.draw.rect(gameDisplay,white,((0,0),(display_width,display_height)),linethickness*2)
    pygame.draw.line(gameDisplay,white,((display_width/2),0),((display_width/2),display_height),int(linethickness/2))
    scoreDisplay()
    if count2 == 0:
        drawBall()
    else:
        count2 -= 1
    drawPaddle(player1,x1,y1)
    drawPaddle(player2,x2,y2)
            
    pygame.display.flip()

#Main Game Loop
#--------------
def gameLoop():
    global gameExit
    global pause
    global y1_change
    global y2_change
    global milliseconds
    global playtime
    global x1
    global x2
    global y1
    global y2
    global ball_dirX
    global ball_dirY
    global insideGameLoop
    insideGameLoop = True

    playerCreate()
    ballCreate()
    
    gameExit = False
    pause = False
    
    y1_change = 0
    y2_change = 0
    
    frameUpdate()

    time.sleep(2)
    
    while not gameExit:

        #Process Player Input
        processPlayerInput()

        y1 = changePos(player1,x1,y1,y1_change)
        y2 = changeAIPos(player2,x2,y2)
        
        moveBall(ball_dirX,ball_dirY)

        checkScoreEarned()

        #Collision Detection
        ball_dirX,ball_dirY = checkBoundaryCollision(ball_dirX,ball_dirY)
        ball_dirX,ball_dirY = checkPaddleCollision(x1,y1,ball_dirX,ball_dirY)
        ball_dirX,ball_dirY = checkPaddleCollision(x2,y2,ball_dirX,ball_dirY)

        clock.tick_busy_loop(FPS)
        
        frameUpdate()
        
#FlashScreen()
playMusic()
playerCreate()
ballCreate()
startMenu()
gameLoop()

pygame.quit()
sys.exit()
