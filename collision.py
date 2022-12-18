# ref: https://github.com/bronzelion/fireworks_simulator
# global declaration

accelerate        =   1.5
windX             =   0.0
windY             =   0.0
maxAge            =   60
explosionSpeed    =   2
explosionVariation=   5
explodeCount      =   10
originalColor     =   [1.0,1.0,0.0,1.0]
originalSize      =   1
particleSize      =   1
initPosX          =   0
initPosY          =   0
collide_sstar     =   True

import random
import math

from OpenGL.GL import *
from OpenGL.GLUT import *


def getRadians(x):
	return math.pi/180.0 * x

def getRandomColor():
		color = [1.0]
		for i in range(3):
			color.insert(0,random.random())	
		return color

def getFlameColor():
		color = [1.0, 0.0, 0.0, 1.0]
		for i in range(3):
			color[1] = random.random()
		return color

def collide_or_sstar(type):
	global collide_sstar
	if type == 0:	# Collision
		collide_sstar = True
	else:			# Shooting star
		collide_sstar = False

def change_explodeCount(num):
	global explodeCount
	explodeCount = num

def change_maxAge(num):
	global maxAge
	maxAge = num

# list for all particles in the system
particleList = []


class Particle(object):
	'''Main Particle class, contains all attributes for a particle'''
	def __init__(self,x,y,vx,vy,ax,ay,color,size):
		self.x = x			#Position
		self.y = y		
		self.vx = vx		#velocity in *-direction
		self.vy = vy
		self.ax = ax
		self.ay = ay

		self.age= 0			#Current age of the particle
		self.max_age=maxAge	#Maximum age of the particle

		self.size = size	#Size of particle
		
		self.color=color	#Color
		self.is_dead = False	# Check if it is "dead"

	def update(self,dx=0.05,dy=0.05):
		#print("updating particle in list")
		self.vx += dx - self.ax*accelerate	# update dx, dy
		self.vy += dy - self.ay*accelerate

		self.x += self.vx	# update x, y
		self.y += self.vy
		self.check_particle_age()	# update particle age

	def draw(self):
		#print "x: %s Y: %s" %(self.x,self.y) 
		#gluSphere()
		glColor4fv(self.color)
		glPushMatrix()
		glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [1.0, 1.0, 0.0, 0.0])
		glTranslatef(self.x,self.y,0)
		glutSolidSphere(self.size,20,20)
		#glutSolidCube(1.5)
		glPopMatrix()
		glutPostRedisplay()	# modify

	def check_particle_age(self):		
		self.age +=1 
		if self.age >= self.max_age:
			self.is_dead = True
		else:
			self.is_dead = False

		#Start ageing
		# Achieve a linear color falloff(ramp) based on age.
		self.color[3]= 1.0 - float(self.age)/float(self.max_age)	# 시간이 지날수록 색이 점점 어두워집니다

class ParticleDebris(Particle):	
	def __init__(self,x,y,vx,vy,ax,ay):
		#print("initializing particle burst")
		color = originalColor
		size = originalSize		
		Particle.__init__(self,x,y,vx,vy,ax,ay,color,size)

	def explode(self):	# IMPORTANT
		#pick random burst color
		global explodeCount
		if collide_sstar:
			color = getRandomColor()	
		else:
			color = getFlameColor()
		explodeCount = explodeCount	# 40, 한번 폭발 시 그려지는 입자 개수

		for i in range(explodeCount):
			angle = getRadians(random.randint(0,360))		# 입자가 나가는 방향 랜덤으로	
			speed = explosionSpeed * (1 -random.random())	# 입자 퍼지는 속도 랜덤으로
			vx = math.cos(angle)*speed						# x 방향 속도
			vy = -math.sin(angle)*speed						# y 방향 속도
			x  = self.x + vx
			y  = self.y + vy
			# Create Fireworks particles
			obj = Particle(x,y,vx,vy,self.ax,self.ay,color,particleSize)	# 해당 입자 클라스 생성
			particleList.append(obj)						# 입자 리스트에 입자 클라스 append

	def check_particle_age(self):
		
		self.age += 1

		temp = int ( 100 * random.random()) + explosionVariation
		#print("check particle age", self.age, temp)
		
		if self.age > temp:
			self.is_dead = True			
			self.explode()
		self.color[3]= 1.0 - float(self.age)/float(self.max_age)
                                                           
class ParticleSystem():
	def __init__(self):		
		self.x = initPosX
		self.y = initPosY
		self.timer = 0

	def update(self):
		#print("ParticleSystem.update")
		self.timer += 1
		
		for i in range(len(particleList)-1,0,-1): # particle index가 1씩 줄어들 때
			#print("particle number:", i)
			p = particleList[i]
			x = windX
			y = windY			
			p.update(x,y)
			p.check_particle_age()			
			if p.is_dead:		
				#print("particle dead")			
				p.color = [0.0,0.0,0.0,0.0]				
				particleList.pop(i)				
			else:
				#print("draw particle")
				p.draw()
