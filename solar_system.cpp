//#include <gl/glu.h>
#include <Windows.h>
#include <stdio.h>
#include <gl/glut.h>
#include <gl/glaux.h>

float revolutionEarth_y;
float rotationEarth_y;

double LookAt_viewrPos_x;
double LookAt_viewrPos_y;
double LookAt_viewrPos_z;


double LookAt_viewrDir_x;
double LookAt_viewrDir_y;
double LookAt_viewrDir_z;
GLUquadric *sphere;
unsigned int ids[10];
AUX_RGBImageRec *tex[10];
GLfloat plane_coef_s[] = {1.0, 0.0, 0.0, 1.0};
GLfloat plane_coef_t[] = {0.0, 1.0, 0.0, 1.0};
GLfloat plane_coef_r[] = {1.0, 0.0, 1.0, 1.0};

GLfloat mat_amb[4] = {0.1, 0.1, 0.1, 0.1};  //주변광에 대한 반사값
GLfloat mat_dif[4] = {0.6, 0.2, 0.6, 0.0};  //분산광에 대한 반사값
GLfloat mat_spc[4] = {0.8, 0.2, 0.8, 0.5};  //반사광에 대한 반사값
GLfloat mat_emi[4] = {0.1, 0.1, 0.0, 0.0};  //발광값
GLfloat mat_shi[1] = {100.0, 0.0};  //광택

GLfloat mat_emi_sun[4] = {1.0, 0.1, 0.0, 0.0};  //태양 발광값
GLfloat mat_emi_other[4] = {0.0, 0.0, 0.0, 0.0};  //태양 이외의 emission값
GLfloat mat_dif_sun[4] = {0.4, 0.1, 0.3, 0.0};  //태양 분산광에 대한 반사값
GLfloat mat_dif_mercury[4] = {0.2, 0.1, 0.7, 0.0};  //수성 분산광에 대한 반사값
GLfloat mat_dif_venus[4] = {0.5, 0.1, 0.2, 0.0};  //금성 분산광에 대한 반사값
GLfloat mat_dif_earth[4] = {0.2, 0.4, 0.2, 0.0};  //지구 분산광에 대한 반사값
GLfloat mat_dif_mars[4] = {0.8, 0.4, 0.2, 0.0};  //화성 분산광에 대한 반사값
GLfloat mat_dif_jupiter[4] = {0.1, 0.2, 0.7, 0.0};  //목성 분산광에 대한 반사값
GLfloat mat_dif_saturn[4] = {0.8, 0.5, 0.5, 0.0};  //토성 분산광에 대한 반사값
GLfloat mat_dif_uranus[4] = {0.5, 0.2, 0.7, 0.0};  //천왕성 분산광에 대한 반사값
GLfloat mat_dif_neptune[4] = {0.1, 0.1, 0.8, 0.0};  //혜왕성 분산광에 대한 반사값

//비트맵 파일명
wchar_t bitmap[12][20] = {TEXT("sun.bmp"), TEXT("Mercury.bmp"), TEXT("Venus.bmp"), 
                            TEXT("earth.bmp"), TEXT("Moon.bmp"), TEXT("Mars.bmp"), 
                            TEXT("Jupiter.bmp"), TEXT("Saturn.bmp"), TEXT("Uranus.bmp"),
                            TEXT("Nepture.bmp")};

//광원 초기화
void init_light(void) {
    static GLfloat lit_amb[4] = {1.0, 1.0, 1.0, 0.0}; //주변광의 강도
    static GLfloat lit_dif[4] = {1.0, 1.0, 1.0, 0.0}; //분산광의 강도
    static GLfloat lit_spc[4] = {1.0, 1.0, 1.0, 0.0}; //반사광의 강도
    static GLfloat lit_pos[4] = {0.0, 0.0, 0.0, 1.0}; //광원의 위치

    glLightfv(GL_LIGHTO, GL_AMBIENT, lit_amb);
    glLightfv(GL_LIGHTO, GL_DIFFUSE, lit_dif);
    glLightfv(GL_LIGHTO, GL_SPECULAR, lit_spc);
    glLightfv(GL_LIGHTO, GL_POSITION, lit_pos);

    //광원 ON
    glEnable(GL_LIGHTO);
    glEnable(GL_LIGHTING);
}

void textureinit() {
    //LPCWSTR file = 'earth.bmp';
    for (int i = 0; i < 10; i++) {//이미지 로드
        tex[i] = auxDIBImageLoad(bitmap[i]);
    } 

    glGenTextures(10, $ids[0]);

    for (int i = 0; i < 10; i++) {
        //printf("%s\n", bitmap[i]);
        //puts(bitmap[i]);
        wprintf(bitmap[i]);
        glBindTexture(GL_TEXTURE_2D, ids[i]);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);

        glTeximage2D(GL_TEXTURE_2D, 0, 3, tex[i] -> sizeX, tex[i] -> sizeY, 0, GL_RGB, GL_UNSIGNED_BYTE, tex[i] -> data);
    }

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
}

void reshape (int w, int h) {
    float ratio = w / (float)h;
    glViewport(0, 0, w, h);
    gl MatrixMode(GL_PROJECTION);
    glLoadidentity();

    gluPerspective(45, ratio, 0.1, 1000); //시야각, 가로 종횡비, 최소, 최대거리
}

void drawPlanet() {
    //GLfloat_coef_s[] = {1.0, 0.0, 0.0, 1.0};
    //GLfloat_coef_t[] = {0.0, 1.0, 0.0, 1.0};

    //재질세팅
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_amb);
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_spc);
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, mat_shi);

    glPushMatrix();
        glPushMatrix();
            glPushMatrix(); //태양
                //재질 특성 설정
                glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emi_sun);
                glRotatef(revolutionEarth_y, 0, 1, 0) //B의 공전 3.0
                glPushMatrix();

                    glTranslatef(0, 0, 0);
                    glRotatef(revolutionEarth_y, 0, 1, 0); //A의 자전 3.0
                    glBindTexture(GL_TEXTURE_2D, ids[0]);
                    gluSphere(sphere, 10., 20, 20);
                    // glutSolidSphere(7, 20, 20);
                glPopMatrix();

            glPopMatrix();

            glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emi_other);
            //glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, mat_emi_other);
            glPushMatrix(); //수성
                //glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_mercury);
                glRotatef(revolutionEarth_y, 0, 1, 0); //B 자전 7.0
                glPushMatrix(); 
                    glTranslatef(30, 0, 0);
                    glRotatef(rotationEarth_y, 0, 1, 0);                
                    glBindTexture(GL_TEXTURE_2D, ids[1]);
                    gluSphere(sphere, 3.0, 20, 20);
                    //glutSolidSphere(3, 20, 20);
                glPopMatrix();
            glPopMatrix();

            glPushMatrix(); //금성
                //glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_venus);
                glRotatef(revolutionEarth_y * (1/0.61), 0, 1, 0); //B의 공전 3.0
                glPushMatrix(); //금성
                    glTranslatef(50, 0, 0); // B x cnrdmfh 30
                    glRotatef(rotationEarth_y, 0, 1, 0); //B 자전 7.0
                    glBindTexture(GL_TEXTURE_2D, ids[2]);
                    gluSphere(sphere, 3.0, 20, 20);
                    //glutSolidSphere(3, 20, 20);
                glPopMatrix();
            glPopMatrix();

            glPushMatrix(); //지구
                //glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_earth);
                glRotatef(revolutionEarth_y, 0, 1, 0); //B의 공전 3.0
                glTranslatef(60, 0, 0); //x 축으로

                glPushMatrix(); //지구
                    glRotatef(rotationEarth_y, 0, 1, 0); //B 자전 7.0
                    glBindTexture(GL_TEXTURE_2D, ids[3]);
                    gluSphere(sphere, 3.0, 20, 20);
                glPopMatrix();

                glPushMatrix(); //달
                    glRotatef(revolutionEarth_y, 0, 1, 0); //달의 공전
                    glPushMatrix(); //달
                        glTranslatef(5, 0, 0); //B x축으로 30
                        glRotatef(rotationEarth_y, 0, 1, 0); //달 자전 7.0
                        glBindTexture(GL_TEXTURE_2D, ids[4]);
                    gluSphere(sphere, 1.0, 20, 20);

                        //glutSolidSphere(1, 20, 20);
                    glPopMatrix();
                glPopMatrix();
            glPopMatrix();

            glPushMatrix(); //화성
                //glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_mars);
                glRotatef(revolutionEarth_y * (1/1.9), 0, 1, 0); //B의 공전 3.0
                glPushMatrix();
                    glTranslatef(80, 0, 0);
                    glRotatef(rotationEarth_y, 0, 1, 0); //B 자전 7.0
                    //glutSolidSphere(3, 20, 20);
                    glBindTexture(GL_TEXTURE_2D, ids[5]);
                    gluSphere(sphere, 3.0, 20, 20);

                glPopMatrix();
            glPopMatrix();

            glPushMatrix(); //토성
                //glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_saturn);
                glRotatef(revolutionEarth_y * (1/11.9), 0, 1, 0);
                glTranslatef(120, 0, 0); //B x축으로 30

                glPushMatrix(); //토성
                    glRotatef(27, 1, 0, 0);
                    glRotatef(rotationEarth_y, 0, 1, 0); //B 자전 7.0
                    //glutWireSphere(3, 10, 10);
                    //glutSolidSphere(3, 20, 20);
                    glBindTexture(GL_TEXTURE_2D, ids[6]);
                    gluSphere(sphere, 5.0, 20, 20);
                glPopMatrix();

                //gluDisk(gluNewQuadric(), 4, 5, 1, 10);
                glPushMatrix();
                    glRotatef(revolutionEarth_y * (1/1), 0, 1, 0);
                    glPushMatrix();
                        glTranslatef(5, 0, 0); //B 축으로 30
                        glRotatef(rotationEarth_y, 0, 1, 0); //B 자전 7.0
                        glBindTexture(GL_TEXTURE_2D, ids[4]);
                        gluSphere(sphere, 1.0, 20, 20);
                        //glutSolidSphere(1, 20, 20);
                    glPopMatrix();
                glPopMatrix();

                glPushMatrix();
                    glRotatef(revolutionEarth_y * (1 / 1.2), 0, 1, 0);
                    glPushMatrix();
                        glTranslatef(7, 0, 0); //B 축으로 30
                        glRotatef(rotationEarth_y * 2, 0, 1, 0); //B 자전 7.0
                        glBindTexture(GL_TEXTURE_2D, dis[4]);
                        gluSphere(sphere, 1.0, 20, 20);
                    glPopMatrix();
                glPopMatrix();

            glPopMatrix();

            glPushMatrix();
                //glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_dif_jupiter);
                glRotatef(revolutionEarth_y * (1 / 29.5), 0, 1, 0);
                glPushMatrix(); //목성
                    glTranslatef(150, 0, 0); //B x축으로 30
                    glRotatef(rotationEarth_y, 0, 1, 0); //B 자전 7.0
                    //glutSolidSphere(3, 20, 20);
                    glBindTexture(GL_TEXTURE_2D, ids[7]);
                    gluSphere(sphere, 6.0, 20, 20);
                glPopMatrix();
            glPopMatrix();

            glPushMatrix(); //천왕성
                //glMaterialfv(GL_FRONT_AND_BACK, Gl_DIFFUSE, mat_dif_uranus);
                glRotatef(revolutionEarth_y * (1 / 1.5), 0, 1, 0);
                glPushMatrix(); //천왕성
                    glTranslatef(160, 0, 0); //B x측으로 30
                    glRotatef(rotationEarth_y, 0, 1, 0); //B 자전 7.0
                    glBindTexture(GL_TEXTURE_2D, ids[8]);
                    gluSphere(sphere, 3.0, 20, 20);
                glPopMatrix();
            glPopMatrix();


            glPushMatrix(); //해왕성
                //glMaterialfv(GL_FRONT_AND_BACK, Gl_DIFFUSE, mat_dif_uranus);
                glRotatef(revolutionEarth_y * (1 / 1.2), 0, 1, 0);
                glPushMatrix(); //해왕성
                    glTranslatef(180, 0, 0); //B x측으로 30
                    glRotatef(rotationEarth_y, 0, 1, 0); //B 자전 7.0
                    glBindTexture(GL_TEXTURE_2D, ids[9]);
                    gluSphere(sphere, 3.0, 20, 20);
                glPopMatrix();
            glPopMatrix();
        glPopMatrix();
    glPopMatrix();
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glColor3f(0.8, 0.5, 0.8);
    glMatrixMode(GL_MODEVIEW);
    glLoadidentity();

    //방향키를 움직이면 뷰어의 위치와 방향을 바꾼다.
    gluLookAt(LookAt_viewrPos_x, LookAt_viewrPos_y, LookAt_viewrPos_z,
            LookAt_viewrDir_x, LookAt_viewrDir_y, LookAt_viewrDir_z,
            0, 1, 0);
    glScalef(2, 2, 1);
    init_light();

    revolutionEarth_y += 0.01f; //A의 자전 증가
    rotationEarth_y += 0.1f; //B의 자전 증가

    glEnable(GL_TEXTURE_2D);
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    sphere = gluNewQuadric();
    gluNewQuadric(sphere, GL_TRUE);

    drawPlanet(); //행성 그리기

    glFlush();
}

void spckeycallback(int key, int x, int y) {
    //키보드 콜백함수
    //카메라의 위치를 변화시킨다

    printf("%d ", key);
    if (key == 100) { //왼쪽이동
        LookAt_viewrPos_x -= 5.0f;
        LookAt_viewrDir_x -= 5.0f;
    }
    if (key == 102) { //오른쪽이동
        LookAt_viewrPos_x += 5.0f;
        LookAt_viewrDir_x += 5.0f;
    }
    if (key == 103) { //앞쪽이동
        LookAt_viewrPos_z += 5.0f;
        LookAt_viewrDir_z += 5.0f;
    }
    if (key == 101) { //뒤쪽이동
        LookAt_viewrPos_z -= 5.0f;
        LookAt_viewrDir_z -= 5.0f;
    }
}

int main(int argc, char** argv) {
    revolutionEarth_y = 1.0f; //초기화
    rotationEarth_y = 7.0f;
    LookAt_viewrPos_x = 10;
    LookAt_viewrPos_y = 40;
    LookAt_viewrPos_z = 500;
    LookAt_viewrDir_x = 0;
    LookAt_viewrDir_y = 0.3;
    LookAt_viewrDir_z = 0;

    glutinit(&argc, argv);
    glutinitDisplayMode(GLUT_SINGLE | GLUT_RGB);

    glutintiWindowSize(640, 480);
    glutCreateWindow("Solar System");

    glutDisplayFunc(display);
    glutdisFunc(display);
    glutSpecialFunc(spckeycallback);
    glutReshapeFunc(reshape); //창의 크기가 변할 때 실행

    glEnable(GL_DEPTH_TEST);
    textureinit();
    glutMainLoop();

    return 0;
}