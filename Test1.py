import pyglet,sys,os
from pyglet.window import key,mouse

window = pyglet.window.Window()

path = os.path.dirname(sys.argv[0])
imagepath = path +'/images/'

egg = pyglet.image.load(imagepath+'eggpic.png')
adult = pyglet.image.load(imagepath +'flightpic.png')
guy = pyglet.image.load(imagepath+'swordguy.gif')
slug = pyglet.image.load(imagepath+'slug.gif')

image = [egg]

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center',anchor_y='center')

xlocs = [200,300,400]
ylocs = [100,200,300]

locations = [[(x,y) for y in ylocs] for x in xlocs]

things =[[slug for y in range(3)] for x in range(3)]


def getloc(x,y):
    if x >= 200 and x < 500 and y >= 100 and y < 400:
        return [x//100-2,y//100-1]
    return False

def dist(z,z1):
    x = z[0]
    y = z[1]
    x1 = z1[0]
    y1 = z1[1]
    return abs(x-x1)+abs(y-y1)

@window.event
def on_mouse_press(x,y,button,modifiers):
    z = getloc(x,y)
    if z:
        if dist(z,guyloc) == 1:
            if things[z[0]][z[1]] == None:
                things[guyloc[0]][guyloc[1]] = None
                things[z[0]][z[1]] = guy
                guyloc[0]=z[0]
                guyloc[1]=z[1]
            elif things[z[0]][z[1]] == slug:
                things[z[0]][z[1]] = None

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.Q:
        image[0] = adult
        print("huzzahhh")
    elif symbol == key.W:
        image[0] = egg

@window.event
def on_draw():
    window.clear()
    image[0].blit(50,50)
    for i in range(3):
        for j in range(3):
            thing = things[i][j]
            if thing is not None:
                things[i][j].blit(*locations[i][j])

guyloc = [1,1]
things[1][1] = guy


pyglet.app.run()