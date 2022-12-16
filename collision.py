# ref: https://github.com/bronzelion/fireworks_simulator
# global declaration

gravity           =   9.8
dragFactor        =   10
windX             =   0.01
windY             =   0
maxAge            =   60	# 입자 나이. 줄어들수록 작고 빠르게 터지는것처럼 보이고 늘어날수록 크고 느리게 터지는것처럼 보임
launchSpeed       =   10
launchVariation   =   50
launchIterval     =   30
explosionSpeed    =   2
explosionVariation=   5
explodeCount      =   10
launchColor       =   [1.0,1.0,1.0,1.0]
launchSize        =   1
particleSize      =   1
initPosX          =   200	# 현재 스페이스 바 누르면 두 군데에서 폭발이 일어날텐데, 그 중 사용자기준 오른쪽에 있는 폭발. 아마 초기값으로 설정된 것 같네요
initPosY          =   200

#!/usr/bin/python
import random
import math

from OpenGL.GL import *
from OpenGL.GLUT import *

'''
class Utils():
	Utilitiy Class for repeated function calls
	Loads the config for sim from config.json
	
	def __init__(self):
		try:
			fp = open('./config.json')
			self.params = json.load(fp)
		except:
			logging.exception("Unable to load the config file")

	@property
	def config(self):
		return self.params

	@staticmethod
	def getRadians(x):
		return math.pi/180.0 * x

	@staticmethod
	def getRandomColor():
		color = [1.0]				#Alpha channel
		for i in range(3):
			color.insert(0,random.random())	
		return  color
'''

def getRadians(x):
	return math.pi/180.0 * x

def getRandomColor():
		color = [1.0]				#Alpha channel
		for i in range(3):
			color.insert(0,random.random())	
		return  color

# Place holder for all particles in the system
# Made this global, as it needs access across
particleList = []
#utils = Utils()
#params = utils.config


class Particle(object):
	'''Main Particle class, contains all attributes for a particle'''
	def __init__(self,x,y,vx,vy,color,size):
		#super(Particle, self).__init__()		
		self.x = x			#Position
		self.y = y		
		self.vx = vx		#velocity in *-direction
		self.vy = vy

		self.age= 0			#Current age of the particle
		self.max_age=maxAge	#Maximum age of the particle

		self.size = size	#Size of particle
		
		self.color=color	#Color
		self.is_dead = False	# Check if it is "dead"

	def update(self,dx=0.05,dy=0.05):
		#print("updating particle in list")
		self.vx += dx	# update dx, dy
		self.vy += dy

		#self.vx *= 1- dragFactor/1000	#공기저항같은건데 별로 중요하진 않습니다 주석처리하셔도 영향 없어요
		#self.vy *= 1- dragFactor/1000

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
		#self.is_dead = (self.age >= self.max_age)	

		#Start ageing
		# Achieve a linear color falloff(ramp) based on age.
		self.color[3]= 1.0 - float(self.age)/float(self.max_age)	# 시간이 지날수록 색이 점점 어두워집니다

class ParticleBurst(Particle):	
	def __init__(self,x,y,vx,vy):
		#print("initializing particle burst")
		color = launchColor
		size = launchSize		
		Particle.__init__(self,x,y,vx,vy,color,size)
		self.wind=1		

	def explode(self):	# IMPORTANT
		#pick random burst color
		global explodeCount
		color = getRandomColor()	
		explodeCount = explodeCount	# 40, 한번 폭발 시 그려지는 입자 개수

		for i in range(explodeCount):
			angle = getRadians(random.randint(0,360))		# 입자가 나가는 방향 랜덤으로	
			speed = explosionSpeed * (1 -random.random())	# 입자 퍼지는 속도 랜덤으로
			vx = math.cos(angle)*speed						# x 방향 속도
			vy = -math.sin(angle)*speed						# y 방향 속도
			x  = self.x + vx
			y  = self.y + vy
			# Create Fireworks particles
			obj = Particle(x,y,vx,vy,color,particleSize)	# 해당 입자 클라스 생성
			particleList.append(obj)						# 입자 리스트에 입자 클라스 append

	# Override parent method for Exploder particle
	def check_particle_age(self):	# 원래 불꽃놀이면 그 처음 불꽃 나타내는 함수같은데 저희 시뮬레이터에 그렇게 필요할 것 같진 않네요
		
		if self.vy != 0:
			self.age += 1
		#if self.vy <0:
		#	self.age += 1

		# Tweaking explode time
		temp = int ( 100*  random.random()) + explosionVariation
		#print("check particle age", self.age, temp)
		
		if self.age > temp:
			self.is_dead = True			
			self.explode()
		self.color[3]= 1.0 - float(self.age)/float(self.max_age)
                                                           
class ParticleSystem():
	'''Container class for the Simulation.
	Takes care to add Exploders at a given interval
	'''
	def __init__(self):		
		self.x = initPosX
		self.y = initPosY
		self.timer = 0
		#self.addExploder()
		#self.explode()

	def addExploder(self):
		speed = explosionSpeed	# 5
		speed *= (1 - random.uniform(0,explosionVariation)/100)
		angle = 270*3.14/180 + round(random.uniform(-0.5,0.5),2)
		vx = speed * math.cos(angle) 
		vy = -speed * math.sin(angle)
		
		f = ParticleBurst(30,10,vx,vy )			
		particleList.append(f)

	def update(self):
		# Clock to launch fireworks,
		#print("ParticleSystem.update")
		interval = launchIterval	# 30 time
		self.timer += 1

		#if self.timer % interval == 0 or self.timer < 2:	
			#print("add Exploder")	
			#self.addExploder()
		
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
