from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image as Image
import numpy as np
import random
import math
import collision

###Global variable declaration###
is_collide             = False
shooting_star          = False
explodeCount           =  0
collide_x, collide_y   = -90, 30
shooting_x, shooting_y = -90, -90
rx, ry                 = 1, 1
###---------------------------###

mat_emi_sun = [1.0, 0.1, 0.0, 0.0]

#texture mapping 
def load_texture(texture_url):
    img = Image.open(texture_url)
    img_data = np.array(list(img.getdata()), np.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID
    

def reshape(w, h):
    ratio = w / h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, ratio, 0.1, 3000) #시야각, 가로 종횡비, 최소, 최대거리

def stars():
    global LookAt_viewrPos_x
    global LookAt_viewrPos_z
    global LookAt_viewrDir_x
    global LookAt_viewrDir_z
    global Add_viewrPos_x
    global Add_viewrPos_z
    global Add_viewrDir_x
    global Add_viewrDir_z
    
    glPushMatrix()
    LookAt_viewrPos_x += Add_viewrPos_x / 10000
    LookAt_viewrDir_x += Add_viewrDir_x / 10000
    LookAt_viewrPos_z += Add_viewrPos_z / 10000
    LookAt_viewrDir_z += Add_viewrDir_z / 10000
    gluLookAt(LookAt_viewrPos_x, LookAt_viewrPos_y, LookAt_viewrPos_z,
            LookAt_viewrDir_x, LookAt_viewrDir_y, LookAt_viewrDir_z,
            0, 1, 0)
    
    glRotatef(angle_x/80, 0, 1, 0)
    glRotatef(angle_y/80, 0, 0, 1)
    
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_FRONT)
    #texture1 = load_texture("starmap.jpg")
    star = gluNewQuadric()
    gluQuadricTexture(star, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    #glBindTexture(GL_TEXTURE_2D, texture1)
    gluSphere(star, 800, 20, 20)
    gluDeleteQuadric(star)

    LookAt_viewrPos_x -= Add_viewrPos_x / 10000
    LookAt_viewrDir_x -= Add_viewrDir_x / 10000
    LookAt_viewrPos_z -= Add_viewrPos_z / 10000
    LookAt_viewrDir_z -= Add_viewrDir_z / 10000
    glPopMatrix()
    
def trace(radius, rotate, translate):
    for i in range(80):
        glPushMatrix()
        glRotatef(rotate-(radius/translate)*60-1.25*(i+1), 0, 1, 0)
        glTranslatef(translate, 0, 0)
        glDisable(GL_TEXTURE_2D)
        glColor4f(1.0, 1.0, 1.0, 1-(i+1)/20)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glEnable(GL_BLEND)
        glutSolidSphere(0.2, 10, 10)
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glPopMatrix()

def random_track():
    x = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
    y = [1, 2, 3, 4, 5]
    num1 = random.randint(0,9)
    num2 = random.randint(0,4)
    return x[num1], y[num2]

        
#rotaion y축 기준
def rotation(angle):
    rotation = np.eye(4)
    angle = angle * math.pi / 180
    rotation[0, 0] = math.cos(angle)
    rotation[2, 0] = math.sin(angle)
    rotation[0, 2] = - math.sin(angle)
    rotation[2, 2] = math.cos(angle)
    return (rotation)

def translation(x, y, z):
    translation = np.eye(4)
    translation[3, 0] = x
    translation[3, 1] = y
    translation[3, 2] = z
    return (translation)

def drawPlanet():
    global planet_center
    planet_center = [np.array([0, 0, 0, 1])] * 10
    planet = gluNewQuadric()
    gluQuadricTexture(planet, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glPushMatrix()
    
    if planet_exist[0]:
        glPushMatrix() #태양
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emi_sun)
        glRotatef(revolutionEarth_y, 0, 1, 0)
        glTranslatef(0, 0, 0)
        glRotatef(revolutionEarth_y, 0, 1, 0) 
        planet_center[0] = planet_center[0] @ translation(0, 0, 0) @ rotation(revolutionEarth_y) 
        #texture1 = load_texture("sunmap_low.jpg")
        #glBindTexture(GL_TEXTURE_2D, texture1)
        gluSphere(planet, 12, 20, 20)
        glPopMatrix()    
    
    if planet_exist[1]:
        glPushMatrix() #수성
        #자취
        trace(1.14, revolutionEarth_y, 24)
        #수성
        glRotatef(revolutionEarth_y, 0, 1, 0)
        glTranslatef(24, 0, 0)
        glRotatef(rotationEarth_y, 0, 1, 0)   
        planet_center[1] = planet_center[1] @ translation(24, 0, 0) @ rotation(revolutionEarth_y) 
        #texture1 = load_texture("mercurymap_low.jpg")
        #glBindTexture(GL_TEXTURE_2D, texture1)
        gluSphere(planet, 1.14, 20, 20)
        glPopMatrix()
    '''
    glPushMatrix()
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(list(planet_center[1])[0],list(planet_center[1])[1],list(planet_center[1])[2])
    glVertex3f(list(planet_center[1])[0]+100,list(planet_center[1])[1]+100,list(planet_center[1])[2]+100)
    glEnd()
    glColor3f(1,1.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(list(planet_center[1])[0],list(planet_center[1])[1],list(planet_center[1])[2])
    glVertex3f(list(planet_center[1])[0]-100,list(planet_center[1])[1]+100,list(planet_center[1])[2]+100)
    glEnd()
    glPopMatrix()
    '''
    if planet_exist[2]:
        glPushMatrix() #금성
        trace(2.85, revolutionEarth_y * (1/0.61), 42)
        glRotatef(revolutionEarth_y * (1/0.61), 0, 1, 0) 
        glTranslatef(42, 0, 0) #B x cnrdmfh 30
        glRotatef(rotationEarth_y, 0, 1, 0) #B 자전 7.0
        planet_center[2] = planet_center[2] @ translation(42, 0, 0) @ rotation(revolutionEarth_y) 
        #texture1 = load_texture("venusmap_low.jpg")
        gluSphere(planet, 2.85, 20, 20)
        glPopMatrix()
    
    
    if planet_exist[3]:
        glPushMatrix() #지구
        trace(3, revolutionEarth_y, 60)
        glRotatef(revolutionEarth_y, 0, 1, 0) 
        glTranslatef(60, 0, 0) #x 축으로
        glPushMatrix() #지구
        glRotatef(rotationEarth_y, 0, 1, 0) 
        planet_center[3] = planet_center[3] @ translation(60, 0, 0) @ rotation(revolutionEarth_y) 
        #texture1 = load_texture("earthmap_low.jpg")
        gluSphere(planet, 3, 20, 20)
        glPopMatrix()
        
        if planet_exist[4]:
            glPushMatrix() #달
            trace(1, revolutionEarth_y, 5)
            glRotatef(revolutionEarth_y, 0, 1, 0)
            glTranslatef(5, 0, 0)
            glRotatef(rotationEarth_y, 0, 1, 0) 
            planet_center[4] = planet_center[4] @ translation(5, 0, 0) @ rotation(revolutionEarth_y) 
            planet_center[4] = planet_center[4] @ translation(60, 0, 0) @ rotation(revolutionEarth_y) 
            #texture1 = load_texture("moonmap_low.jpg")
            gluSphere(planet, 1, 20, 20)
            glPopMatrix()
        glPopMatrix()
    

    if planet_exist[5]:
        glPushMatrix() #화성
        trace(1.59, revolutionEarth_y * (1/1.9), 80)
        glRotatef(revolutionEarth_y * (1/1.9), 0, 1, 0) 
        glTranslatef(80, 0, 0)
        glRotatef(rotationEarth_y, 0, 1, 0)
        planet_center[5] = planet_center[5] @ translation(80, 0, 0) @ rotation(revolutionEarth_y) 
        #texture1 = load_texture("marsmap_low.jpg")
        gluSphere(planet, 1.59, 20, 20)
        glPopMatrix()


    if planet_exist[6]:
        glPushMatrix() #목성
        trace(9, revolutionEarth_y * (1 / 29.5), 120)
        glRotatef(revolutionEarth_y * (1 / 29.5), 0, 1, 0)
        glTranslatef(120, 0, 0)
        glRotatef(rotationEarth_y, 0, 1, 0)
        planet_center[6] = planet_center[6] @ translation(120, 0, 0) @ rotation(revolutionEarth_y) 
        #texture1 = load_texture("jupitermap_low.jpg")
        gluSphere(planet, 9, 20, 20)
        glPopMatrix()
    
    
    if planet_exist[7]:
        glPushMatrix() #토성
        trace(7.5, revolutionEarth_y * (1/11.9), 150)
        glRotatef(revolutionEarth_y * (1/11.9), 0, 1, 0)
        glTranslatef(150, 0, 0) 
        glRotatef(27, 1, 0, 0)
        glRotatef(rotationEarth_y, 0, 1, 0)
        planet_center[7] = planet_center[7] @ translation(150, 0, 0) @ rotation(revolutionEarth_y) 
        #texture1 = load_texture("saturnmap_low.jpg")
        gluSphere(planet, 7.5, 20, 20)
        glPopMatrix()

            
    if planet_exist[8]:     
        glPushMatrix() #천왕성
        trace(3.75, revolutionEarth_y * (1 / 1.5), 162)
        glRotatef(revolutionEarth_y * (1 / 1.5), 0, 1, 0)
        glTranslatef(162, 0, 0)
        glRotatef(rotationEarth_y, 0, 1, 0)
        planet_center[8] = planet_center[8] @ translation(162, 0, 0) @ rotation(revolutionEarth_y) 
        #texture1 = load_texture("neptunemap_low.jpg")
        gluSphere(planet, 3.75, 20, 20)
        glPopMatrix()
            
    
    if planet_exist[9]:
        glPushMatrix() #해왕성
        trace(3.75, revolutionEarth_y * (1 / 1.2), 180)
        glRotatef(revolutionEarth_y * (1 / 1.2), 0, 1, 0)
        glTranslatef(180, 0, 0)
        glRotatef(rotationEarth_y, 0, 1, 0)
        planet_center[9] = planet_center[9] @ translation(180, 0, 0) @ rotation(revolutionEarth_y) 
        #texture1 = load_texture("neptunemap_low.jpg")
        gluSphere(planet, 3.75, 20, 20)
        glPopMatrix()
    
    glPopMatrix()
    gluDeleteQuadric(planet)
    
def create_planet(new_center_x, new_center_y, new_center_z):
    global speed
    glPushMatrix()
    planet = gluNewQuadric()
    gluQuadricTexture(planet, GL_TRUE)
    glEnable(GL_TEXTURE_2D)
    glRotatef(rotationEarth_y + speed, 0, 1, 0)
    glTranslatef(new_center_x, new_center_y, new_center_z)
    #texture1 = load_texture("newmap.jpg")
    gluSphere(planet, 5, 20, 20)
    #print(new_center_x)
    #print(new_center_y)
    gluDeleteQuadric(planet)
    glPopMatrix()
    
def check_crash(new_center_x, new_center_y, new_center_z, planet_coor):
    global planet_center
    planet_x = planet_coor[0]
    planet_y = planet_coor[1]
    planet_z = planet_coor[2]
    if ((new_center_x - planet_x)**2 + (new_center_y - planet_y)**2 + (new_center_z - planet_z)**2) > 80:
        return True
    else:
        return False
    
def display():
    global LookAt_viewrPos_x, LookAt_viewrPos_z
    global LookAt_viewrDir_x, LookAt_viewrDir_z
    global Add_viewrPos_x, Add_viewrPos_z
    global Add_viewrDir_x, Add_viewrDir_z
    global revolutionEarth_y
    global rotationEarth_y
    global angle_x, angle_y
    global new_center_x, new_center_y, new_center_z
    global new_center_x_des, new_center_y_des, new_center_z_des
    global exist_new
    global explodeCount
    global is_collide
    global shooting_star
    global collide_x, collide_y
    global shooting_x, shooting_y
    global rx, ry
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.8, 0.5, 0.8)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    #background
    #stars()

    #방향키를 움직이면 카메라의 위치와 방향을 바뀜
    LookAt_viewrPos_x += Add_viewrPos_x*5
    LookAt_viewrDir_x += Add_viewrDir_x*5
    LookAt_viewrPos_z += Add_viewrPos_z*5
    LookAt_viewrDir_z += Add_viewrDir_z*5
    gluLookAt(LookAt_viewrPos_x, LookAt_viewrPos_y, LookAt_viewrPos_z,
            LookAt_viewrDir_x, LookAt_viewrDir_y, LookAt_viewrDir_z,
            0, -1, 0)
    Add_viewrPos_x = 0
    Add_viewrPos_z = 0
    Add_viewrDir_x = 0
    Add_viewrDir_z = 0
    
    glScalef(2, 2, 2)
    
    #background
    
    #마우스 수평이동: 태양 y축 기준으로 회전
    glRotatef(angle_x, 0, 1, 0)
    #마우스 수직이동: 태양 z축 기준으로 회전
    glRotatef(angle_y, 0, 0, 1)
    
    revolutionEarth_y += 2 
    rotationEarth_y += 3
    drawPlanet()
    
    x_move = (new_center_x_des - new_center_x)/10
    y_move = (new_center_y_des - new_center_y)/10
    z_move = (new_center_z_des - new_center_z)/10
    if (((new_center_x - new_center_x_des)**2 + (new_center_y - new_center_y_des)**2 + (new_center_z - new_center_z_des)**2)> 20):
        new_center_x += x_move
        new_center_y += y_move
        new_center_z += z_move
    
    
    if exist_new:
        create_planet(new_center_x, new_center_y, new_center_z)
    
    for planet in range(9):
        if check_crash(new_center_x, new_center_y, new_center_z, planet_center[planet]) is not True:
            is_collide = True
            collide_x, collide_y = (new_center_x + planet_center[planet][0])/2, (new_center_y + planet_center[planet][1])/2
            planet_exist[planet] = False
            exist_new = False
            #print("planet_exist: ", planet_exist[planet])
            
    if is_collide:  # 충돌이 일어날 때 효과 나타남
        print("collid")
        collision.collide_or_sstar(0)
        collision.change_explodeCount(10)
        collision.change_maxAge(60)
        particledebris = collision.ParticleDebris(collide_x, collide_y, 0.1, 0.1, 0.0, 0.0)
        if(explodeCount < 40):
            collision.particleList.append(particledebris)    # 입자 리스트에 폭발 시작 지점 입자 추가
        
        collid = collision.ParticleSystem()
        collid.update()     # 입자 state 업데이트
        explodeCount += 1   

        if explodeCount >= 100:
            is_collide = False
            explodeCount = 0            

    if shooting_star:
        print("Shooting star!")
        collision.collide_or_sstar(1)
        collision.change_explodeCount(60)
        collision.change_maxAge(30)
        particledebris = collision.ParticleDebris(shooting_x, shooting_y, 0.2, 0.2, 0.1*rx, 0.1*ry)
        if(explodeCount < 200):
            collision.particleList.append(particledebris)    # 입자 리스트에 폭발 시작 지점 입자 추가
        
        collid = collision.ParticleSystem()
        collid.update()     # 입자 state 업데이트
        explodeCount += 1   
        if rx==ry:
            shooting_x += rx
            shooting_y += ry
        else:
            shooting_x += rx*0.5
            shooting_y += ry*0.5

        if explodeCount >= 250:
            rx, ry = random_track()
            shooting_star = False
            explodeCount = 0
            shooting_x, shooting_y = -90, -90

    glutSwapBuffers()



def spckeycallback(key, x, y):
    global Add_viewrPos_x
    global Add_viewrPos_z
    global Add_viewrDir_x
    global Add_viewrDir_z

    if key == 100:
        Add_viewrPos_x = -10.0
        Add_viewrDir_x = -10.0
    
    if key == 102: 
        Add_viewrPos_x = 10.0
        Add_viewrDir_x = 10.0
    
    if key == 103: #앞쪽이동
        Add_viewrPos_z = 10.0
        Add_viewrDir_z = 10.0
    
    if key == 101: #뒤쪽이동
        Add_viewrPos_z = -10.0
        Add_viewrDir_z = -10.0
       
       
def keyboard(key, x, y): 
    global angle_x
    global angle_y
    global new_center_x_des
    global new_center_y_des
    global new_center_z_des
    global speed
    global is_collide
    global shooting_star
    
    if key == b'd':
        angle_x = 0
        angle_y = 0
        
    if key == b'a':
        new_center_x_des, new_center_y_des, new_center_z_des = input("INPUT CENTER(x, y, z): ").split()
        new_center_x_des = int(new_center_x_des)
        new_center_y_des = int(new_center_y_des)
        new_center_z_des = int(new_center_z_des)
    
    if key == b'w':
        speed = 5
    
    if key == b' ':
        is_collide = True

    if key == b's':
        shooting_star = True


def mouse(button, state, x, y):
    #print("button: ", button)
    #print("state: ", state)
    #print("state: ", state)
    #global button_
    #global state_
    global mouse_init_x
    global mouse_init_y
    global new_center_x
    global new_center_y
        
    mouse_init_x = x     
    mouse_init_y = y 
    #button_ = button
    #state_ = state
    '''
    if (button_ == 2 and state_ == 0):
        new_center_x = 1/400*mouse_init_x - 1 
        new_center_y = -1/400*mouse_init_y + 1
    print("cew: ", new_center_x)
    print(mouse_init_x)
    '''

def motion(x, y):
    #global button_
    #global state_
    global angle_x
    global angle_y
    global mouse_init_x
    global mouse_init_y
        
        
    #if (button_ == 0 and state_ == 0):
    angle_x += (x - mouse_init_x) * 0.1
    angle_y += (mouse_init_y - y) * 0.1
        #mouse_init_x = x     
        #mouse_init_y = y 

if __name__ == "__main__":
    Add_viewrPos_x = 0
    Add_viewrPos_z = 0
    Add_viewrDir_x = 0
    Add_viewrDir_z = 0
    revolutionEarth_y = 1.0 #초기화
    rotationEarth_y = 7.0
    LookAt_viewrPos_x = 10
    LookAt_viewrPos_y = 40
    LookAt_viewrPos_z = 500
    LookAt_viewrDir_x = 0
    LookAt_viewrDir_y = 0.3
    LookAt_viewrDir_z = 0
    angle_x = 0
    angle_y = 0
    new_center_x = 500
    new_center_y = 0
    new_center_z = 0
    new_center_x_des = new_center_x
    new_center_y_des = new_center_y
    new_center_z_des = new_center_z
    #수, 금, 지, 달, 화, 목, 토, 천, 해
    planet_center = [np.array([0, 0, 0, 1])] * 10
    planet_exist = [True] * 10
    exist_new = True
    stop = False
    speed = 0

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(1600, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Solar System")

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(spckeycallback)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutReshapeFunc(reshape) #창의 크기가 변할 때 실행

    glutMainLoop()

