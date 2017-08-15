import pyglet,sys,os
from pyglet.window import key,mouse

window = pyglet.window.Window(800,600)

pyglet.clock.set_fps_limit(60)
path = os.path.dirname(sys.argv[0])
imagepath = path +'/images/'

bg = pyglet.image.load(imagepath+'bg5px.gif')
bg.anchor_x,bg.anchor_y = 5,5
adult = pyglet.image.load(imagepath+'flightpic.png')
guypic = pyglet.image.load(imagepath+'swordguy.gif')
slugpic = pyglet.image.load(imagepath+'slug.gif')

xlocs = [100,200,300,400,500]
ylocs = [50,150,250,350,450]

locations = [[(x,y) for y in ylocs] for x in xlocs]
things =[[None for y in range(5)] for x in range(5)]
level = [2]
batch = pyglet.graphics.Batch()
Yourmove = [True]


def turnstart(dt):
    Yourmove[0] = True

Wall = []

def isgood(i,j):
    if 0<=i and i<5 and 0<=j and j<5:
        return True
    return False

class Monster():
    def __init__(self,x,y):
        self.loc = [x, y]
        self.sprite = pyglet.sprite.Sprite(self.pic, x=xlocs[x], y=ylocs[y],batch=batch)
        things[x][y] = self

    def animate(self, dt, velocity):
        print(dt)
        if dt > 0.02:
            dt = 0.015
        self.sprite.x += dt * velocity[0]
        self.sprite.y += dt * velocity[1]

    def arrive(self,dt,newloc):
        pyglet.clock.unschedule(self.animate)
        self.sprite.x = xlocs[newloc[0]]
        self.sprite.y = ylocs[newloc[1]]

    def move(self,dir):
        newx = self.loc[0]+dir[0]
        newy = self.loc[1]+dir[1]
        if 0<= newx and newx< 5 and 0<= newy and newy< 5:
            self.moveto((newx,newy))

    '''def moveto(self,loc):
        prevloc = self.loc
        self.loc = [coord for coord in loc]
        self.sprite.set_position(xlocs[self.loc[0]], ylocs[self.loc[1]])
        things[prevloc[0]][prevloc[1]] = None
        things[loc[0]][loc[1]] = self'''

    def moveto(self,loc):
        prevx,prevy = self.loc
        newx,newy = loc
        self.loc = [newx,newy]
        things[prevx][prevy] = None
        things[loc[0]][loc[1]] = self
        pyglet.clock.schedule_once(self.arrive, 0.2,loc)
        pyglet.clock.schedule(self.animate,
                                       velocity=[5*(xlocs[newx]-xlocs[prevx]), 5*(ylocs[newy]-ylocs[prevy])])

    def adjacents(self):
        x,y = self.loc
        adjacents = []
        for k in [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]:
            i,j = k
            if isgood(i,j):
                adjancents.append([i,j,things[i][j]])

class Slug(Monster):
    def __init__(self,x,y):

        self.pic = slugpic
        Monster.__init__(self, x, y)

    def act(self):
        pass


class Guy(Monster):
    def __init__(self,x,y):
        self.pic = guypic
        Monster.__init__(self,x,y)

    def attackmove(self,dire):
        newx = self.loc[0] + dire[0]
        newy = self.loc[1] + dire[1]
        if 0 <= newx and newx < 5 and 0 <= newy and newy < 5:
            self.attackmoveto([newx,newy])
        #self.attackmoveto([1, 1])

    def attackmoveto(self,z):
        Yourmove[0] = False
        battle = currentstate[0]
        object = things[z[0]][z[1]]
        pyglet.clock.schedule_once(currentstate[0].enemyactions, 0.1)
        pyglet.clock.schedule_once(turnstart, 0.3)
        if object == None:
            # Nothing there
            self.moveto(z)
            pass
        elif object != guy:
            battle.enemies.remove(object)
            object.sprite.delete()
            things[z[0]][z[1]] = None
            if battle.enemies == []:
                print("WOOOO")
                level[0] += 1
                if level[0] > 15:
                   level[0] = 1
                currentstate[0] = Battle(Myarena, level[0])

guy = Guy(0,0)

class Arena():
    def __init__(self,image):
        self.image = image
        self.disallowed = None

Myarena = Arena(bg)

class Battle():
    def __init__ (self,arena = Myarena,enemies = 2):
        self.arena = arena
        guy.moveto([2, 1])
        self.disallowed = arena.disallowed
        self.enemycount = enemies
        self.usedlocs = []
        self.enemies = []
        for i in range(enemies):
            x = i%5
            y = i//5
            self.enemies.append(Slug(x,4-y))

    def enemyactions(self,dt):
        for enemy in self.enemies:
            enemy.act()

currentstate = [Battle()]

def getloc(x,y):
    if x >= 100 and x < 600 and y >= 50 and y < 550:
        return [x//100-1,(y-50)//100]
    return False

def dist(z,z1):
    x = z[0]
    y = z[1]
    x1 = z1[0]
    y1 = z1[1]
    return abs(x-x1)+abs(y-y1)

def diff(z,z1):
    x = z[0]
    y = z[1]
    x1 = z1[0]
    y1 = z1[1]
    return (x-x1),(y-y1)

@window.event
def on_mouse_press(x,y,button,modifiers):
    z = getloc(x,y)
    #battle = currentstate[0]
    if z is not False:
        if dist(z,guy.loc) == 1 and Yourmove[0]:
            guy.attackmoveto(z)

@window.event
def on_key_press(symbol, modifiers):
    if Yourmove[0]:
        if symbol == key.A:
            guy.attackmove((-1, 0))
        elif symbol == key.W:
            guy.attackmove((0,1))
        elif symbol == key.S:
            guy.attackmove((0, -1))
        elif symbol == key.D:
            guy.attackmove((1, 0))

@window.event
def on_draw():
    #print(int(guy.sprite.x),int(guy.sprite.y))
    window.clear()
    battle = currentstate[0]
    battle.arena.image.blit(100,50)
    batch.draw()


pyglet.app.run()