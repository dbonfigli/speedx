from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys
import time
import random



def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class Oggetti():

    def __init__(self):
        self.p = [ (-2,0,0), (-1,0,0)]#, (0,0,0), (0,0,-1), (1,1,-2), (1,2,-3), (2,3,-4), (3,1,-6) ]
        self.rebuild()
        print self.p
        self.l = self._path(4)
        self.l2 = self._path(8)
        self.staticTube = self._buildStaticTube(self.l)

    def rebuild(self):
        newp = list(self.p)
        print self.p
        for i in range(30):
            w = round(random.random())-1
            if random.random() > 0.5:
                rany, ranz = w, 0
            else:
                rany, ranz = 0, w
            pn = ( self.p[-1][0]+1*i+1, self.p[-1][1]+rany, self.p[-1][2]+ranz )
        #    pn = ( self.p[-1][0]+1*i, self.p[-1][1]+round(random.random())-1, self.p[-1][2]+round(random.random())-1 )
            newp.append(pn)
        self.p = newp
#        print newp
        #ricordarsi di eliminare quelli passati
        self.l = self._path(4)
        self.l2 = self._path(8)
        self.staticTube = self._buildStaticTube(self.l)

    def _path(self, iterations):
        
        p = self.p
        for n in range(iterations):
            l = []
            for i in range(len(p)):

                if i == 0:
                    l.append(p[i])
                    x = 1.0/8.0 * (4.0*p[i][0] + 4.0*p[i+1][0])
                    y = 1.0/8.0 * (4.0*p[i][1] + 4.0*p[i+1][1])
                    z = 1.0/8.0 * (4.0*p[i][2] + 4.0*p[i+1][2])
                    l.append( (x,y,z) )
                elif i == len(p) - 1:
                    l.append(p[i])
                else:
                    x = 1.0/8.0 * (p[i-1][0] + 6.0*p[i][0] + p[i+1][0])
                    y = 1.0/8.0 * (p[i-1][1] + 6.0*p[i][1] + p[i+1][1])
                    z = 1.0/8.0 * (p[i-1][2] + 6.0*p[i][2] + p[i+1][2])
                    l.append( (x,y,z) )
                    x = 1.0/8.0 * (4.0*p[i][0] + 4.0*p[i+1][0])
                    y = 1.0/8.0 * (4.0*p[i][1] + 4.0*p[i+1][1])
                    z = 1.0/8.0 * (4.0*p[i][2] + 4.0*p[i+1][2])
                    l.append( (x,y,z) )
            p = list(l)
        return l

    def _sectionSoft(self):

        n = 12
        lenght = 0.12
        angleinc =  (math.pi*2) / n
        angle = 0.0
        s = []
        for i in range(n+1):
            x = math.cos(angle) * lenght
            y = math.sin(angle) * lenght
            p = (x, y, 0)
            s.append(p)
            angle += angleinc       
        return s

    def _buildStaticTube(self, l): # -> lista(centro, struttura cerchio)

        secSoft = self._sectionSoft()
        retv = []
        for i in range(len(l)-1):
            center = l[i]
            direction = normalize(difference(l[i+1], l[i]))
            ax = normalize (cross( (0.,0.,-1.), direction )) #ax: asse di rotazione
            ns = []
            for p in secSoft:      
                pt = rotateArbitrary(p, ax, math.acos(dot((0.,0.,-1.), direction)) )
                pt = (pt[0] + center[0], pt[1] + center[1], pt[2] + center[2]) #traslazione
                rn = int(random.random()*3)+2 if random.random() * 10 <= 1 else 0 #attenzione! qui ricreo pure quelli creati precedentemente!
                ns.append( (pt, rn ) )
#                ns.append( pt )
            retv.append( (center, ns) )

#        ###### normali
#        staticTube = []
#        for iCirc in range(len(retv)-1):  #staticTube contiene tutti i punti gia ruotati
#            elemTube = (retv[0][0], retv[iCirc] )
#            for i in range(len(retv[iCirc][1])-1): # per tutti i punti nel cerchio
#                p1 = staticTube[iCirc][1][i]
#                p2 = staticTube[iCirc][1][i+1]
#                p3 = staticTube[iCirc+1][1][i+1]
#                p4 = staticTube[iCirc+1][1][i]
#                norm = cross(difference(p2,p1), difference(p4,p1))
#                static
#        ##############

        return retv

#################################################

def difference(a, b):
    return ( a[0] - b[0], a[1] - b[1], a[2] - b[2] )

def vLen(v):
    return math.sqrt( (v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2]) )

def normalize(v):
    vLen = math.sqrt( (v[0] * v[0]) + (v[1] * v[1]) + (v[2] * v[2]) )
    if vLen == 0.:
        return v
    return ( v[0] / vLen, v[1] / vLen, v[2] / vLen )

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def cross(a, b):
    c = (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])
    return c

def multip(v, s):
    return (v[0]*s, v[1]*s, v[2]*s)

def add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def zero(m,n):     # Create zero matrix
    new_matrix = [[0.0 for row in range(n)] for col in range(m)]
    return new_matrix

def mult(matrix1,matrix2):
    # Matrix multiplication
    if len(matrix1[0]) != len(matrix2):
        # Check matrix dimensions
        print 'Matrices must be m*n and n*p to multiply!'
    else:
        # Multiply if correct dimensions
        new_matrix = zero(len(matrix1),len(matrix2[0]))
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
                    new_matrix[i][j] += matrix1[i][k]*matrix2[k][j]
        return new_matrix

def rotatex(v, alfa):
    sx = math.sin(alfa)
    cx = math.cos(alfa)
    mrot = [ [1.0,0.0,0.0,0.0], [0.0,cx,-sx,0.0], [0.0,sx,cx,0.0], [0.0,0.0,0.0,1.0] ]
    vector = [ [v[0]], [v[1]], [v[2]], [0.0] ]
    res = mult(mrot, vector)
    return ( res[0][0], res[1][0], res[2][0] )
   
def rotatey(v, alfa):
    sx = math.sin(alfa)
    cx = math.cos(alfa)
    mrot = [ [cx,0.0,sx,0.0], [0.0,1,0.0,0.0], [-sx,0.0,cx,0.0], [0.0,0.0,0.0,1.0] ]
    vector = [ [v[0]], [v[1]], [v[2]], [0.0] ]
    res = mult(mrot, vector)
    return ( res[0][0], res[1][0], res[2][0] )

def rotatez(v, alfa):
    sx = math.sin(alfa)
    cx = math.cos(alfa)
    mrot = [ [cx,-sx,0.0,0.0], [sx,cx,0.0,0.0], [0.0,0.0,1.0,0.0], [0.0,0.0,0.0,1.0] ]
    vector = [ [v[0]], [v[1]], [v[2]], [0.0] ]
    res = mult(mrot, vector)
    return ( res[0][0], res[1][0], res[2][0] )

def rotateArbitrary(v, d, alfa): #v:vettore da ruotare, d: asse, alfa: angolo
    ca = math.cos(alfa)
    sa = math.sin(alfa)
    x,y,z = d[0], d[1], d[2]
    mrot = [ [ca + x*x*(1-ca),  x*y*(1-ca)-z*sa,  x*z*(1-ca)+y*sa ] , \
            [y*x*(1-ca)+z*sa,  ca+y*y*(1-ca),    y*z*(1-ca)-x*sa ] ,  \
            [z*x*(1-ca)-y*sa,  z*y*(1-ca)+x*sa,  ca+z*z*(1-ca)   ]    \
          ] 
    vector = [ [v[0]], [v[1]], [v[2]] ]
    res = mult(mrot, vector)
    return ( res[0][0], res[1][0], res[2][0] )




