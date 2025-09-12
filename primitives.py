# coding: utf-8
import sys

try :
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ("Error: PyOpenGL not installed properly !!")
  sys.exit()

from math import radians,sin,cos

angle_y=0.0
c_rho,c_phi,c_theta=10,0,90

def square(size) :
# face avant : sommets de couleurs RGBW
  glBegin(GL_POLYGON)
  glColor3f(1.0,0.0,0.0)   # Red 
  glVertex2f(-size,-size)
  glColor3f(0.0,1.0,0.0)   # Green
  glVertex2f(size,-size)
  glColor3f(0.0,0.0,1.0)   # Blue
  glVertex2f(size,size)
  glColor3f(1.0,1.0,1.0)   #  White
  glVertex2f(-size,size)
  glEnd()
# face arriere : couleur uniforme White
  glBegin(GL_POLYGON)
  glVertex2f(-size,-size)
  glVertex2f(-size,size)
  glVertex2f(size,size)
  glVertex2f(size,-size)
  glEnd()

def cube_colored(size) :
  glBegin(GL_QUADS)
  glColor3ub(0,255,0)            # face rouge
  glVertex3d(size,size,size)
  glVertex3d(size,size,-size)
  glVertex3d(-size,size,-size)
  glVertex3d(-size,size,size)
  glColor3ub(255,0,0)            # face verte
  glVertex3d(size,-size,size)
  glVertex3d(size,-size,-size)
  glVertex3d(size,size,-size)
  glVertex3d(size,size,size) 
  glColor3ub(0,0,255)           # face bleue
  glVertex3d(size,-size,size)
  glVertex3d(size,size,size)
  glVertex3d(-size,size,size)
  glVertex3d(-size,-size,size)
  glColor3ub(255,255,0)          #  face jaune
  glVertex3d(-size,size,size)
  glVertex3d(-size,size,-size)
  glVertex3d(-size,-size,-size)
  glVertex3d(-size,-size,size)
  glColor3ub(255,0,255)           # face magenta
  glVertex3d(-size,-size,size)
  glVertex3d(-size,-size,-size)
  glVertex3d(size,-size,-size)
  glVertex3d(size,-size,size) 
  glColor3ub(0,255,255)          # face cyan
  glVertex3d(size,size,-size)
  glVertex3d(size,-size,-size)
  glVertex3d(-size,-size,-size)
  glVertex3d(-size,size,-size)
  glEnd()

# def sphere(radius,slices=20,stacks=10) :
def sphere(radius,longitude=20,latitude=10) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluSphere(params,radius,longitude,latitude)
  gluDeleteQuadric(params)

def cylinder(base,top,height,slices=10,stacks=5) : #ici on crée un cylindre
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluCylinder(params,base,top,height,slices,stacks)
  gluDeleteQuadric(params)

def disk(inner,outer,slices=10,loops=5) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluDisk(params,inner,outer,slices,loops)
  gluDeleteQuadric(params)

def cone(base,height,slices=10,stacks=5) :
  glPushMatrix()
  glRotatef(180,0,1,0)
  disk(0,base,slices,stacks)
  glPopMatrix()
  cylinder(base,0,height,slices,stacks)

def stick(base,top,height,slices=10,stacks=5) :
  glPushMatrix()
  glRotatef(180,0,1,0)
  glColor3f(1,0,0)
  disk(0,base,slices,stacks)
  glPopMatrix()
  glColor3f(0,1,0)
  cylinder(base,top,height,slices,stacks)
  glPushMatrix()
  glTranslatef(0,0,height)
  glColor3f(1,0,0)
  disk(0,top,slices,stacks)
  glPopMatrix()

def torus(inner,outer,sides=10,rings=5) :
  glutSolidTorus(inner, outer, sides, rings)


def floor(size,tiles=10) :
  tile_size=size/tiles
  for i in range(10+1) :
    for j in range(10+1) :
        glPushMatrix()
        glTranslatef(-size/2.0+tile_size*i,0.0,-size/2.0+tile_size*j)
        if (i+j)%2 == 0 :
            glColor3f(1.0,1.0,1.0)
            glRotatef(-90,1,0,0)
            glRectf(-tile_size/2.0, -tile_size/2.0, tile_size/2.0, tile_size/2.0)
        else :
            glColor3f(0.0,0.0,0.0)
            glRotatef(90,1,0,0)
            glRectf(-tile_size/2.0, -tile_size/2.0, tile_size/2.0, tile_size/2.0)
        glPopMatrix()

def wcs_lines(size) :
  glLineWidth(3)
  glBegin(GL_LINES)
  glColor3f(0.0,1.0,0.0)
  glVertex2f(0,0)
  glVertex2f(0,size)
  glColor3f(1.0,0.0,0.0)
  glVertex2f(0,0)
  glVertex2f(size,0)
  glColor3f(0.0,0.0,1.0)
  glVertex2f(0,0)
  glVertex3f(0,0,size)
  glEnd()
  glLineWidth(1)

def bone(size) : #crée un os pour l'ACA
  glPushMatrix()
  glColor3f(1,0,0)
  sphere(0.2*size)
  glColor3f(0,1,0)
  glTranslatef (0.0,0.0,0.1*size)
  cylinder(0.2*size,0.1*size,size)
  glPopMatrix()

# TODO : create 3D axe with disk,cylinder,cone
def axis(base,height,slices=10,stacks=5) : # crée un axe (shaft + arrowhead) orienté le long de +Oz
  shaft_height = 0.8*height
  head_height = height - shaft_height
  # shaft
  cylinder(base, base, shaft_height, slices, stacks)
  # arrow head
  glPushMatrix()
  glTranslatef(0,0,shaft_height)
  cone(2*base, head_height, slices, stacks)
  glPopMatrix()

# TODO : create 3D World Coordinates System using the above axis() fonction  
def wcs_axis(size) :
  # (Ox, Oy, Oz) axes <=> (R, G, B)
  radius = 0.05*size
  height = 1.2*size
  # X axis (red)
  glPushMatrix()
  glColor3f(1.0,0.0,0.0)
  glRotatef(90,0,1,0)  # align +Oz to +Ox
  axis(radius, height)
  glPopMatrix()
  # Y axis (green)
  glPushMatrix()
  glColor3f(0.0,1.0,0.0)
  glRotatef(-90,1,0,0) # align +Oz to +Oy
  axis(radius, height)
  glPopMatrix()
  # Z axis (blue)
  glPushMatrix()
  glColor3f(0.0,0.0,1.0)
  axis(radius, height)
  glPopMatrix()

def gl_init() :
#  glClearColor(1.0,1.0,1.0,0.0);
  glClearColor(0.5,0.5,0.5,0.0)
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)

def display() :
  global size,angle_y
  global c_rho,c_phi,c_theta
  gl_init()
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  size=1.0
  # camera positioning
  theta=radians(c_theta)
  phi=radians(c_phi)
  c_position_z=c_rho*sin(theta)*cos(phi)
  c_position_x=c_rho*sin(theta)*sin(phi)
  c_position_y=c_rho*cos(theta)
  c_direction_x,c_direction_y,c_direction_z=[0,0,0]
  c_viewup_x, c_viewup_y, c_viewup_z=[0,1,0]
  
  gluLookAt(
    c_position_x,c_position_y,c_position_z,
    c_direction_x,c_direction_y,c_direction_z,
    c_viewup_x,c_viewup_y,c_viewup_z
  )
  glPushMatrix()
  glRotatef(angle_y,0,1,0)
  wcs_lines(size)
  # 1) TODO : floor creation
  #    call square() primitive
  #    tranform it to visualize square() in the Oxz plane

  glPushMatrix()
  glRotatef(-90,1,0,0)
  square(2*size)
  
  #floor(10*size)
  glPopMatrix()

  # 2) TODO : test primitives
  #    create primitive (cone() ...)
  #    center it on the WCS and place it on the floor
  glPushMatrix()
  glRotatef(-90,1,0,0) #(angle, x,y,z)
  cone(size, size*2)
  glPopMatrix()


  # 3) TODO : CW and CCW faces # 4) TODO : create WCS with 3D axis
  #    call  wcs_axis() (implement above axis() and  wcs_axis() functions)
  #    create  cube_colored()
  #    use (c/C) key to visualize CW,CCW visualisation
  #    use (z/Z) key to start/stop animation
  glPushMatrix()
  glTranslatef(2.0*size, 0.5*size, 0.0)
  cube_colored(0.5*size)
  glPopMatrix()



  # 4) TODO : create WCS with 3D axis
  #    call  wcs_axis() (implement above axis() and  wcs_axis() functions)
  wcs_axis(size)
  glPopMatrix()
  glutSwapBuffers()

def reshape(width,height) :
  glViewport(0,0, width,height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  fovy,ratio,near,far=60.0,width*1.0/height,0.1,50.0
  gluPerspective(fovy,ratio,near,far)

def on_keyboard_action(key,x,y) :
  global c_position,c_rho,c_phi,c_theta
  speed=0.1
  if key==b'h':
    print("----------------------------------------") 
    print("Documentation Interaction  : Nom-Prenom ") 
    print("h : afficher cette aide")
    print("---------") 
    print("Affichage")
    print("---------") 
    print("c/C : afficher faces CW/CCW")
    print("p/f/l : afficher sommets/faces/aretes")
    print("---------------------") 
    print("Contrôle de la caméra")
    print("---------------------")
    print("u/U : déplacer la caméra en hauteur")
    print("key up : rapprocher la caméra au centre de la scene")
    print("key down : eloigner la caméra du centre de la scene")
    print("key left : déplacer la caméra sur la gauche autour de la scene")
    print("key right : déplacer la caméra sur la droite autour de la scene")
    print("---------") 
    print("Animation")
    print("---------")
    print("z/Z : lancer/stopper l'animation")
    print("----------------------------------------") 
  elif key== b'c' :
    glFrontFace(GL_CW)
  elif key== b'C' :
    glFrontFace(GL_CCW)
  elif key== b'p' :
    glPolygonMode(GL_FRONT_AND_BACK,GL_POINT);
  elif key== b'f':
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
  elif key== b'l':
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
  if key == b'u' :
    c_theta+=5*speed
  elif key == b'U' :
    c_theta-=5*speed
  elif key == b'q' :
    exit(0)
  elif  key== b'z' :
    glutIdleFunc(animation)
  elif  key== b'Z' : 
    glutIdleFunc(None)
  glutPostRedisplay()

def animation() :
  global angle_y
  angle_y+=0.1
  if angle_y > 360 :
    angle_y=0
  glutPostRedisplay()

def on_special_keyboard_action(key,x,y) :
  global c_rho,c_phi,c_theta
  speed=0.1
  if key ==  GLUT_KEY_UP :
        c_rho=c_rho-speed
  elif  key ==  GLUT_KEY_DOWN :
      c_rho=c_rho+speed
  elif key ==  GLUT_KEY_LEFT :
      c_phi=c_phi-5*speed
  elif  key ==  GLUT_KEY_RIGHT :
      c_phi=c_phi+5*speed
  else :
    print(f"no interaction on special key : {key}")
  glutPostRedisplay()


if __name__ == "__main__" :
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
  glutInitWindowSize(1200,1000)
  glutInitWindowPosition(100,100)
  glutCreateWindow ("REV 2025P : Primitives")
  glutDisplayFunc(display)
  glutReshapeFunc(reshape)
  glutKeyboardFunc(on_keyboard_action)
  glutSpecialFunc(on_special_keyboard_action)
  glutMainLoop()
