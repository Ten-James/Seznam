import pygame, random, time, math
import numpy
import ai
from pygame.locals import *

#VARIABLES
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 10
GRAVITY = 0.5
GAME_SPEED = 5

score = 0

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

MAXINDEX = 140
GENERATIONSIZE = range(MAXINDEX)
generace = 1
t = [0, 1]


PIPE_GAP = 150

wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

pos = [0,0]






def lerp(a, b, t):
    return (t * a) + ((1-t) * b)



def generateModif(data, rand, index, t, gen_multi):
    if index== 0:
        return data
        
    if index<= 20:
        t = 0.03
    if index>= MAXINDEX -5:
        return rand
    
    modifval = rand.copy()
    for a, z in zip(data, modifval):
        for b, y in zip(a, z):
            for c, x in zip(b, y):
                c = lerp(x, c, t * gen_multi* 0.1* index / MAXINDEX)
    return modifval


pygame.mixer.init()


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.aliveFrom = pygame.time.get_ticks()
        self.Died = 0

        self.netw = ai.Network([6,5,3,1])

        self.dist = 1000
        self.speed = SPEED

        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2



    def update(self):
        self.speed += GRAVITY
        global pos
        if self.netw.Clac(self.getrelativepos(pos)):
            self.bump()
        #UPDATE HEIGHT
        self.rect[1] += self.speed

    def Die(self):
        global pos
        self.Died = pygame.time.get_ticks() - self.aliveFrom
        self.dist = self.getrelativepos(pos)[1]

    def bump(self):
        self.speed = -SPEED

    def isOffScreen(self):
        return self.rect[1] < 0 or self.rect[1] > SCREEN_HEIGHT

    def begin(self, data):
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2
        self.aliveFrom = pygame.time.get_ticks()
        self.Died = 0
        self.netw.setData(data)

    def getrelativepos(self, pos):
        return [pos[0]-self.rect[0],
        pos[1]-self.rect[1],
        1 if pos[1]-self.rect[1] > 0 else 0,
        1 if pos[1]-self.rect[1] < 0 else 0,
         self.rect[1],
          self.speed]




class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self. image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))


        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize


        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        global pos
        self.rect[0] -= GAME_SPEED
        if self.rect[1] > 0:
            pos = [self.rect[0],self.rect[1] - PIPE_GAP /2]
        

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted


def get_ceter_pipes(xpos):
    size = 300
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

activated = []
bird_group = []
bird = []
for i in GENERATIONSIZE:
    bird_group.append(pygame.sprite.Group())
    bird.append(Bird())
    activated.append(1)
    bird_group[i].add(bird[i])


ground_group = pygame.sprite.Group()

for i in range (2):
    ground = Ground(GROUND_WIDHT * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range (2):
    pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])



clock = pygame.time.Clock()

begin = True

while begin:

    clock.tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                begin = False

    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, (120, 150))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)

    ground_group.update()
    for group in bird_group:
        group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()


while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                pass

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDHT - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDHT * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        score += 1

    for group in GENERATIONSIZE:
        if activated[group]:
            bird_group[group].update()
    ground_group.update()
    pipe_group.update()

    for group in GENERATIONSIZE:
        if activated[group]:
            bird_group[group].draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    for ind in GENERATIONSIZE:
        if activated[ind] == 0:
            continue
        if bird[ind].isOffScreen():
            activated[ind] = 0
            bird[ind].Die()

        if (pygame.sprite.groupcollide(bird_group[ind], ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group[ind], pipe_group, False, False, pygame.sprite.collide_mask)):
            activated[ind] = 0
            bird[ind].Die()

        
        if sum(activated) == 0:
            pipe_group.remove(pipe_group.sprites())
            pipes = get_ceter_pipes(SCREEN_WIDHT * 2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])
            alfa = ind
            for b in GENERATIONSIZE:
                if bird[b].Died == bird[alfa].Died:
                    if bird[b].dist < bird[alfa].dist:
                        alfa = b

            data = bird[alfa].netw.getData()
            for i in GENERATIONSIZE:
                bird[i].begin(generateModif(data,bird[alfa].netw.getRandomData(), i, 1, (13 / generace) * numpy.math.sin(generace) +1))
                activated[i] = 1
            t[1] = lerp(t[1],t[0], 0.99)
            generace += 1
            print(f"Skore: {score}\nGenerace: {generace}", end="\t")
            score = 0

