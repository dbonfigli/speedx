from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys
import time
import random
import Image
import pygame

import geometry
from geometry import *

###############################################################################

def axis(length):
    """ Draws an axis (basicly a line with a cone on top) """
    glPushMatrix()
    glBegin(GL_LINES)
    glVertex3d(0,0,0)
    glVertex3d(0,0,length)
    glEnd()
    glTranslated(0,0,length)
    glutWireCone(0.04,0.2, 12, 9)
    glPopMatrix()
    
def threeAxis(length):
    """ Draws an X, Y and Z-axis """ 
    glPushMatrix()
    glColor3f(1.0,0.0,0.0) 
    axis(length) # Z-axis
    glRotated(90,0,1.0,0)  
    glColor3f(0.0,1.0,0.0)
    axis(length) # X-axis
    glRotated(-90,1.0,0,0) 
    glColor3f(0.0,0.0,1.0)
    axis(length) # Y-axis
    glPopMatrix()

###############################################################################

def nowVector(l): # -> (posizione adesso, posizione punto sezione successiva, index sezione adesso)

    global t
    sofar = 0.
    sofarPrev = 0.
    vNow = (0.,0.,0.)
    lenNow = 0.
#    nowP = (0.,)
#    nNext = (0.,)
    nowInd = 0
    for i in range(len(l)-1):
        diff = difference(l[i+1], l[i])
        sofar += vLen(diff)
        if sofar >= t:
            vNow = diff
            nNext = l[i+1]
            lenNow = t - sofarPrev
            nowP = add (l[i], multip(normalize(vNow),lenNow))
            nowInd = i
            break
        else:
            sofarPrev = sofar
    return (nowP, nNext, nowInd)

####################################################################

def displayFun():

    # inizializzazione
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(0.0,1.0,0.0)

    #telecamera
    global globalOggetti
    nowP, nNext, nowInd = nowVector(globalOggetti.l2)

    altezzaCam = 0.08
    d = normalize(difference(nNext, nowP)) # rotazione intorno a questo vettore
    v = cross(d, (0.,1.,0.))
    v = multip(v, altezzaCam) # adesso ho il vettore della pos della cam non ruotato non traslato
    vr = rotateArbitrary(v, d, angleCam)

    vec = (vr[0]+nowP[0],vr[1]+nowP[1], vr[2]+nowP[2])
    vec2 = ( vec[0]+d[0], vec[1]+d[1], vec[2]+d[2]) 

    up = (nowP[0] - vec[0], nowP[1] - vec[1], nowP[2] - vec[2])

    gluLookAt(vec[0], vec[1], vec[2], vec2[0], vec2[1], vec2[2], up[0], up[1], up[2])

    glRotatef(d_x, 0.0, 1.0, 0.0);	#/* y-axis rotation */
    glRotatef(-d_y, 1.0, 0.0, 0.0);	#/* x-axis rotation */

    #oggetti centrali
   # threeAxis(0.5)
   # glutWireCube(1)

    #tubo
    glColor3f(1.0,.0,.0)
    drawTube()

    glFlush()
    glutSwapBuffers()
   # pygame.display.flip()

def drawTube():

    global globalOggetti
    staticTube = globalOggetti.staticTube

    nowP1, nNext1, nowSecInd = nowVector(globalOggetti.l)
#    print nowInd

  #  print len(staticTube)
    nsecstart = nowSecInd
    nsecsend = nowSecInd + 16
    if nsecsend > len(staticTube)-2:
        nsecsend = len(staticTube)-2
        

    for iCirc in range(nsecstart, nsecsend): #was: -1 #staticTube contiene tutti i punti gia ruotati     
 
        glPushMatrix()

        for i in range(len(staticTube[iCirc][1])-1): # per tutti i punti nel cerchio

            p1 = staticTube[iCirc][1][i][0]
            p2 = staticTube[iCirc][1][i+1][0]
            p3 = staticTube[iCirc+1][1][i+1][0]
            p4 = staticTube[iCirc+1][1][i][0]

            obstacle = False
            colorObs = 0
            if staticTube[iCirc][1][i][1] != 0 and staticTube[iCirc][1][i+1][1] != 0:
                obstacle = True
                colorObs = staticTube[iCirc][1][i][1]

            norm = (1., 1., 1., 0.)
            #norm = cross(difference(p2,p1), difference(p4,p1))  

#            pn1 = staticTube[iCirc+1][1][i]
#            pn2 = staticTube[iCirc+1][1][i+1]

#            pn3 = staticTube[iCirc+2][1][i+1]
#            pn4 = staticTube[iCirc+2][1][i]

#            normn = cross(difference(pn2,pn1), difference(pn4,pn1))

#            pp1 = staticTube[iCirc-1][1][i]
#            pp2 = staticTube[iCirc-1][1][i+1]

#            pp3 = staticTube[iCirc][1][i+1]
#            pp4 = staticTube[iCirc][1][i]

#            normp = cross(difference(pp2,pp1), difference(pp4,pp1))  
#  
#            normnown = ( (norm[0] + normn[0]) / 2. , (norm[1] + normn[1]) / 2. , (norm[2] + normn[2]) / 2. )
#            normnowp = ( (norm[0] + normp[0]) / 2. , (norm[1] + normp[1]) / 2. , (norm[2] + normp[2]) / 2. )

            normnowp = norm
            normnown = norm


            glBindTexture(GL_TEXTURE_2D, 1)
            glBegin(GL_QUADS)
            glTexCoord2f(1., 0.)
            glNormal3d(normnowp[0], normnowp[1], normnowp[2])
            glVertex3d(p1[0], p1[1], p1[2])

            glTexCoord2f(1., 1.)
            glNormal3d(normnown[0], normnown[1], normnown[2])
            glVertex3d(p2[0], p2[1], p2[2])

            glTexCoord2f(0., 1.)
            glNormal3d(normnown[0], normnown[1], normnown[2])
            glVertex3d(p3[0], p3[1], p3[2])

            glTexCoord2f(0., 0.)
            glNormal3d(normnowp[0], normnowp[1], normnowp[2])
            glVertex3d(p4[0], p4[1], p4[2])
            glEnd()


            if obstacle == True:
                drawObstacle(p1, p2, p3, p4, staticTube[iCirc][0], staticTube[iCirc+1][0], colorObs)

        glPopMatrix()

    ################################################

#    print len(globalOggetti.l) , nowSecInd, len(globalOggetti.l) - nowSecInd
    if len(globalOggetti.l) - nowSecInd < 220:
#        print nowSecInd, len(globalOggetti.l)
        globalOggetti.rebuild()
#        print len(globalOggetti.l)


#immagina sul terreno la figura
#p4 p3
#p1 p2
def drawObstacle(p1, p2, p3, p4, cNear, cFar, colorObs):

    p1u = add( p1, multip ( add(multip(p1, -1), cNear), 0.5))
    p2u = add( p2, multip ( add(multip(p2, -1), cNear), 0.5))
    p3u = add( p3, multip ( add(multip(p3, -1), cFar ), 0.5))
    p4u = add( p4, multip ( add(multip(p4, -1), cFar ), 0.5))

    glBindTexture(GL_TEXTURE_2D, colorObs)
    glBegin(GL_QUADS)
    glTexCoord2f(0., 0.)
    glVertex3d(p2[0], p2[1], p2[2])
    glTexCoord2f(1., 0.)
    glVertex3d(p3[0], p3[1], p3[2])
    glTexCoord2f(1., 1.)
    glVertex3d(p3u[0], p3u[1], p3u[2])
    glTexCoord2f(0., 1.)
    glVertex3d(p2u[0], p2u[1], p2u[2])
    glEnd()

    glBindTexture(GL_TEXTURE_2D, colorObs)
    glBegin(GL_QUADS)
    glTexCoord2f(0., 0.)
    glVertex3d(p1[0], p1[1], p1[2])
    glTexCoord2f(1., 0.)
    glVertex3d(p2[0], p2[1], p2[2])
    glTexCoord2f(1., 1.)
    glVertex3d(p2u[0], p2u[1], p2u[2])
    glTexCoord2f(0., 1.)
    glVertex3d(p1u[0], p1u[1], p1u[2])
    glEnd()


    glBindTexture(GL_TEXTURE_2D, colorObs)
    glBegin(GL_QUADS)
    glTexCoord2f(0., 0.)
    glVertex3d(p4[0], p4[1], p4[2])
    glTexCoord2f(1., 0.)
    glVertex3d(p1[0], p1[1], p1[2])
    glTexCoord2f(1., 1.)
    glVertex3d(p1u[0], p1u[1], p1u[2])
    glTexCoord2f(0., 1.)
    glVertex3d(p4u[0], p4u[1], p4u[2])
    glEnd()


    glBindTexture(GL_TEXTURE_2D, colorObs)
    glBegin(GL_QUADS)
    glTexCoord2f(0., 0.)
    glVertex3d(p1u[0], p1u[1], p1u[2])
    glTexCoord2f(1., 0.)
    glVertex3d(p2u[0], p2u[1], p2u[2])
    glTexCoord2f(1., 1.)
    glVertex3d(p3u[0], p3u[1], p3u[2])
    glTexCoord2f(0., 1.)
    glVertex3d(p4u[0], p4u[1], p4u[2])
    glEnd()

    glTexCoord2f(1., 0.)
    glVertex3d(p1[0], p1[1], p1[2])


################################################################################
### EVENTS #####################################################################
################################################################################
################################################################################

def mouseFun(x, y):
    global m_last_x
    global m_last_y 
    global d_x
    global d_y
    d_x = (d_x + x - m_last_x) % 360
    d_y = (d_y + y - m_last_y) % 360
    m_last_x = x
    m_last_y = y
    glutPostRedisplay()

def mouseFun2(button, state, x, y):
    global m_last_x
    global m_last_y 
    if state == GLUT_DOWN:
        m_last_x = x;
        m_last_y = y;


def keyFunUp(c,x,y):
    global goLeft
    global goRight
    if c=="a":
        goRight = False
    if c=="d":
        goLeft = False

def keyFunDown(c,x,y):
    global angleCam
    global goLeft
    global goRight
    global stopTime
    global speed
    if c=="a":
        goRight = True
    if c=="d":
        goLeft = True
    if c=="w":
        speed += 0.005
    if c=="s":
        speed -= 0.005
    if c==" ":
        global t
        t += speed
        glutPostRedisplay()
    if c=="p":
        stopTime = True if stopTime == False else False
        print stopTime

def timeFun(x):
    global t
    global t0
    global angleCam
    global goLeft
    global goRight

    global inertia
    global direc
    if goLeft == True:
        direc = -1
        inertia = 1

    if goRight == True:
        direc = 1
        inertia = 1

    if inertia > 0:
        inertia -= 0.07
    else:
        inertia = 0.

    angleCam += inertia*direc*0.1

    global speed
    global stopTime
    if stopTime == False:
        t += speed

    glutPostRedisplay()
    glutTimerFunc	( 1*(1000 /25)  , timeFun, 0)

################################################################################
### MAIN #######################################################################
################################################################################
################################################################################

if __name__ == '__main__':

    goLeft = False
    goRight = False
    stopTime = False
    #init vars
    angleCam = 0
    t = 0.
    t0 = 0.
    m_last_x = 0.0
    m_last_y = 0.0
    d_x = 0
    d_y = 0
    speed = 0.02
    inertia = 0.
    direc = 0
    globalOggetti = Oggetti()

    #init opengl
    glutInit()
    glutInitWindowSize(1200, 800)

    glutCreateWindow("3D")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0,0.0,0.0,0.0)
    glutDisplayFunc(displayFun)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(100.0, 1200./800., 0.01, 10) #glOrtho(-10, 10, -10, 10, -10, 10)
    
    #init events
    glutMouseFunc(mouseFun2)
    glutMotionFunc(mouseFun)
   # glutKeyboardFunc(keyFun)
    glutSetKeyRepeat(GLUT_KEY_REPEAT_OFF)
    glutKeyboardFunc(keyFunDown)
    glutKeyboardUpFunc(keyFunUp)
  #  glutKeyboardDownFunc(keyFunDown)

    #lights
    glEnable(GL_LIGHTING)

    subdLevelSlice = 0
    subdLevelStack = 0
    shine = 25

    glEnable(GL_NORMALIZE)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)

    diffuse0=(0.0, 0.0, 0.0, 1.0)
    ambient0=(0.0, 0.0, 0.0, 1.0)
    specular0=(1.0, 0.0, 0.0, 1.0)
    light0_pos = (1000.0, -3000.0, -0000, 1.0)

    glLightfv(GL_LIGHT0, GL_POSITION, light0_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular0)
    glEnable(GL_LIGHT0)

    diffuse1=(0.0, 0.5, 1.0, 1.0)
    ambient1=(0.0, 0.5, 1.0, 1.0)
    specular1=(1.0, 1.0, 1.0, 1.0)
    light1_pos=(000.0, -30000.0, -30000, 1.0)

    glLightfv(GL_LIGHT1, GL_POSITION, light1_pos)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specular1)
    glEnable(GL_LIGHT1)

    ambient = (0.7, 0.7, 0.7, 0.0)
    diffuse = (.7, 0.7, 0.7, 0.0)
    specular = (1.0, 1.0, 1.0, 0.0)

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMateriali(GL_FRONT, GL_SHININESS, shine)

    glShadeModel(GL_SMOOTH)

###############

#    glEnable(GL_BLEND)
#    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
#    glEnable(GL_POLYGON_SMOOTH)
#    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

#############################################################

    glFogi(GL_FOG_MODE, GL_EXP2)
    glFogfv(GL_FOG_COLOR, (0., 0., 0., 1.))
    glFogf(GL_FOG_DENSITY, 2.35)
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogf(GL_FOG_START, 1.0)
    glFogf(GL_FOG_END, 4.0)
    glEnable(GL_FOG)


#############################################################

    glEnable(GL_TEXTURE_2D)
    glShadeModel(GL_SMOOTH)
    imgsurf = pygame.image.load("/home/bonfigli/Desktop/pygl/speedx2/h.jpg")
    imgstring = pygame.image.tostring(imgsurf, "RGBA", 1)
    width, height = imgsurf.get_size()

    print glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, 1)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgstring)

#######

    imgsurf2 = pygame.image.load("/home/bonfigli/Desktop/pygl/speedx2/h1.jpg")
    imgstring2 = pygame.image.tostring(imgsurf2, "RGBA", 1)
    width2, height2 = imgsurf2.get_size()

    print glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, 2)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width2, height2, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgstring2)

#######

    imgsurf3 = pygame.image.load("/home/bonfigli/Desktop/pygl/speedx2/h2.jpg")
    imgstring3 = pygame.image.tostring(imgsurf3, "RGBA", 1)
    width3, height3 = imgsurf3.get_size()

    print glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, 3)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width3, height3, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgstring3)

#######

    imgsurf4 = pygame.image.load("/home/bonfigli/Desktop/pygl/speedx2/h3.jpg")
    imgstring4 = pygame.image.tostring(imgsurf4, "RGBA", 1)
    width4, height4 = imgsurf4.get_size()

    print glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, 4)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width4, height4, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgstring4)

###############

    #GO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    glutTimerFunc( 1000 / 5 , timeFun, 0)
    t0 = time.time()
    glutMainLoop()

