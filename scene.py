# coding: utf-8
# https://stackoverflow.com/questions/49236745/opengl-translation-before-and-after-a-rotation
from primitives import *



try :
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ("Error: PyOpenGL not installed properly !!")
  sys.exit()

from math import radians,sin,cos
from primitives import square,floor,wcs_lines,wcs_axis
from primitives import sphere,cylinder,cone,bone


c_rho,c_phi,c_theta=10,0,90
m_rho,m_theta=0,0.0
m_position=[0.0,0,0.0]

# TODO : create two connected bones to rotate with angles (arm,forarm)
arm,forarm=90.0,45.0
# TODO  :  create robot to manage arm,forarm angles rotation aroune one axis
def robot(size) :
  global arm,forarm
  # Hierarchical arm → forearm around Y axis (in Oxz plane)
  glPushMatrix()
  glRotatef(arm, 0, 1, 0)     # rotate upper arm
  bone(size)                  # draw upper arm along +Z
  glTranslatef(0.0, 0.0, size)
  glRotatef(forarm, 0, 1, 0)  # rotate forearm
  bone(size)                  # draw forearm
  glPopMatrix()


# TODO  : create car with a bodywork, 4 rotating wheels  with bolts
w_orientation=0.0
def wheel(size=1.0,bolts=3) :
  global w_orientation            # cf callback on_keyboard_action()
  glPushMatrix()  # wheel creation
  # TODO : transformation to rotate wheel with bolts when car go forward/backward
  glRotatef(90,0,1,0)
  glColor3f(0,0,0)
  torus(0.1*size,size)
  angle=360.0/bolts
  for i in range(bolts) :   # bolts creation on wheel 
    glPushMatrix() 
    # TODO : transformation to set position bolts en wheel
    stick(0.1*size,0.1*size,0.25*size)
    glPopMatrix()
  glPopMatrix()  # end wheel creation

def bodywork(size) :
  glColor3f(1.0,1.0,0.0)
  cone(0.2*size,size)

def car(size) :
  bodywork(size)
  #glPushMatrix()
  #--------------------------------

# Dimensions
  wheel_size = 0.2 * size
  wheel_offset_x = 0.5 * size   # écart sur l’axe X entre le centre de la voiture et les roues (gauche/droite)
  wheel_offset_y = 0 * size # hauteur des roues par rapport au corps
  wheel_offset_z = 0.6 * size   # écart sur l’axe Z entre l’avant et l’arrière

  # AVG
  glPushMatrix()
  glTranslatef(-wheel_offset_x, wheel_offset_y, wheel_offset_z)
  wheel(wheel_size,5)
  glPopMatrix()

  # AVD
  glPushMatrix()
  glTranslatef(wheel_offset_x, wheel_offset_y, wheel_offset_z)
  wheel(wheel_size,5)
  glPopMatrix()

  # ARD
  glPushMatrix()
  glTranslatef(wheel_offset_x, wheel_offset_y, -wheel_offset_z)
  wheel(wheel_size,5)
  glPopMatrix()

  # ARG
  glPushMatrix()
  glTranslatef(-wheel_offset_x, wheel_offset_y, -wheel_offset_z)
  wheel(wheel_size,5)
  glPopMatrix()

  #--------------------------------

'''
 # TODO : create and positioning  (transform) left front wheel 

  # left front wheel
  glPushMatrix()
  glTranslatef(-0.35*size, -0.25*size, 0.35*size)
  wheel(0.2*size)
  glPopMatrix()

  # TODO : create and positioning  (transform) right front wheel 

  glPushMatrix()
  glTranslatef(0.35*size, -0.25*size, 0.35*size)
  wheel(0.2*size)
  glPopMatrix()

  # TODO : create and positioning  (transform) right back wheel

  glPushMatrix()
  glTranslatef(0.35*size, -0.25*size, -0.35*size)
  wheel(0.2*size)
  glPopMatrix()

  # TODO : create and positioning  (transform) left back wheel
  glPopMatrix()  # end car creation

  glPushMatrix()
  glTranslatef(-0.35*size, -0.25*size, -0.35*size)
  wheel(0.2*size)
  glPopMatrix() # end car creation'''

# Robot animation (when robot()implementing to manage arm,forarm rotation)
def animation() :
  global arm,forarm
  arm+=0.5
  forarm+=0.9
  if arm > 90.0 :
    arm=0.0
  if forarm > 90.0 :
    forarm=0.0
  glutPostRedisplay()

def gl_init() :
#  glClearColor(1.0,1.0,1.0,0.0);
  glClearColor(0.5,0.5,0.5,0.0)
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)

def display() :
  global size
  global c_rho,c_phi,c_theta
  global m_theta,m_position
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
  #wcs_lines(2*size)
  wcs_axis(2*size)



  # 1) TODO : use square() from primitives module and place it on Oxz plane
  floor(size*10)

  '''glPushMatrix()
  glRotatef(90, 1, 0, 0)
  floor(size*10)
  glPopMatrix()'''

  # 2) TODO : replace wcs_lines() by wcs_axis()

#ligne 132 fait

  # 3) TODO : replace square() by  floor() from primitives module
  glPushMatrix()  # begin transformation

#done

  # 4) TODO : keyboard interaction on an object (the cone())
  #           use (w,a,s,d) to move object (cone()) on the Oxz plane
  #           with global variables m_theta,m_position (see : on_keyboard_action())
  # Apply keyboard-driven transform: translate on Oxz, then yaw rotate
  '''glTranslatef(m_position[0], 0.0, m_position[2])
  glRotatef(m_theta, 0, 1, 0)
  glColor3f(1,0,0)'''
  r = 0.2*size
  glTranslatef(m_position[0],r,m_position[2])
  glRotatef(m_theta,0,1,0)
  car(size)
  #cone(0.25*size,size)    # object to transform
  #robot(0.25*size,size)    # object to transform

  # 5)TODO : replace cone()  by bone() from  primitives module
  # 6)TODO : replace bone() by robot() and animate with z/Z
  '''glPushMatrix  ()
  glRotatef(90,0,1,0) #(angle, x,y,z
  car(size)    # object to transform
  glPopMatrix()'''

  glPushMatrix  ()
  glRotatef(90,0,0,1) #(angle, x,y,z
  robot(size)    # object to transform
  glPopMatrix()

  # 6)TODO : create the above robot() function (robot with arm,forarm) 
  #          replace bone() by robot() 
  #          use (z/Z) key to animate (arm,forarm) the robot
  # 7)TODO : create the above car() function (car with wheels,bolts) 
  #          replace robot() by  car() and control car and wheels movements
  glPopMatrix()          # end  transformation
  glutSwapBuffers()

def reshape(width,height) :
  glViewport(0,0, width,height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  fovy,ratio,near,far=60.0,width*1.0/height,0.1,50.0
  gluPerspective(fovy,ratio,near,far)

def on_keyboard_action(key,x,y) :
  global m_rho,m_theta
  global w_orientation
  global c_rho,c_phi,c_theta
  speed=0.1
  if key==b'h':
    print("-------------------------------------------") 
    print("Concepteur d'application : Nom-Prenom -----") 
    print("Documentation interaction sur l'application") 
    print("-------------------------------------------") 
    print("h : afficher cette aide ")
    print("q : sortie d'application")
    print("------------------------") 
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
    print("--------------------------------") 
    print("Contrôle directionnel d'un objet")
    print("--------------------------------")
    print("w : Avancer ")
    print("a : Tourner a gauche")
    print("s : Reculer")
    print("d : Tourner a droite")
    print("---------") 
    print("Animation")
    print("---------")
    print("z/Z : lancer/stopper l'animation")
  elif  key== b'z' :  # avancer
    m_rho+=0.1
    m_position[0]+=speed*m_rho*sin(radians(m_theta))
    m_position[2]+=speed*m_rho*cos(radians(m_theta))
    w_orientation-=50
    if w_orientation < -360 :
       w_orientation=360
  elif  key== b'q' :  # à gauche
    m_theta+=5
    m_theta=m_theta%360
  elif  key== b's' : # reculer
    m_rho+=0.1
    m_position[0]-=speed*m_rho*sin(radians(m_theta))
    m_position[2]-=speed*m_rho*cos(radians(m_theta))
    w_orientation+=50
    w_orientation=w_orientation%360
  elif  key== b'd' : # à droite
    m_theta-=5
    if m_theta < -360 :
      m_theta=360
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
  elif key == b'u' :
    c_theta+=5*speed
  elif key == b'U' :
    c_theta-=5*speed
  elif key == b'0' :
    exit(0)
  elif  key== b'w' :
      glutIdleFunc(animation)
  elif  key== b'W' : 
      glutIdleFunc(None)
  else :
    print(f"no interaction on key : {key}")
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
  glutCreateWindow ("REV : Dupond-Dupont")
  glutDisplayFunc(display)
  glutReshapeFunc(reshape)
  glutKeyboardFunc(on_keyboard_action)
  glutSpecialFunc(on_special_keyboard_action)
  glutMainLoop()



'''
          (__)
          (xx)
   /-------\/
  / |     ||
 *  ||----||
    ^^    ^^
 Cow who used Jolt to wash
down psychadelic mushrooms

'''
