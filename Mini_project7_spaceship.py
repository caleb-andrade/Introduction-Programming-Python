# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
#missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound = simplegui.load_sound("http://www.sa-matra.net/sounds/starwars/TIE-Fire.wav")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# Additional FX
FX = []
FX.append(simplegui.load_sound("http://www.sa-matra.net/sounds/starwars/Falcon-Fly1.wav"))
FX.append(simplegui.load_sound("http://www.sa-matra.net/sounds/starwars/Falcon-Fly2.wav"))
FX.append(simplegui.load_sound("http://soundbible.com/grab.php?id=1305&type=wav"))
FX.append(simplegui.load_sound("http://www.kiwi-nutz.com/sounds/wav_starwars/swtheme.wav"))
FX.append(simplegui.load_sound("http://www.thesoundarchive.com/starwars/R2D2-yeah.wav"))
FX.append(simplegui.load_sound("http://www.thesoundarchive.com/starwars/R2D2-do.wav"))
FX.append(simplegui.load_sound("http://www.thesoundarchive.com/starwars/R2D2-hey-you.wav"))
FX.append(simplegui.load_sound("http://www.gotwavs.com/0053148414/MP3S/Movies/Star_Wars/knowbett.mp3"))
FX.append(simplegui.load_sound("http://www.gotwavs.com/0053148414/MP3S/Movies/Star_Wars/down.mp3"))
FX.append(simplegui.load_sound("http://www.gotwavs.com/0053148414/MP3S/Movies/Star_Wars/madness.mp3"))

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def fx(n):
    FX[n].play()

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.info = info        
        
    def draw(self,canvas):
        if self.thrust:
            image_center = [135, 45]
        else:
            image_center = self.image_center
        canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        forward = angle_to_vector(self.angle)
        c = 0.008
        
        #updating the position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] > 835:
            self.pos[0] %= 835
            fx(0)
        if self.pos[1] > 635:
            self.pos[1] %= 635
            fx(1)
        if self.pos[0] < -35:
            self.pos[0] = 835
            fx(0)
        if self.pos[1] < -35:
            self.pos[1] = 635
            fx(1)
        
        #updating the velocity
        if self.thrust:
            self.vel[0] += 0.08*forward[0]
            self.vel[1] += 0.08*forward[1]
            
        #updating velocity with friction
        self.vel[0] *= (1-c)
        self.vel[1] *= (1-c)
        
        #updating the angular velocity
        self.angle += self.angle_vel
    
    def LangularVelocity(self):
        self.angle_vel += -0.12
               
    def RangularVelocity(self):
        self.angle_vel += 0.12
        
    def AngleVelOff(self):
        self.angle_vel = 0
                       
    def ThrustOn(self):
        #print "thrust is on"
        self.thrust = True
        ship_thrust_sound.play()
                
    def ThrustOff(self):
        #print "thrust is off"
        self.thrust = False
        ship_thrust_sound.rewind()
        
        
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_vel = [self.vel[0]+5*forward[0], self.vel[1]+5*forward[1]]
        missile_pos = [self.pos[0]+45*forward[0], self.pos[1]+45*forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, self.angle_vel, missile_image, missile_info, missile_sound)

        
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        forward = angle_to_vector(self.angle)
                
        #updating the position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.pos[0] > 835:
            self.pos[0] %= 835
        if self.pos[1] > 635:
            self.pos[1] %= 635
        if self.pos[0] < -35:
            self.pos[0] = 835
        if self.pos[1] < -35:
            self.pos[1] = 635
        
        #updating the angle
        self.angle += self.angle_vel
                

def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw score and remaining lives
    canvas.draw_text("Score: "+str(score), [650, 40], 20, "White")
    canvas.draw_text("Lives: "+str(lives), [50, 40], 20, "White")
      
    
def keydown(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.ThrustOn()
                  
    if key == simplegui.KEY_MAP["right"]:
        my_ship.RangularVelocity()
        fx(random.randint(4,9))
                
    if key == simplegui.KEY_MAP["left"]:
        my_ship.LangularVelocity()
        fx(random.randint(4,9))
                
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    FX[2].rewind()     
        
def keyup(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.ThrustOff()
                  
    if key == simplegui.KEY_MAP["right"]:
        my_ship.AngleVelOff()
                
    if key == simplegui.KEY_MAP["left"]:
        my_ship.AngleVelOff()
    fx(2)
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    pos = [800*random.random(), 600*random.random()]
    vel = [2*random.random()-1, 2*random.random()-1]
    ang = 3.1416*random.random()
    ang_vel = float(2*random.randint(0,10)-10)/100
    a_rock = Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info)

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
fx(2)
fx(3)


# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_missile = Sprite([2-10,-10], [0,0], 0, 0, missile_image, missile_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, -0.1, asteroid_image, asteroid_info)

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()