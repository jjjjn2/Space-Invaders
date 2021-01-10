#Import Packages
import turtle
import os
import math
import random
import winsound
import playsound
from playsound import playsound

#Setup screen
wn = turtle.Screen()
wn.title("Space Invaders")
wn.bgcolor("Black")
wn.setup(width= 700, height= 700)
wn.bgpic("space_invaders_background.gif")
wn.tracer(0)

#Register shapes
wn.register_shape("player.gif")
wn.register_shape("invader.gif")

#Draw Border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range (4):
    border_pen.forward(600)
    border_pen.left(90)
border_pen.hideturtle()

#Set score to zero
score = 0

#Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: {}".format (score)
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

#Player
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 6



#Create the enemy
#Choose number of enemies
number_of_enemies = 30
#Creat an empty list
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
	#Create the enemy
	enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0	

for enemy in enemies:
	enemy.color("red")
	enemy.shape("invader.gif")
	enemy.penup()
	enemy.speed(0)
	x = enemy_start_x  + (50 * enemy_number)
	y = enemy_start_y 
	enemy.setposition(x, y)
	#Update th enemy number
	enemy_number += 1
	if enemy_number == 10:
		enemy_start_y -= 50
		enemy_number = 0

enemyspeed = 0.280

#Create player bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 8

#define bullet state
#ready - ready to fire
#fire - bullet is firing
bulletstate = "ready"


#Move the Player left and right [and up and down ( ͡° ͜ʖ ͡°)]
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = - 280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def move_foward():
    y = player.ycor()
    y += playerspeed
    if y > 280:
        y = 280
    player.sety(y)

def move_backwards():
    y = player.ycor()
    if y < -280:
        y = - 280
    y -= playerspeed
    player.sety(y)

def fire_bullet():
	#Declare bulletstate as a global if it needs changed
	global bulletstate 
	if bulletstate == "ready":
		winsound.PlaySound("laser.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
		bulletstate = "fire"
		#Move the bullet to just above the player
		x = player.xcor() 
		y = player.ycor() +10 
		bullet.setposition(x, y)
		bullet.showturtle()

def isCollision(t1, t2):
    distance =  t1.distance(t2)
    if distance < 15: 
        return True
    else:
        return False



#Keybinds (Player)
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_left, "a")
wn.onkeypress(move_right, "Right")
wn.onkeypress(move_right, "d")
wn.onkeypress(move_foward, "Up")
wn.onkeypress(move_foward, "w")
wn.onkeypress(move_backwards, "Down")
wn.onkeypress(move_backwards, "s")
wn.onkeypress(fire_bullet, "space")

#Main game loop
while True:
	
	wn.update()

	for enemy in enemies:
		#Move the enemy
		x = enemy.xcor()
		x += enemyspeed
		enemy.setx(x)

		#Move the enemy back and down
		if enemy.xcor() > 280:
			#Move all enemies down
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
			#Change enemy direction
			enemyspeed *= -1
		
		if enemy.xcor() < -280:
			#Move all enemies down
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
			#Change enemy direction
			enemyspeed *= -1
			
		#Check for a collision between the bullet and the enemy
		if isCollision(bullet, enemy):
			winsound.PlaySound("explosion.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
			#Reset the bullet
			bullet.hideturtle()
			bulletstate = "ready"
			bullet.setposition(0, -400)
			#Kill enemy 
			enemy.setposition(0, 10000000)
			#Update the score
			score += 10
			scorestring = "Score: {}".format (score)
			score_pen.clear()
			score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
		
		if isCollision(player, enemy):
			playsound('explosion.wav')
			player.hideturtle()
			enemy.hideturtle()
			print ("Game Over")
			break

		
	#Move the bullet
	if bulletstate == "fire":
		y = bullet.ycor()
		y += bulletspeed
		bullet.sety(y)
	
	#Check to see if the bullet has gone to the top
	if bullet.ycor() > 275:
		bullet.hideturtle()
		bulletstate = "ready"

