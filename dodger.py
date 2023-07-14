import pygame, sys, random 

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
TEXT_COLOR = 'black'
BG_COLOR = 'lightblue'
BADDIE_MIN_SIZE = 10
BADDIE_MAX_SIZE = 40
BADDIE_MIN_SPEED = 1
BADDIE_MAX_SPEED = 8
ADD_NEW_BADDIE_RATE = 7
PLAYER_MOVE_RATE = 6 
FPS = 40



"""
Setting up pygame
"""
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Dodger')
font = pygame.font.SysFont("Arial", 30, "bold")
clock = pygame.time.Clock()

# set the mouse cursor to be false 
# can just use player icon as the cursor 
pygame.mouse.set_visible(False)

# set up images and sounds
playerImage = pygame.image.load('player.png')
baddieImage = pygame.image.load('baddie.png')
gameoverSound = pygame.mixer.Sound('gameover.wav')

# get player rect so can check whether player collides with baddie rect (gameover)
playerRect = playerImage.get_rect()


"""
Functions to support the while loop(to keep the game running) later on 
"""
# just for convenience
# if subsequent functions need to terminate the game 
def terminate():
    pygame.quit()
    sys.exit()

# start the game only if player pressed a random key 
# but if player mousebuttondown top right corner "X" / press RETURN
# quit the game 
# pressing other key will return this while loop, starting the game
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    terminate()
                return 

# drawing the text 
# an overall function, whether its for the starting scene, gameover scene or score of the game 
# first get the rectangle of the text 
# so that u can set the top left to be x and y (arguments given to this function)
def drawText(text, font, surface, x, y):
    textObj = font.render(text, True, TEXT_COLOR)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)

# if player hits baddie (player rectangle collides with baddies rect)
# must check for all baddies 
# so in the first place ur baddie is not just a single baddie 
# its a list of many baddies 
# arguments for this function should include a list of baddies and player rect
def playerHitsBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True 
    return False 


"""
keep a record of the top score 
"""
topScore = 0


"""
show the "starting" scene, which u need to press a key to start 
this scene wont appear again
if u restart, the "gameover" ending scene will prompt u to restart instead of this starting scene
"""
window.fill(BG_COLOR) # always draw bg first 
drawText('Dodger', font, window, (WINDOW_WIDTH/3 + 45), (WINDOW_HEIGHT/3 + 20))
drawText('Press a key to start', font, window, (WINDOW_WIDTH/3 - 30), (WINDOW_HEIGHT/3 + 75))
drawText('Press RETURN to quit', font, window, (WINDOW_WIDTH/3 - 45), (WINDOW_HEIGHT/3 + 140))
pygame.display.update()
waitForPlayerToPressKey()

"""
a while loop to pause the game when gameover, not end it 
so that u can set the start and end of the game, then set option to restart 
start being starting scene, already drawn out in the aforementioned section ^^
end being gameover scene(gameover sound, text, and option to restart), drawing at the end of this while loop
then if player were to press key, the game can restart 
restart by starting a second while loop of this outer while loop 
"""
while True:
    """
    set up the start of the game 
    """
    # set a list of baddies 
    # set in while loop and keep appending so no. of baddies dropping will never end 
    # also rmb the player rect is being checked for collision against a list of all baddies, not just one
    # so we need a list here 
    baddies = []

    # set a score that will keep increasing in the while loop 
    # so when the loop keeps on running, the score increases with time 
    score = 0

    # set the starting position of the player 
    # bottom centre so player has time to evade baddies dropping from the top
    # set it with position with respect to the player image's center
    playerRect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 50)

    # all player movement set to false at the start of the game 
    left = right = up =  down = False

    # set player cheating methods to false 
    # 1. reverse. can reverse the direction of the baddies, make player seem like it is dropping further than baddie 
    # 2. slow down. slow down the speed of the baddies dropping from the top 
    reverse = slow = False

    # initialise adding baddie to 0 
    baddieAddCounter = 0 


    """
    inner while loop created to keep the game running 
    if gameover, break this inner while loop, go to outer while loop to display end scenes
    then from there wait for player to press key to restart the game again
    """
    while True:
        # score increases with time while the ganme runs 
        score += 1

        # pygame events 
        for event in pygame.event.get():
            # for quiting 
            if event.type == pygame.QUIT:
                terminate()

            """
            for player control
            """
            # wasd / key up down left right for player movement
            # z to reverse (cheat)
            # x to slow down (cheat)
            if event.type == pygame.KEYDOWN:
                if event.key == ord('z'):
                    reverse = True 
                if event.key == ord('x'):
                    slow = True 
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    right = False 
                    left = True 
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    right = True
                    left = False
                if event.key == pygame.K_UP or event.key == ord('w'):
                    down = False 
                    up = True 
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    down  = True 
                    up = False 
                # for quitting 
                if event.key == pygame.K_RETURN:
                    terminate()

            # if release the key 
            if event.type == pygame.KEYUP:
                if event.key == ord('z'):
                    reverse = False 
                if event.key == ord('x'):
                    slow = False 
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    left = False
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    right = False
                if event.key == pygame.K_UP or event.key == ord('w'):
                    up = False
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    down = False
                
            # if mouse move, move the player where the cursor is 
            if event.type == pygame.MOUSEMOTION:
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)
            
        # player movement (check whether it is possible)
        # if for eg, the cursor is at the ultimate left of the window (0), the player wont move left anymore
        if left and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
        if right and playerRect.right < WINDOW_WIDTH:
            playerRect.move_ip(PLAYER_MOVE_RATE, 0)
        if up and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYER_MOVE_RATE)
        if down and playerRect.bottom < WINDOW_HEIGHT:
            playerRect.move_ip(0, PLAYER_MOVE_RATE)


        """
        for baddie control
        """
        # adding baddies to the list (append it to the baddie list)
        # for newBaddie rect, Rect(left, top, width, height)
        # the starting left for baddie rect will be a random int between 0 and window_width - baddie_size 
        # so that the baddie will start falling from different point horizontally 
        # the top is 0 - baddie_size so the baddies start falling from the top before the game start(cant be seen at the start)
        # since it is < 0 of the window 
        if not reverse and not slow:
            baddieAddCounter += 1
        if baddieAddCounter == ADD_NEW_BADDIE_RATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIE_MIN_SIZE, BADDIE_MAX_SIZE)
            baddieSpeed = random.randint(BADDIE_MIN_SPEED, BADDIE_MAX_SPEED)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOW_WIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                         'speed': baddieSpeed, 
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize))}
            
            baddies.append(newBaddie)
        
        # baddie movement(moving the baddies down)
        # delete baddies that fall past the bottom 
        for b in baddies:
            if not reverse and not slow:
                b['rect'].move_ip(0, b['speed'])
            elif reverse:
                b['rect'].move_ip(0, -5)
            elif slow:
                b['rect'].move_ip(0, 1)

            if b['rect'].top > WINDOW_HEIGHT:
                baddies.remove(b)

        """
        settings control
        """
        # draw the window background 
        # always draw bg first 
        window.fill(BG_COLOR)

        # draw the score and the top score on the top left hand corner 
        drawText('Score:' + str(score), font, window, 10, 0)
        drawText('Top Score:' + str(topScore), font, window, 10, 40)

        # draw the player onto the player rect 
        # blit(source, dest, area=None, special_flags=0)
        window.blit(playerImage, playerRect)

        # draw the baddies onto the baddies rect (after scaling)
        for b in baddies:
            window.blit(b['surface'], b['rect'])

        # check if player hit baddies, end current round of game 
        if playerHitsBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score 
            break

        # keep updating the game 
        pygame.display.update()
        clock.tick(FPS)


    """
    set up the end of the game
    """
    # gameover sound and text(using drawText)
    # then update everything with the display
    # wait for player to press a key to restart 
    # stop the sound from playing 
    # AND
    # put waitForPlayerToPressKey(), if key is pressed, that function's while loop will be returned, this outer while 
    # loop to run the game will restart again, restarting the game 
    # if key is not pressed, the control will be trapped in that function's while loop, the gameover scene will be paused there 
    # until a key is pressed 
    # if RETURN is pressed, terminate the game 
    gameoverSound.play()
    drawText('GAME OVER', font, window, (WINDOW_WIDTH/3 + 20), (WINDOW_HEIGHT/3 + 50))
    drawText('Press a key to play again.', font, window, (WINDOW_WIDTH/3 - 55), (WINDOW_HEIGHT/3 + 100))
    pygame.display.update()
    waitForPlayerToPressKey()
    gameoverSound.stop()