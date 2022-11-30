from ast import Global
from tokenize import Double
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pygame
from pygame.locals import *
import sys


#속도조절 막대
#마우스가 존재하는 위치에서 줌인
#궤도 일정 시간동안
#태양 중심 rotation

mat_amb = [0.1, 0.1, 0.1, 0.1]  #주변광에 대한 반사값
mat_dif = [0.6, 0.2, 0.6, 0.0]  #분산광에 대한 반사값
mat_spc = [0.8, 0.2, 0.8, 0.5]  #반사광에 대한 반사값
mat_emi = [0.1, 0.1, 0.0, 0.0]  #발광값
mat_shi = [100.0, 0.0]  #광택

mat_emi_sun = [1.0, 0.1, 0.0, 0.0]  #태양 발광값
mat_emi_other = [0.0, 0.0, 0.0, 0.0]  #태양 이외의 emission값
mat_dif_sun = [0.4, 0.1, 0.3, 0.0]  #태양 분산광에 대한 반사값
mat_dif_mercury = [0.2, 0.1, 0.7, 0.0]  #수성 분산광에 대한 반사값
mat_dif_venus = [0.5, 0.1, 0.2, 0.0]  #금성 분산광에 대한 반사값
mat_dif_earth = [0.2, 0.4, 0.2, 0.0]  #지구 분산광에 대한 반사값
mat_dif_mars = [0.8, 0.4, 0.2, 0.0]  #화성 분산광에 대한 반사값
mat_dif_jupiter = [0.1, 0.2, 0.7, 0.0]  #목성 분산광에 대한 반사값
mat_dif_saturn = [0.8, 0.5, 0.5, 0.0]  #토성 분산광에 대한 반사값
mat_dif_uranus = [0.5, 0.2, 0.7, 0.0]  #천왕성 분산광에 대한 반사값
mat_dif_neptune = [0.1, 0.1, 0.8, 0.0]  #혜왕성 분산광에 대한 반사값


#texture mapping 임시
def load_texture(texture_url):
    tex_id = glGenTextures(1)
    tex = pygame.image.load(texture_url)
    tex_surface = pygame.image.tostring(tex, 'RGBA')
    tex_width, tex_height = tex.get_size()
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width, tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_surface)
    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id

#광원 초기화
def light():
    glEnable(GL_LIGHTING) #OpenGL 자체의 전체 조명 기능을 켜고
    glEnable(GL_DEPTH_TEST)

    lit_amb = [1.0, 1.0, 1.0, 0.0] #주변광의 강도
    lit_dif = [1.0, 1.0, 1.0, 0.0] #분산광의 강도
    lit_spc = [1.0, 1.0, 1.0, 0.0] #반사광의 강도
    lit_pos = [0.0, 0.0, 0.0, 1.0] #광원(태양)의 위치

    glLightfv(GL_LIGHT0, GL_AMBIENT, lit_amb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lit_dif)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lit_spc)
    glLightfv(GL_LIGHT0, GL_POSITION, lit_pos)
    glEnable(GL_LIGHT0) #태양의 조명 설정


def reshape(w, h):
    ratio = w / h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, ratio, 0.1, 1000) #시야각, 가로 종횡비, 최소, 최대거리



def drawPlanet():
    #재질세팅
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_amb) #앞면과 뒷면 모두
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_spc)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shi)
    
    glPushMatrix()
    
    glPushMatrix() #태양
    #재질 특성 설정
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emi_sun)
    glRotatef(revolutionEarth_y, 0, 1, 0) #B의 공전 3.0
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glRotatef(revolutionEarth_y, 0, 1, 0) #A의 자전 3.0
    texture = load_texture("sunmap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture)
    #gluSphere(sphere, 10., 20, 20)
    glutSolidSphere(30, 20, 20)
    glPopMatrix()
    glPopMatrix()


    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emi_other)
    
    
    glPushMatrix() #수성
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_mercury)
    glRotatef(revolutionEarth_y, 0, 1, 0) #B 자전 7.0
    glPushMatrix()
    glTranslatef(40, 0, 0)
    glRotatef(rotationEarth_y, 0, 1, 0)    
    texture = load_texture("mercurymap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture)         
    #gluSphere(sphere, 3.0, 20, 20)
    glutSolidSphere(1.2, 20, 20)
    glPopMatrix()
    glPopMatrix()
    
    
    glPushMatrix() #금성
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_venus)
    glRotatef(revolutionEarth_y * (1/0.61), 0, 1, 0) #B의 공전 3.0
    glPushMatrix() 
    glTranslatef(70, 0, 0) #B x cnrdmfh 30
    glRotatef(rotationEarth_y, 0, 1, 0) #B 자전 7.0
    texture = load_texture("venusmap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture)  
    #gluSphere(sphere, 3.0, 20, 20)
    glutSolidSphere(2.7, 20, 20)
    glPopMatrix()
    glPopMatrix()
    
    
    glPushMatrix() #지구, 달
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_earth)
    glRotatef(revolutionEarth_y, 0, 1, 0) #B의 공전 3.0
    glTranslatef(100, 0, 0) #x 축으로

    glPushMatrix() #지구
    glRotatef(rotationEarth_y, 0, 1, 0) #B 자전 7.0
    texture = load_texture("earthmap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture) 
    #gluSphere(sphere, 3.0, 20, 20)
    glutSolidSphere(3, 20, 20)
    glPopMatrix()

    glPushMatrix() #달
    glRotatef(revolutionEarth_y, 0, 1, 0) #달의 공전
    glPushMatrix()
    glTranslatef(5, 0, 0)
    glRotatef(rotationEarth_y, 0, 1, 0) #달 자전 7.0
    texture = load_texture("moonmap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture) 
    #gluSphere(sphere, 1.0, 20, 20)
    glutSolidSphere(1, 20, 20)
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    
    
    glPushMatrix() #화성
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_mars)
    glRotatef(revolutionEarth_y * (1/1.9), 0, 1, 0) #B의 공전 3.0
    glPushMatrix()
    glTranslatef(150, 0, 0)
    glRotatef(rotationEarth_y, 0, 1, 0) #B 자전 7.0
    texture = load_texture("marsmap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture) 
    #gluSphere(sphere, 3.0, 20, 20)
    glutSolidSphere(1.5, 20, 20)
    glPopMatrix()
    glPopMatrix()

    

    glPushMatrix() #토성
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_saturn)
    glRotatef(revolutionEarth_y * (1/11.9), 0, 1, 0)
    glTranslatef(950, 0, 0) #B x축으로 30
    glPushMatrix() #토성
    glRotatef(27, 1, 0, 0)
    glRotatef(rotationEarth_y, 0, 1, 0)
    #glutWireSphere(3, 10, 10)
    texture = load_texture("saturnmap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture) 
    #gluSphere(sphere, 5.0, 20, 20)
    glutSolidSphere(33.6, 20, 20)
    glPopMatrix()
    gluDisk(gluNewQuadric(), 4, 5, 1, 10)
    glPopMatrix()
    

    glPushMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_jupiter)
    glRotatef(revolutionEarth_y * (1 / 29.5), 0, 1, 0)
    glPushMatrix() #목성
    glTranslatef(520, 0, 0)
    glRotatef(rotationEarth_y, 0, 1, 0)
    texture = load_texture("jupitermap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture) 
    #gluSphere(sphere, 6.0, 20, 20)
    glutSolidSphere(28.2, 20, 20)
    glPopMatrix()
    glPopMatrix()
            
            
    glPushMatrix() #천왕성
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_uranus)
    glRotatef(revolutionEarth_y * (1 / 1.5), 0, 1, 0)
    glPushMatrix()
    glTranslatef(1920, 0, 0)
    glRotatef(rotationEarth_y, 0, 1, 0)
    texture = load_texture("neptunemap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture) 
    #gluSphere(sphere, 3.0, 20, 20)
    glutSolidSphere(12, 20, 20)
    glPopMatrix()
    glPopMatrix()
            
    
    glPushMatrix() #해왕성
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_neptune)
    glRotatef(revolutionEarth_y * (1 / 1.2), 0, 1, 0)
    glPushMatrix()
    glTranslatef(3010, 0, 0)
    glRotatef(rotationEarth_y, 0, 1, 0)
    texture = load_texture("neptunemap.jpg")
    glBindTexture(GL_TEXTURE_2D, texture) 
    #gluSphere(sphere, 3.0, 20, 20)
    glutSolidSphere(11.7, 20, 20)
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    
    
    
def display():
    global revolutionEarth_y
    global rotationEarth_y
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.8, 0.5, 0.8)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #방향키를 움직이면 뷰어의 위치와 방향을 바꾼다.
    gluLookAt(LookAt_viewrPos_x, LookAt_viewrPos_y, LookAt_viewrPos_z,
            LookAt_viewrDir_x, LookAt_viewrDir_y, LookAt_viewrDir_z,
            0, 1, 0)
    glScalef(2, 2, 1)
    light()

    revolutionEarth_y += 2 #A의 자전 증가
    rotationEarth_y += 3 #B의 자전 증가

    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    #sphere = gluNewQuadric()
    #gluQuadricTexture(sphere, GL_TRUE)

    drawPlanet()

    glFlush()



def spckeycallback(key, x, y):
    #키보드 콜백함수
    #카메라의 위치를 변화시킨다
    global LookAt_viewrPos_x
    global LookAt_viewrPos_z
    global LookAt_viewrDir_x
    global LookAt_viewrDir_z

    print(key)
    if (key == 100): #왼쪽이동
        LookAt_viewrPos_x -= 5.0
        LookAt_viewrDir_x -= 5.0
    
    if (key == 102): #오른쪽이동
        LookAt_viewrPos_x += 5.0
        LookAt_viewrDir_x += 5.0
    
    if (key == 103): #앞쪽이동
        LookAt_viewrPos_z += 5.0
        LookAt_viewrDir_z += 5.0
    
    if (key == 101): #뒤쪽이동
        LookAt_viewrPos_z -= 5.0
        LookAt_viewrDir_z -= 5.0
    

if __name__ == "__main__":
    revolutionEarth_y = 1.0 #초기화
    rotationEarth_y = 7.0
    LookAt_viewrPos_x = 10
    LookAt_viewrPos_y = 40
    LookAt_viewrPos_z = 500
    LookAt_viewrDir_x = 0
    LookAt_viewrDir_y = 0.3
    LookAt_viewrDir_z = 0

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    glutInitWindowSize(1600, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Solar System")

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutSpecialFunc(spckeycallback)
    glutReshapeFunc(reshape) #창의 크기가 변할 때 실행

    glutMainLoop()

