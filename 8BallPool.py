# Project Name: 8 Ball Pool!
# Language: python
# Name: Youwei Jiang
# Andrew ID: youweij

#Physics functions reference from: 
#https://github.com/max-kov/pool
#https://www.real-world-physics-problems.com/physics-of-billiards.html

#Pictures Reference:
#https://www.familyeducation.com/fun/pub-games/pool-game-eight-ball
#https://photos.com/featured/1-pool-balls-maria-toutoudaki.html

#Sound Reference:
#https://www.soundfishing.eu/sound/billiards

#Image Drawing reference:
#http://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#imageMethods

# Events Reference:
#http://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#events

# Game AI Reference:
#http://www.cs.cmu.edu/~112/notes/notes-monte-carlo.html
# Game AI mini lecture
#https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=907a7ba8-351b-44ed-90fe-add60187c05d&start=0

from cmu_112_graphics import *
from math import *
import random
import math
import pygame

#helper functions set

#Reference: http://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)

# colors set up
pooltable = rgbString(10, 108, 3)
black = rgbString(0, 0, 0)
white = rgbString(255, 255, 255)
green = rgbString(40, 180, 99)
blue = rgbString(52, 152, 219)
red = rgbString(203, 67, 53)
orange = rgbString(255, 165, 0)
yellow = rgbString(255, 255, 0)
purple = rgbString(136, 78, 160)
brown = rgbString(165, 42, 42)
poolstick = rgbString(193, 154, 107)

radius = 10
margin = 30
width = 660
height = 360

colors = [yellow, blue, red, purple, orange, green, brown, black, 
yellow, blue, red, purple, orange, green, brown]

##########################################
# Classes
##########################################
# Ball Class
class Ball:
    def __init__(self, cx, cy, speed, color, angle, num):
        self.cx = cx
        self.cy = cy
        self.speed = speed
        self.color = color
        self.angle = angle
        self.num = num
        self.r = 7
    
    #draw the ball
    def onePlayer_drawBall(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r,
                        self.cx + self.r, self.cy + self.r,
                        fill = self.color)
        if self.color != white:
            canvas.create_oval(self.cx - self.r*0.5, self.cy - self.r*0.5, self.cx + self.r*0.5, self.cy + self.r*0.5,
        fill = "white")
            canvas.create_text(self.cx, self.cy, text = self.num, font = "Helvetica 9")

    def onePlayer_timerFired(self, app):
        # applies friction
        if self.speed <= 0:
            self.speed += 0.3
        if self.speed >= 0:
            self.speed -= 0.3
        if abs(self.speed) <= 0.3:
            self.speed = 0

        self.cx = self.cx + self.speed*math.cos(math.radians(self.angle))
        self.cy = self.cy + self.speed*math.sin(math.radians(self.angle))

        #bounce if off the pooltable
        if not (self.cx < width - radius - margin*1.2):
            self.cx = width - radius - margin - app.margin*0.2
            self.angle = 180 - self.angle
        if not(radius + margin*1.2 < self.cx):
            self.cx = radius + margin + app.margin*0.2
            self.angle = 180 - self.angle
        if not (self.cy < height - radius - margin*1.2):
            self.cy = height - radius - margin - app.margin*0.2
            self.angle = -self.angle
        if not(radius + margin*1.2 < self.cy):
            self.cy = radius + margin + app.margin*0.2
            self.angle = -self.angle
    
    #draw the ball
    def twoPlayer_drawBall(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r,
                        self.cx + self.r, self.cy + self.r,
                        fill = self.color)
        if self.color != white:
            canvas.create_oval(self.cx - self.r*0.62, self.cy - self.r*0.62, self.cx + self.r*0.62, self.cy + self.r*0.62,
        fill = "white")
            canvas.create_text(self.cx, self.cy, text = self.num, font = "Arial 8 bold")
        
    def twoPlayer_timerFired(self, app):
        # applies friction
        if self.speed <= 0:
            self.speed += 0.3
        if self.speed >= 0:
            self.speed -= 0.3
        if abs(self.speed) <= 0.3:
            self.speed = 0

        self.cx = self.cx + self.speed*math.cos(math.radians(self.angle))
        self.cy = self.cy + self.speed*math.sin(math.radians(self.angle))

        #bounce if off the pooltable
        if not (self.cx < width - radius - margin*1.2):
            self.cx = width - radius - margin - app.margin*0.2
            self.angle = 180 - self.angle
        if not(radius + margin*1.2 < self.cx):
            self.cx = radius + margin + app.margin*0.2
            self.angle = 180 - self.angle
        if not (self.cy < height - radius - margin*1.2):
            self.cy = height - radius - margin - app.margin*0.2
            self.angle = -self.angle
        if not(radius + margin*1.2 < self.cy):
            self.cy = radius + margin + app.margin*0.2
            self.angle = -self.angle

# Pocket Class
class Pockets:
    def __init__(self, x, y):
        self.r = margin/2
        self.x = x + self.r
        self.y = y + self.r

    def onePlayer_drawPocket(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = "gray")  

    def twoPlayer_drawPocket(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = "gray")  

# Reference: http://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSounds
# Sound Class
class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1

    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play(loops=loops)

    def stop(self):
        pygame.mixer.music.stop() 

#All modes reference from:
#http://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes

##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    canvas.create_image(330, 180, image=ImageTk.PhotoImage(app.image2))
    
    # Help Mode Set up
    font = 'Arial 16'
    canvas.create_text(app.width/2, 50, text= "If you choose Two Player Mode, you will be competing with your friend.", font = font)
    canvas.create_text(app.width/2, 100, text =  "If you choose One Player Mode, You will be competing with a adversary AI.", font = font)
    canvas.create_text(app.width/2, 150, text = "You can drag the cue stick at any length and any angle.", font = font)
    canvas.create_text(app.width/2, 200, text = "The force is shown at the bottom of the page. Press the mouse to release the cue ball.", font = font)
    canvas.create_text(app.width/2, 250, text = "When the game ends, press Space to quit the game.", font = font)
    canvas.create_text(app.width/2, 300, text = 'Press Space to return to the Game Menu!', font = "Arial 22 bold")
    canvas.create_text(app.width/2, 320, text = 'Press 1 to return to One Player Mode!', font = "Arial 22 bold")
    canvas.create_text(app.width/2, 340, text = 'Press 2 to return to Two Player Mode!', font = "Arial 22 bold")

def helpMode_keyPressed(app, event):
    if event.key == "Space":
        app.mode = 'gameStart'
    elif event.key == "1":
        app.mode = "onePlayer"
    elif event.key == "2":
        app.mode = "twoPlayer"

##########################################
# game Start Mode
##########################################

def gameStart_appStarted(app):
    app.image11 = app.loadImage('8BallFeature.jpg')

#switch mode
def gameStart_mousePressed(app, event):
    x1 = app.width * 0.06
    x2 = app.width * 0.46
    y0 = app.height /2

    if (event.x >= x1 and event.x <= x2 and 
    event.y >= y0 - 125 and event.y <= y0 - 25):
        app.mode = 'twoPlayer'
        app.sound[2].start()
    
    elif (event.x >= x1 and event.x <= x2 and 
    event.y >= y0 + 25 and event.y <= y0 + 125):
        app.mode = "onePlayer"
        app.sound[2].start()

def gameStart_keyPressed(app, event):
    if event.key == "Enter":
        app.mode = "helpMode"
 
def gameStart_redrawAll(app, canvas):
    x1 = app.width * 0.06
    x2 = app.width * 0.46
    y0 = app.height /2

    canvas.create_image(330, 180, image=ImageTk.PhotoImage(app.image11))
    canvas.create_rectangle( x1, y0 - 125, x2, y0 - 25, fill = "yellow")
    canvas.create_rectangle( x1, y0 + 25, x2, y0 + 125, fill = "yellow")
    canvas.create_text( app.width*0.26, y0 - 75, text = "Two Player Mode", font = "Arial 20")
    canvas.create_text( app.width*0.26, y0 + 75, text = "One Player Mode", font = "Arial 20")
    canvas.create_text( app.width*0.73, y0 - 75, text = "*Press Enter to Advance to Help Mode" , font = "Arial 20", fill = "blue")

##########################################
# Main Game App
##########################################

def appStarted(app):
    #initialize the variables
    app.image11 = app.loadImage('8BallFeature.jpg')
    app.image2 = app.loadImage('background2.jpg')
    app.margin = 30
    app.radius = 0.5*app.margin
    app.p1ballsRemaining = 7
    app.p2ballsRemaining = 7
    app.radius = 7
    app.clickx = None
    app.clicky = None
    app.startPosn = None
    app.endPosn = None
    app.force = 0
    app.length = 0
    app.tangent = 0
    app.player = 0
    app.l = 0
    app.gameWins = False
    app.gameLoses = False
    app.freeBall = False
    app.paused = False
    app.stop = True

    onePlayer_startPockets(app)
    onePlayer_restart(app)
    onePlayer_resetApp(app)
    twoPlayer_startPockets(app)
    twoPlayer_restart(app)
    twoPlayer_resetApp(app)

    pygame.mixer.init()
    app.sound = []
    app.sound.append(Sound("billiard2.mp3"))
    app.sound.append(Sound("billiard4.mp3"))
    app.sound.append(Sound("billiard1.mp3"))
    
def keyPressed(app, event):
    if event.key == "Space":
        app.mode = 'gameStart'
        app.sound[2].start()

def redrawAll(app, canvas):
    canvas.create_image(330, 180, image=ImageTk.PhotoImage(app.image11))
    canvas.create_text(app.width/2, app.height*0.25, text = "8 Ball Pool Game!", font = "Arial 50 bold", fill = blue)
    canvas.create_text(app.width * 0.3, app.height *0.85, text = "Press Space to Start Game! ", font = "Arial 22 bold")

##########################################
# One Player Mode
##########################################

#Reference: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def onePlayer_resetApp(app):
    app.timerDelay = 125

def onePlayer_appStarted(app):
    #initialize the variables
    app.margin = 30
    app.radius = 0.5*app.margin
    app.p1ballsRemaining = 7
    app.p2ballsRemaining = 7
    app.radius = 7
    app.clickx = None
    app.clicky = None
    app.startPosn = None
    app.endPosn = None
    app.force = 0
    app.length = 0
    app.tangent = 0
    app.player = 0
    app.l = 0
    app.gameWins = False
    app.gameLoses = False
    app.freeBall = False
    app.paused = False
    app.stop = True
    
    onePlayer_startPockets(app)
    onePlayer_restart(app)
    onePlayer_resetApp(app)

# Calculate the forces
def onePlayer_mouseMoved(app, event):
    if app.freeBall == False:
        if app.player % 2 == 0:
            app.clickx = event.x
            app.clicky = event.y
            app.l = distance(app.cueBall.cx , app.cueBall.cy, app.clickx, app.clicky)/ 8
            if app.l > 25:
                app.l = 25
            if app.cueBall.speed == 0:
                app.tangent = (math.degrees(math.atan2((app.cueBall.cy - app.clicky), (app.cueBall.cx - app.clickx))))
            app.t = app.tangent
    
def onePlayer_keyPressed(app, event):
    if (event.key == 'Space'):
        if app.gameLoses == True:
            onePlayer_quit(app)
        if app.gameWins == True:
            onePlayer_quit(app)
    elif (event.key == 'p'):    
        app.paused = not app.paused
    elif event.key == "h":
        app.mode = "helpMode"

def onePlayer_ballStop(app):
    for i in app.balls:
        if i.speed != 0:
            app.stop = False
            continue
        else:
            app.stop = True

# Apply the AI move           
def onePlayer_hitTheCue(app):
    if app.freeBall == False:
        if app.player % 2 == 1:
            if app.cueBall.speed == 0 and app.stop == True:
                app.cueBall.speed, app.tangent = onePlayer_findMoveMiniMax(app)
        
        app.cueBall.speed = app.force
        app.player += 1
        app.sound[0].start()
        
def onePlayer_mousePressed(app, event):
    if app.freeBall == False:
        if app.player % 2 == 0:
            app.startPosn = [app.cueBall.cx, app.cueBall.cy]
            app.endPosn = [event.x, event.y]
            app.force = distance(app.startPosn[0] , app.startPosn[1], app.endPosn[0], app.endPosn[1])/ 8
            
            if app.force > 25:
                app.force = 25
            
            if app.cueBall.speed == 0 and app.stop == True:
                onePlayer_hitTheCue(app)
                app.sound[0].start()

def onePlayer_cueBalltimerFired(app):
    # applies friction
    if app.cueBall.speed <= 0:
        app.cueBall.speed += 0.3
    if app.cueBall.speed >= 0:
        app.cueBall.speed -= 0.3
    if abs(app.cueBall.speed) <= 0.3:
        app.cueBall.speed = 0

    app.cueBall.cx += app.cueBall.speed*math.cos(math.radians(app.tangent))
    app.cueBall.cy += app.cueBall.speed*math.sin(math.radians(app.tangent))

#Reference: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#example:pong
    if (app.cueBall.cy + app.radius >= app.height - app.margin*1.2):
        # The ball went off the bottom!
        app.cueBall.cy = app.height - app.margin*1.2 - app.radius
        app.tangent = - app.tangent
    elif (app.cueBall.cy - app.radius <= app.margin*1.2):
    # The ball went off the up!
        app.cueBall.cy = app.margin*1.2 + app.radius
        app.tangent = - app.tangent
        
    if (app.cueBall.cx + app.radius >= app.width - app.margin*1.2):
    # The ball went off the right!
        app.cueBall.cx = app.width - app.margin*1.2 - app.radius
        app.tangent = 180 - app.tangent
    elif (app.cueBall.cx - app.radius <= app.margin*1.2):
    # The ball went off the left!
        app.cueBall.cx = app.margin*1.2 + app.radius
        app.tangent = 180 - app.tangent

def onePlayer_ballsTimerFired(app):
    for i in range(len(app.balls)):
        app.balls[i].onePlayer_timerFired(app)

#all the physics functions combined
def onePlayer_physics(app):
    onePlayer_cueBalltimerFired(app)
    onePlayer_checkCueCollision(app)
    onePlayer_checkBallCollision(app)
    onePlayer_inThePocket(app)
    onePlayer_ballsTimerFired(app)
    onePlayer_ballStop(app)

def onePlayer_timerFired(app):
    if app.paused == False:

        onePlayer_physics(app)
        if app.cueBall.speed == 0 and app.stop == True:
            if app.player % 2 == 1:
                
                onePlayer_hitTheCue(app)
                onePlayer_findMoveMiniMax(app)

def onePlayer_drawPoolStick(app, canvas):
    if app.cueBall.speed == 0 and app.stop == True:
        if app.clicky != None and app.clickx != None:
            canvas.create_line(app.cueBall.cx + 75*math.cos(math.radians(app.tangent)), 
            app.cueBall.cy + 75*math.sin(math.radians(app.tangent)), app.cueBall.cx, app.cueBall.cy, fill = white, width = 1)
            canvas.create_line(app.clickx, app.clicky, app.cueBall.cx, app.cueBall.cy, fill = poolstick , width = 3)

def onePlayer_redrawAll(app, canvas):
    # draw the pool table
    canvas.create_rectangle(app.margin, app.margin, app.width-app.margin, app.height - app.margin, 
    fill = pooltable, width = app.margin//2)
    canvas.create_line(app.width*0.7, app.margin*1.225, app.width*0.7, app.height - app.margin*1.225, fill = white, width = 0.3)
    #draw the balls
    for i in range(len(app.balls)):
            app.balls[i].onePlayer_drawBall(canvas)
    #draw the pockets
    for i in range(6):
        app.pockets[i].onePlayer_drawPocket(canvas)
    #draw the poolstick
    if app.freeBall == False:
        onePlayer_drawPoolStick(app, canvas)
    #draw the cueBall
    app.cueBall.onePlayer_drawBall(canvas)
    #indicate the player
    if app.player % 2 == 0:
        if app.cueBall.speed == 0 and app.stop == True:
            canvas.create_text(app.width*0.25, app.height * 0.96, text = "Player 1's Turn!", fill = "black")
    if app.player % 2 == 1:
        if app.cueBall.speed == 0 and app.stop == True:
            canvas.create_text(app.width*0.25, app.height * 0.96, text = "Player 2's Turn!", fill = "black")
    #indicate the force        
    if app.cueBall.speed == 0 and app.stop == True:
        canvas.create_text(app.width*0.75, app.height * 0.96, text = f"Force: {int(app.l)}", fill = "black")
    
    # keep the scores
    canvas.create_text(app.width*0.25, app.height * 0.04, text = f"P1 Balls Remaining: {app.p1ballsRemaining}", fill = "black")
    canvas.create_text(app.width*0.75, app.height * 0.04, text = f"P2 Balls Remaining: {app.p2ballsRemaining}", fill = "black")

    #Keep Track of the game, if it ends, quit the game

    if app.gameLoses == True:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = pooltable, width = app.margin//2)
        canvas.create_text( app.width/2, app.height/2, text = "You Lose!", fill = black )
        canvas.create_text( app.width/2, app.height*0.7, text = "Press Space to Quit The Game!", fill = black )
    
    #Keep Track of the game, if it wins, quit the game
    if app.gameWins == True:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = pooltable, width = app.margin//2)
        if app.player % 2 == 0:
            canvas.create_text( app.width/2, app.height/2, text = "Player 2 Wins!", fill = black )
            canvas.create_text( app.width/2, app.height*0.7, text = "Press Space to Quit The Game!", fill = black )
        if app.player % 2 == 1:
            canvas.create_text( app.width/2, app.height/2, text = "Player 1 Wins!", fill = black )
            canvas.create_text( app.width/2, app.height*0.7, text = "Press Space to Quit The Game!", fill = black )
               
# Checks if ball has entered the pocket
def onePlayer_inThePocket(app):
    app.ballsCopy = copy.copy(app.balls)
    i = 0
    while i < len(app.balls):
    # check if the balls are in the six pockets
        if (
            distance(app.balls[i].cx, app.balls[i].cy, app.margin/2, app.margin/2 + 15) <= 25 or
            distance(app.balls[i].cx, app.balls[i].cy, app.margin/2, app.height - app.margin*1.5) <= 15 or
            distance(app.balls[i].cx, app.balls[i].cy, app.width/2, app.margin/2 + 15) <= 25 or
            distance(app.balls[i].cx, app.balls[i].cy, app.width/2, app.height - app.margin*1.5) <= 25 or
            distance(app.balls[i].cx, app.balls[i].cy, app.width - app.margin*1.5, app.margin/2 + 15) <= 15 or
            distance(app.balls[i].cx, app.balls[i].cy, app.width - app.margin*1.5, app.height - app.margin*1.5) <= 15
            ):
                # update the number of the balls
                if app.balls[i].num >= 0 and app.balls[i].num < 8:
                    app.p1ballsRemaining -= 1
                if app.balls[i].num > 8:
                    app.p2ballsRemaining -= 1
                app.sound[1].start()

                #check if the game ends
                if ((app.balls[i].num == 8 and app.p1ballsRemaining == 0) or (app.balls[i].num == 8 and app.p2ballsRemaining == 0)):
                    app.gameWins = True
                elif ((app.balls[i].num == 8 and app.p1ballsRemaining != 1) or (app.balls[i].num == 8 and app.p2ballsRemaining != 1)):
                    app.gameLoses = True       
                app.balls.pop(i)
        i += 1    

# Checks Collision
def onePlayer_collision(ball1, ball2):
    if distance(ball1.cx, ball1.cy, ball2.cx, ball2.cy) < 7*2:
        return True
    else:
        return False

# Checks if Cue Ball hits any Ball
def onePlayer_checkCueCollision(app):
    for i in range(len(app.balls)):
        if onePlayer_collision(app.cueBall, app.balls[i]):
            #if two balls overlap, split the two balls
            if app.balls[i].cx == app.cueBall.cx or app.balls[i].cy == app.cueBall.cy:
                app.balls[i].cx -= app.radius/4
                app.cueBall.cx += app.radius/4
            else:
                # collide 
                u1 = app.balls[i].speed
                u2 = app.cueBall.speed
                theta1 = radians(app.balls[i].angle)
                theta2 = radians(app.cueBall.angle)
                phi = atan((app.cueBall.cy - app.balls[i].cy) / (app.cueBall.cx - app.balls[i].cx))
                
                u1n = u1 * cos(theta1-phi)
                u2n = u2 * cos(theta2-phi)
                u1t = u1 * sin(theta1-phi)
                u2t = u2 * sin(theta2-phi)

                app.balls[i].speed = (u2n**2 + u1t**2)**0.5
                app.cueBall.speed = (u1n**2 + u2t**2)**0.5

                app.balls[i].angle = degrees(phi + atan(u1t/(u2n+0.00000001)))
                app.cueBall.angle = degrees(phi + atan(u2t/(u1n+0.00000001)))

                app.balls[i].cx += (app.balls[i].speed)*sin(radians(app.balls[i].angle))
                app.balls[i].cy -= (app.balls[i].speed)*cos(radians(app.balls[i].angle))
                app.cueBall.cx -= (app.cueBall.speed)*sin(radians(app.cueBall.angle))
                app.cueBall.cy += (app.cueBall.speed)*cos(radians(app.cueBall.angle))

                    

# Checks Collision Between Balls
def onePlayer_checkBallCollision(app):
    for i in range(len(app.balls)):
        for j in range(len(app.balls) - 1, i, -1):
            if onePlayer_collision(app.balls[i], app.balls[j]):
                #if two balls overlap, split the two balls
                if app.balls[i].cx == app.balls[j].cx or app.balls[i].cy == app.balls[j].cy:
                    app.balls[i].cx -= app.radius/4
                    app.balls[j].cx += app.radius/4
                else:
                    # collide 
                    u1 = app.balls[i].speed
                    u2 = app.balls[j].speed
                    theta1 = radians(app.balls[i].angle)
                    theta2 = radians(app.balls[j].angle)
                    phi = atan((app.balls[j].cy - app.balls[i].cy) / (app.balls[j].cx - app.balls[i].cx))
                    
                    u1n = u1 * cos(theta1-phi)
                    u2n = u2 * cos(theta2-phi)
                    u1t = u1 * sin(theta1-phi)
                    u2t = u2 * sin(theta2-phi)

                    app.balls[i].speed = (u2n**2 + u1t**2)**0.5
                    app.balls[j].speed = (u1n**2 + u2t**2)**0.5

                    app.balls[i].angle = degrees(phi + atan(u1t/(u2n+0.0000001)))
                    app.balls[j].angle = degrees(phi + atan(u2t/(u1n+0.0000001)))

                    app.balls[i].cx += (app.balls[i].speed)*sin(radians(app.balls[i].angle))
                    app.balls[i].cy -= (app.balls[i].speed)*cos(radians(app.balls[i].angle))
                    app.balls[j].cx -= (app.balls[j].speed)*sin(radians(app.balls[j].angle))
                    app.balls[j].cy += (app.balls[j].speed)*cos(radians(app.balls[j].angle))

def onePlayer_restart(app):
    # initialize the ball objects
    app.cueBall = Ball(width*0.7, height/2, 0, white, 0, "cue")
    app.balls = []

    b1 = Ball(80, height/2 - 4*radius, 0, colors[0], 0, 1)
    b2 = Ball(80 + 2*radius, height/2 - 3*radius, 0, colors[1], 0, 2)
    b3 = Ball(80, height/2 - 2*radius, 0, colors[2], 0, 3)
    b4 = Ball(80 + 4*radius, height/2 - 2*radius, 0, colors[3], 0, 4)
    b5 = Ball(80 + 2*radius, height/2 - 1*radius, 0, colors[4], 0, 5)
    b6 = Ball(80, height/2, 0, colors[5], 0, 6)
    b7 = Ball(80 + 6*radius, height/2 - 1*radius, 0, colors[6], 0, 7)
    b8 = Ball(80 + 4*radius, height/2, 0, colors[7], 0, 8)
    b9 = Ball(80 + 8*radius, height/2, 0, colors[8], 0, 9)
    b10 = Ball(80 + 6*radius, height/2 + 1*radius, 0, colors[9], 0, 10)
    b11 = Ball(80 + 2*radius, height/2 + 1*radius, 0, colors[10], 0, 11)
    b12 = Ball(80, height/2 + 2*radius, 0, colors[11], 0, 12)
    b13 = Ball(80 + 4*radius, height/2 + 2*radius, 0, colors[12], 0, 13)
    b14 = Ball(80 + 2*radius, height/2 + 3*radius, 0, colors[13], 0, 14)
    b15 = Ball(80, height/2 + 4*radius, 0, colors[14], 0, 15)

    app.balls.append(b1)
    app.balls.append(b2)
    app.balls.append(b3)
    app.balls.append(b4)
    app.balls.append(b5)
    app.balls.append(b6)
    app.balls.append(b7)
    app.balls.append(b8)
    app.balls.append(b9)
    app.balls.append(b10)
    app.balls.append(b11)
    app.balls.append(b12)
    app.balls.append(b13)
    app.balls.append(b14)
    app.balls.append(b15)

def onePlayer_startPockets(app):
    # initialize the ball objects
    app.pockets = []
    p1 = Pockets(app.margin/2, app.margin/2)
    p2 = Pockets(app.margin/2, app.height - app.margin*1.5)
    p3 = Pockets(app.width/2, app.margin/2)
    p4 = Pockets(app.width/2, app.height - app.margin*1.5)
    p5 = Pockets(app.width - app.margin*1.5, app.margin/2)
    p6 = Pockets(app.width - app.margin*1.5, app.height - app.margin*1.5)

    app.pockets.append(p1)
    app.pockets.append(p2)
    app.pockets.append(p3)
    app.pockets.append(p4)
    app.pockets.append(p5)
    app.pockets.append(p6)

def onePlayer_quit(app):
    app.quit()

# ---------------------------------------------------------------------
# Game AI 
# ---------------------------------------------------------------------

def onePlayer_generateCombinations():
    L = []
    # generate combinations from 359 degrees and 25 forces
    for degree in range(359):
        for force in range(1, 25, 1):
            L.append((force, degree))
    return L

def onePlayer_appendCombinations():
    L = onePlayer_generateCombinations()
    easy = []
    for i in range(100):
        i = (random.choice(L))
        easy.append(i)
    return easy

def onePlayer_undoMove(app):
    app.balls = copy.deepcopy(app.ballsCopy)
    # Copy the remaining balls
    app.p1ballsRemaining = copy.deepcopy(app.copyp1)
    app.p2ballsRemaining = copy.deepcopy(app.copyp2)
    app.player -= 1

def onePlayer_findMoveMiniMax(app):
    # Copy the balls
    app.ballsCopy = copy.deepcopy(app.balls)
    # Copy the remaining balls
    app.copyp1 = copy.deepcopy (app.p1ballsRemaining)
    app.copyp2 = copy.deepcopy (app.p2ballsRemaining)

    combinations = onePlayer_appendCombinations()
    bestForce = None
    bestDegree = None
    currScore = -30
    maxScore = -20
    
    for force, degree in combinations:
        app.cueBall.speed = force
        app.tangent = degree
        onePlayer_physics(app)

        #heuristics
        if app.copyp2 == app.p2ballsRemaining - 1 and app.copyp1 == app.p1ballsRemaining:
            currScore = 10
        elif app.copyp2 == app.p2ballsRemaining and app.copyp1 == app.p1ballsRemaining:
            currScore = 0
        elif app.copyp1 == app.p1ballsRemaining - 1 and app.copyp2 == app.p2ballsRemaining:
            currScore = -10
    
        if currScore > maxScore:
            maxScore = currScore
            bestForce = force
            bestDegree = degree
        
        onePlayer_undoMove(app)

    return bestForce, bestDegree

##########################################
# Two Player Mode
##########################################

#Reference: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def twoPlayer_resetApp(app):
    app.timerDelay = 75

def twoPlayer_appStarted(app):
    #initialize the variables
    app.margin = 30
    app.radius = 0.5*app.margin
    app.p1ballsRemaining = 7
    app.p2ballsRemaining = 7
    app.radius = 7
    app.clickx = None
    app.clicky = None
    app.startPosn = None
    app.endPosn = None
    app.force = 0
    app.length = 0
    app.tangent = 0
    app.player = 0
    app.l = 0
    app.gameWins = False
    app.gameLoses = False
    app.freeBall = False
    app.paused = False
    app.stop = True

    app.cueBall = Ball(width/2, height/2, 0, white, 0, "cue")
    
    twoPlayer_startPockets(app)
    twoPlayer_restart(app)
    twoPlayer_resetApp(app)

# Calculate the forces
def twoPlayer_mouseMoved(app, event):
    if app.freeBall == False:
        app.clickx = event.x
        app.clicky = event.y
        app.l = distance(app.cueBall.cx, app.cueBall.cy, app.clickx, app.clicky)/8
        if app.l > 25:
            app.l = 25
        if app.cueBall.speed == 0 and app.stop == True:
            app.tangent = (math.degrees(math.atan2((app.cueBall.cy - app.clicky), (app.cueBall.cx - app.clickx))))
        app.t = app.tangent
    
def twoPlayer_keyPressed(app, event):
    if (event.key == 'Space'):
        if app.gameLoses == True:
            twoPlayer_quit(app)
        if app.gameWins == True:
            twoPlayer_quit(app)
    elif (event.key == 'p'):    
        app.paused = not app.paused
    elif event.key == "h":
        app.mode = "helpMode"

def twoPlayer_ballStop(app):
    for i in app.balls:
        if i.speed != 0:
            app.stop = False
            continue
        else:
            app.stop = True

def twoPlayer_hitTheCue(app):
    if app.freeBall == False:
        app.cueBall.speed = app.force
        app.player += 1
        app.sound[0].start()
    
def twoPlayer_mousePressed(app, event):
    if app.freeBall == False:
        app.startPosn = [app.cueBall.cx, app.cueBall.cy]
        app.endPosn = [event.x, event.y]
        app.force = distance(app.startPosn[0] , app.startPosn[1], app.endPosn[0], app.endPosn[1])/ 8
        
        if app.force > 25:
            app.force = 25
        
        if app.cueBall.speed == 0 and app.stop == True:
            twoPlayer_hitTheCue(app)

def twoPlayer_cueBalltimerFired(app):
    # applies friction
    if app.cueBall.speed <= 0:
        app.cueBall.speed += 0.3
    if app.cueBall.speed >= 0:
        app.cueBall.speed -= 0.3
    if abs(app.cueBall.speed) <= 0.3:
        app.cueBall.speed = 0

    app.cueBall.cx += app.cueBall.speed*math.cos(math.radians(app.tangent))
    app.cueBall.cy += app.cueBall.speed*math.sin(math.radians(app.tangent))

#Reference: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#example:pong

    if (app.cueBall.cy + app.radius >= app.height - app.margin*1.2):
    # The ball went off the bottom!
        app.cueBall.cy = app.height - app.margin*1.2 - app.radius
        app.tangent = - app.tangent
    elif (app.cueBall.cy - app.radius <= app.margin*1.2):
    # The ball went off the up!
        app.cueBall.cy = app.margin*1.2 + app.radius
        app.tangent = - app.tangent
    if (app.cueBall.cx + app.radius >= app.width - app.margin*1.2):
    # The ball went off the right!
        app.cueBall.cx = app.width - app.margin*1.2 - app.radius
        app.tangent = 180 - app.tangent
    elif (app.cueBall.cx - app.radius <= app.margin*1.2):
    # The ball went off the left!
        app.cueBall.cx = app.margin*1.2 + app.radius
        app.tangent = 180 - app.tangent

def twoPlayer_ballsTimerFired(app):
    for i in range(len(app.balls)):
        app.balls[i].twoPlayer_timerFired(app)

# applies friction
def twoPlayer_physics(app):
    twoPlayer_cueBalltimerFired(app)
    twoPlayer_checkCueCollision(app)
    twoPlayer_checkBallCollision(app)
    twoPlayer_inThePocket(app)
    twoPlayer_ballsTimerFired(app)
    twoPlayer_ballStop(app)

def twoPlayer_timerFired(app):
    if app.paused == False:
        twoPlayer_physics(app)
        
def twoPlayer_drawPoolStick(app, canvas):
    if app.cueBall.speed == 0 and app.stop == True:
        if app.clicky != None and app.clickx != None:
            canvas.create_line(app.cueBall.cx + 75*math.cos(math.radians(app.tangent)), 
            app.cueBall.cy + 75*math.sin(math.radians(app.tangent)), app.cueBall.cx, app.cueBall.cy, fill = white, width = 1)
            canvas.create_line(app.clickx, app.clicky, app.cueBall.cx, app.cueBall.cy, fill = poolstick , width = 3)

def twoPlayer_redrawAll(app, canvas):
    # draw the pool table
    canvas.create_rectangle(app.margin, app.margin, app.width-app.margin, app.height - app.margin, 
    fill = pooltable, width = app.margin//2)

    canvas.create_line(app.width*0.7, app.margin*1.225, app.width*0.7, app.height - app.margin*1.225, fill = white, width = 0.3)
    #draw the balls
    for i in range(len(app.balls)):
            app.balls[i].twoPlayer_drawBall(canvas)
    #draw the pockets
    for i in range(6):
        app.pockets[i].twoPlayer_drawPocket(canvas)
    #draw the poolstick
    if app.freeBall == False:
        twoPlayer_drawPoolStick(app, canvas)
    #draw the cueBall
    app.cueBall.twoPlayer_drawBall(canvas)
    #indicate the player
    if app.player % 2 == 0:
        if app.cueBall.speed == 0 and app.stop == True:
            canvas.create_text(app.width*0.25, app.height * 0.96, text = "Player 1's Turn!", fill = "black")
    if app.player % 2 == 1:
        if app.cueBall.speed == 0 and app.stop == True:
            canvas.create_text(app.width*0.25, app.height * 0.96, text = "Player 2's Turn!", fill = "black")
    #indicate the force        
    if app.cueBall.speed == 0 and app.stop == True:
        canvas.create_text(app.width*0.75, app.height * 0.96, text = f"Force: {int(app.l)}", fill = "black")
    
    # keep the scores
    canvas.create_text(app.width*0.25, app.height * 0.04, text = f"P1 Balls Remaining: {app.p1ballsRemaining}", fill = "black")
    canvas.create_text(app.width*0.75, app.height * 0.04, text = f"P2 Balls Remaining: {app.p2ballsRemaining}", fill = "black")

    #Keep Track of the game, if it ends, quit the game
    if app.gameLoses == True:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = pooltable, width = app.margin//2)
        canvas.create_text( app.width/2, app.height/2, text = "You Lose!", fill = black )
        canvas.create_text( app.width/2, app.height*0.7, text = "Press Space to Quit The Game!", fill = black )
    #Keep Track of the game, if it wins, quit the game
    if app.gameWins == True:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = pooltable, width = app.margin//2)
        if app.player % 2 == 0:
            canvas.create_text( app.width/2, app.height/2, text = "Player 2 Wins!", fill = black )
            canvas.create_text( app.width/2, app.height*0.7, text = "Press Space to Quit The Game!", fill = black )
        if app.player % 2 == 1:
            canvas.create_text( app.width/2, app.height/2, text = "Player 1 Wins!", fill = black )
            canvas.create_text( app.width/2, app.height*0.7, text = "Press Space to Quit The Game!", fill = black )
               
# Checks if ball has entered the pocket
def twoPlayer_inThePocket(app):
    app.ballsCopy = copy.copy(app.balls)
    i = 0
    while i < len(app.balls):
    # check if the balls are in the six pockets
        if (
            distance(app.balls[i].cx, app.balls[i].cy, app.margin/2, app.margin/2 + 15) <= 25 or
            distance(app.balls[i].cx, app.balls[i].cy, app.margin/2, app.height - app.margin*1.5) <= 15 or
            distance(app.balls[i].cx, app.balls[i].cy, app.width/2, app.margin/2 + 15) <= 25 or
            distance(app.balls[i].cx, app.balls[i].cy, app.width/2, app.height - app.margin*1.5) <= 15 or
            distance(app.balls[i].cx, app.balls[i].cy, app.width - app.margin*1.5, app.margin/2 + 15) <= 25 or
            distance(app.balls[i].cx, app.balls[i].cy, app.width - app.margin*1.5, app.height - app.margin*1.5) <= 15
            ):
                # update the number of the balls
                if app.balls[i].num >= 0 and app.balls[i].num < 8:
                    app.p1ballsRemaining -= 1
                if app.balls[i].num > 8:
                    app.p2ballsRemaining -= 1
                app.sound[1].start()
                
                #check if the game ends
                if ((app.balls[i].num == 8 and app.p1ballsRemaining == 0) or (app.balls[i].num == 8 and app.p2ballsRemaining == 0)):
                    app.gameWins = True
                elif ((app.balls[i].num == 8 and app.p1ballsRemaining != 1) or (app.balls[i].num == 8 and app.p2ballsRemaining != 1)):
                    app.gameLoses = True
                
                app.balls.pop(i)       
        i += 1    

# Checks Collision
def twoPlayer_collision(ball1, ball2):
    if distance(ball1.cx, ball1.cy, ball2.cx, ball2.cy) < 7*2:
        return True
    else:
        return False

# Checks if Cue Ball hits any Ball
def twoPlayer_checkCueCollision(app):
    for i in range(len(app.balls)):
        if twoPlayer_collision(app.cueBall, app.balls[i]):
            #if two balls overlap, split the two balls
            if app.balls[i].cx == app.cueBall.cx or app.balls[i].cy == app.cueBall.cy:
                app.balls[i].cx -= app.radius/4
                app.cueBall.cx += app.radius/4
            else:
                # collide 
                u1 = app.balls[i].speed
                u2 = app.cueBall.speed
                theta1 = radians(app.balls[i].angle)
                theta2 = radians(app.cueBall.angle)
                phi = atan((app.cueBall.cy - app.balls[i].cy) / (app.cueBall.cx - app.balls[i].cx))
                
                u1n = u1 * cos(theta1-phi)
                u2n = u2 * cos(theta2-phi)
                u1t = u1 * sin(theta1-phi)
                u2t = u2 * sin(theta2-phi)

                app.balls[i].speed = (u2n**2 + u1t**2)**0.5
                app.cueBall.speed = (u1n**2 + u2t**2)**0.5

                app.balls[i].angle = degrees(phi + atan(u1t/(u2n+0.00000001)))
                app.cueBall.angle = degrees(phi + atan(u2t/(u1n+0.00000001)))

                app.balls[i].cx += (app.balls[i].speed)*sin(radians(app.balls[i].angle))
                app.balls[i].cy -= (app.balls[i].speed)*cos(radians(app.balls[i].angle))
                app.cueBall.cx -= (app.cueBall.speed)*sin(radians(app.cueBall.angle))
                app.cueBall.cy += (app.cueBall.speed)*cos(radians(app.cueBall.angle))

# Checks Collision Between Balls
def twoPlayer_checkBallCollision(app):
    for i in range(len(app.balls)):
        for j in range(len(app.balls)-1, i, -1):
            if twoPlayer_collision(app.balls[i], app.balls[j]):
                #if two balls overlap, split the two balls
                if app.balls[i].cx == app.balls[j].cx or app.balls[i].cy == app.balls[j].cy:
                    app.balls[i].cx -= app.radius/4
                    app.balls[j].cx += app.radius/4
                else:
                    # collide 
                    u1 = app.balls[i].speed
                    u2 = app.balls[j].speed
                    theta1 = radians(app.balls[i].angle)
                    theta2 = radians(app.balls[j].angle)
                    phi = atan((app.balls[j].cy - app.balls[i].cy) / (app.balls[j].cx - app.balls[i].cx))
                    
                    u1n = u1 * cos(theta1-phi)
                    u2n = u2 * cos(theta2-phi)
                    u1t = u1 * sin(theta1-phi)
                    u2t = u2 * sin(theta2-phi)

                    app.balls[i].speed = (u2n**2 + u1t**2)**0.5
                    app.balls[j].speed = (u1n**2 + u2t**2)**0.5

                    app.balls[i].angle = degrees(phi + atan(u1t/(u2n+0.0000001)))
                    app.balls[j].angle = degrees(phi + atan(u2t/(u1n+0.0000001)))

                    app.balls[i].cx += (app.balls[i].speed)*sin(radians(app.balls[i].angle))
                    app.balls[i].cy -= (app.balls[i].speed)*cos(radians(app.balls[i].angle))
                    app.balls[j].cx -= (app.balls[j].speed)*sin(radians(app.balls[j].angle))
                    app.balls[j].cy += (app.balls[j].speed)*cos(radians(app.balls[j].angle))

def twoPlayer_restart(app):
    # initialize the ball objects
    app.balls = []
    app.cueBall = Ball(width*0.7, height/2, 0, white, 0, "cue")

    b1 = Ball(80, height/2 - 4*radius, 0, colors[0], 0, 1)
    b2 = Ball(80 + 2*radius, height/2 - 3*radius, 0, colors[1], 0, 2)
    b3 = Ball(80, height/2 - 2*radius, 0, colors[2], 0, 3)
    b4 = Ball(80 + 4*radius, height/2 - 2*radius, 0, colors[3], 0, 4)
    b5 = Ball(80 + 2*radius, height/2 - 1*radius, 0, colors[4], 0, 5)
    b6 = Ball(80, height/2, 0, colors[5], 0, 6)
    b7 = Ball(80 + 6*radius, height/2 - 1*radius, 0, colors[6], 0, 7)
    b8 = Ball(80 + 4*radius, height/2, 0, colors[7], 0, 8)
    b9 = Ball(80 + 8*radius, height/2, 0, colors[8], 0, 9)
    b10 = Ball(80 + 6*radius, height/2 + 1*radius, 0, colors[9], 0, 10)
    b11 = Ball(80 + 2*radius, height/2 + 1*radius, 0, colors[10], 0, 11)
    b12 = Ball(80, height/2 + 2*radius, 0, colors[11], 0, 12)
    b13 = Ball(80 + 4*radius, height/2 + 2*radius, 0, colors[12], 0, 13)
    b14 = Ball(80 + 2*radius, height/2 + 3*radius, 0, colors[13], 0, 14)
    b15 = Ball(80, height/2 + 4*radius, 0, colors[14], 0, 15)

    app.balls.append(b1)
    app.balls.append(b2)
    app.balls.append(b3)
    app.balls.append(b4)
    app.balls.append(b5)
    app.balls.append(b6)
    app.balls.append(b7)
    app.balls.append(b8)
    app.balls.append(b9)
    app.balls.append(b10)
    app.balls.append(b11)
    app.balls.append(b12)
    app.balls.append(b13)
    app.balls.append(b14)
    app.balls.append(b15)

def twoPlayer_startPockets(app):
    # initialize the pocket objects
    app.pockets = []
    p1 = Pockets(app.margin/2, app.margin/2)
    p2 = Pockets(app.margin/2, app.height - app.margin*1.5)
    p3 = Pockets(app.width/2, app.margin/2)
    p4 = Pockets(app.width/2, app.height - app.margin*1.5)
    p5 = Pockets(app.width - app.margin*1.5, app.margin/2)
    p6 = Pockets(app.width - app.margin*1.5, app.height - app.margin*1.5)

    app.pockets.append(p1)
    app.pockets.append(p2)
    app.pockets.append(p3)
    app.pockets.append(p4)
    app.pockets.append(p5)
    app.pockets.append(p6)
    
def twoPlayer_quit(app):
    app.quit()

runApp(width = 660, height = 360)