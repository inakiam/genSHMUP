import pygame
from os.path import join as p
from pygame.locals import *

width,height = 640,400


screen = pygame.display.set_mode((width,height),DOUBLEBUF)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.type = type

        if type == 0: #nonlooping / occur-once
            self.rects = [self.rect]
        if type == 1: #tiled
            self.rects = []
            for i in range(-1,width//self.rect.width + 1):
                for j in range(-1,height//self.rect.height + 1):
                    self.rects += [[pygame.Rect((self.rect.left+i*self.rect.width,self.rect.top + j*self.rect.height),
                                               (self.rect.width,self.rect.height)),i,j]]
            print(self.rects)

    def update(self,modX,modY):
        for rect in self.rects:
            rect[0].left = (rect[0].left + modX) % rect[0].width + rect[0].width * rect[1]
            rect[0].top = (rect[0].top + modY) % rect[0].height +  rect[0].height * rect[2]

class Bullet(pygame.sprite.Sprite):

    def __init__(self,pos):
        self.image = pygame.image.load(p('assets','xshipshot.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos
        self.killMe = False

    def update(self):
        self.rect.left += 5
        if self.rect.left > (width + self.rect.width):
            killMe = True

    def draw(self):
        screen.blit(self.image,self.rect)


class Player(pygame.sprite.Sprite):
    mSpeed = 3
    coolDown = 0

    def __init__(self,file,pos):
        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos
        self.shots = []

    def update(self):

        self.coolDown -= 1 if self.coolDown != 0 else 0

        x = 0
        y = 0

        if pygame.key.get_pressed()[K_LEFT]:
            x -= 1
        if pygame.key.get_pressed()[K_RIGHT]:
            x += 1
        if pygame.key.get_pressed()[K_DOWN]:
            y += 1
        if pygame.key.get_pressed()[K_UP]:
            y -= 1
        if pygame.key.get_pressed()[K_x] and not(self.coolDown):
            self.shots += [[Bullet([self.rect.left,self.rect.top]),0]]
            self.coolDown = 10

        for item in self.shots:
            item[0].update()
            if item[0].killMe:
                self.shots.remove(item)
            else: item[0].draw()

        x *= self.mSpeed
        y *= self.mSpeed

        newX = self.rect.left + x
        newY = self.rect.top + y

        if 0 < newX < width - self.rect.width:
            self.rect.left = newX
        if height - self.rect.height > newY > 0:
            self.rect.top = newY

    def draw(self):
        screen.blit(self.image,self.rect)

class Paralaxer(object):
    bg1 = Background(p('assets','bg1.png'), [0, 0],1)
    bg2 = Background(p('assets','bg2.png'), [0, 0],1)
    bg3 = Background(p('assets','bg3.png'), [0, 0],1)
    bg4 = Background(p('assets','bg4.png'), [0, 0],1)
    bgs = [[bg1, 1], [bg2, .49], [bg3, 1/3],[bg4,1/4]][::-1]
    index = 0
    indey = 0

    def __init__(self):
        pass

    def update(self,x,y):

        self.index += x
        self.indey += y

        for bg in self.bgs:
            uX = self.index % round(1/bg[1]) == 0
            uY = (self.indey % round(1/bg[1]) == 0)
            bg[0].update(x if uX else 0,y if uY else 0)

    def draw(self,screen):

        for bg in self.bgs:
            for rect in bg[0].rects:
                screen.blit(bg[0].image,rect[0])


def main():



    

    # bg1 = Background('bg1.png',[0,0])
    # bg2 = Background('bg2.png',[0,0])
    # bg3 = Background('bg3.png',[0,0])

    #bg = [bg1,bg2,bg3][::-1]
    para = Paralaxer()

    player = Player(p('assets','xship.png'),[0,height/2])

    lClock = pygame.time.Clock()


    pygame.display.flip()

    i = 0

    while 1:

        lClock.tick(60)
        i+=1
        x,y = 0,0


        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return None


        para.update(-1,0)
        para.draw(screen)
        player.update()
        player.draw()
        #bg[0].update(x, y)
        #bg[1].update(x, y)
        #bg[2].update(x,y)

        ###for bgs in bg:
           # screen.blit(bgs.image, bgs.rect)


        pygame.display.flip()
        screen.fill((0, 0, 0))


main()
