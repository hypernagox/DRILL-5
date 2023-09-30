import random
from pico2d import *

TUK_WIDTH,TUK_HEIGHT = 1280,1024

open_canvas(1280,1024)

back_ground = load_image('TUK_GROUND.png')
class RandomHand:
    def __init__(self):
        self.pos =[0,0]
        self.handImg = load_image('hand_arrow.png')
        self.pos[0] = random.randint(50, 1280 - 50)
        self.pos[1] = random.randint(52, 1024 - 52)
    def SetRandPos(self):
        self.pos[0] = random.randint(50,1280-50)
        self.pos[1] = random.randint(52,1024-52)
    def Render(self):
        self.handImg.draw(self.pos[0],self.pos[1])

class Boy:
    def __init__(self):
        self.pos = [TUK_WIDTH//2, TUK_HEIGHT//2]
        self.boyImg = load_image('animation_sheet.png')
        self.frame = 0
        self.targetDir = [1,1]
        self.dir = 1
        self.length = 0
        self.speed = 1000
        self.target = RandomHand()
        self.animMap = {
            0 : self.run_right,
            1:  self.run_left
        }
    def run_right(self,frame):
        self.boyImg.clip_draw(frame * 100, 100, 100, 100, self.pos[0], self.pos[1]),
    def run_left(self,frame):
        self.boyImg.clip_draw(frame * 100, 0, 100, 100, self.pos[0], self.pos[1])
    def Update(self):
        dx = self.targetDir[0] * self.speed * 0.02
        dy = self.targetDir[1] * self.speed * 0.02
        self.pos[0] += dx
        self.pos[1] += dy
        self.length -= math.sqrt(dx ** 2 + dy ** 2)
    def Render(self):
        self.animMap[self.dir](self.frame)
        self.frame = (self.frame + 1) % 8
    def CheckArrive(self):
        if 0 >= self.length:
            self.target.SetRandPos()
            dx = self.target.pos[0] - self.pos[0]
            dy = self.target.pos[1] - self.pos[1]
            self.length = math.sqrt(dx ** 2 + dy ** 2)
            self.targetDir[0] = dx / self.length
            self.targetDir[1] = dy / self.length
            if self.targetDir[0] > 0 :
                self.dir = 0
            else:
                self.dir = 1
            self.frame = 0

def handle_event():
    for eve in get_events():
        if eve.type == SDL_KEYDOWN:
            if eve.key == SDLK_ESCAPE:
                return False
    return True
boy = Boy()
hand = RandomHand()
boy.target = hand

while handle_event():
    back_ground.draw(TUK_WIDTH//2,TUK_HEIGHT//2)
    boy.Update()
    hand.Render()
    boy.Render()
    update_canvas()
    boy.CheckArrive()
    clear_canvas()
    delay(0.02)
