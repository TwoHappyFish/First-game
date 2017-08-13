import pyglet,sys
from pyglet.window import key,mouse

window = pyglet.window.Window(800,600)

pyglet.clock.set_fps_limit(60)

egg = pyglet.image.load('/Users/Greg/Documents/Gametesting/eggpic.png')
adult = pyglet.image.load('/Users/Greg/Documents/Gametesting/flightpic.png')
guypic = pyglet.image.load('/Users/Greg/Documents/Gametesting/swordguy.gif')
slugpic = pyglet.image.load('/Users/Greg/Documents/Gametesting/slug.gif')

xlocs = [100,200,300,400,500]
ylocs = [50,150,250,350,450]

locations = [[(x,y) for y in ylocs] for x in xlocs]
things =[[None for y in range(5)] for x in range(5)]
level = [2]
batch = pyglet.graphics.Batch()

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

    def move(self,dir):
        newx = self.loc[0]+dir[0]
        newy = self.loc[1]+dir[1]
        if 0<= newx and newx< 5 and 0<= newy and newy< 5:
            self.moveto((newx,newy))

    def moveto(self,loc):
        prevloc = self.loc
        self.loc = [coord for coord in loc]
        self.sprite.set_position(xlocs[self.loc[0]], ylocs[self.loc[1]])
        things[prevloc[0]][prevloc[1]] = None
        things[loc[0]][loc[1]] = self

    def adjacents(self):
        x,y = self.loc
        adjacents = []
        for k in [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]:
            i,j = k
            if isgood(i,j):
                return [i,j,things[i][j]]

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

    def attackmove(self,dir):
        newx = self.loc[0] + dir[0]
        newy = self.loc[1] + dir[1]
        if 0 <= newx and newx < 5 and 0 <= newy and newy < 5:
            self.attackmoveto((newx,newy))

    def attackmoveto(self,z):
        battle = currentstate[0]
        object = things[z[0]][z[1]]
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

Myarena = Arena(egg)

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
    battle = currentstate[0]
    if z:
        if dist(z,guy.loc) == 1:
            guy.attackmoveto(z)

@window.event
def on_key_press(symbol, modifiers):
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
    window.clear()
    battle = currentstate[0]
    battle.arena.image.blit(100,50)
    batch.draw()


pyglet.app.run()