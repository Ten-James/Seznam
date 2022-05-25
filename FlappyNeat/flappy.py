import pygame, random, time, math, os
import numpy
import neat
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



PIPE_GAP = 150

wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

pos = [0,0]

pop = 0

bird_group = []
bird = []
ge= []
nets = []


pygame.mixer.init()

pygame.init()


FONT = pygame.font.Font('freesansbold.ttf', 20)




screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption('NEAT AI ALGORITHM')

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()




class Bird(pygame.sprite.Sprite):

    def __init__(self,index):
        pygame.sprite.Sprite.__init__(self)

        self.index = index
        self.speed = SPEED

        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2



    def update(self):
        self.speed += GRAVITY
        global pos
        # if self.netw.Clac(self.getrelativepos(pos)):
        #     self.bump()
        #UPDATE HEIGHT
        self.rect[1] += self.speed


    def bump(self):
        self.speed = -SPEED

    def isOffScreen(self):
        return self.rect[1] < 0 or self.rect[1] > SCREEN_HEIGHT

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
        if self.rect[1] > 0 and self.rect[0] < SCREEN_WIDHT:
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



def statistics():
    global bird, pop, score, ge
    maxFit = ge[0].fitness
    for g in ge:
        if g.fitness > maxFit:
            maxFit = g.fitness

    text_1 = FONT.render(f'A: {str(len(bird))} G: {pop.generation+1} S: {score} F: {maxFit}', True, (0, 0, 0))
    screen.blit(text_1, (10, 550))

def remove(index):
    bird.pop(index)
    ge.pop(index)
    nets.pop(index)


def eval_genomes(genomes, config):
    global screen, bird_group, bird, ge, nets, pos, score
    bird_group = []
    bird = []
    ge= []
    score = 0
    nets = []
    index = 0
    for genome_id, genome in genomes:
        bird_group.append(pygame.sprite.Group())
        bird.append(Bird(index))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        bird_group[index].add(bird[index])
        index += 1
        genome.fitness = 0


    ground_group = pygame.sprite.Group()

    for i in range (2):
        ground = Ground(GROUND_WIDHT * i)
        ground_group.add(ground)

    pipe_group = pygame.sprite.Group()
    for i in range (2):
        pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])


    last = 0
    clock = pygame.time.Clock()
    while True:
        if len(bird) == 0:
            break
        a =clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        screen.blit(BACKGROUND, (0, 0))

        last += a
        if last >1000:
            for gen in ge:
                gen.fitness += 100
            last = 0

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
            for gen in ge:
                gen.fitness += 1000
            score +=1

        for b in bird:
            bird_group[b.index].update()
        ground_group.update()
        pipe_group.update()

        for b in bird:
            bird_group[b.index].draw(screen)
            pygame.draw.line(screen,(255,0,0),(b.rect[0]+b.rect[2]/2,b.rect[1]+b.rect[3]/2),(pos[0],pos[1]))
        pipe_group.draw(screen)
        ground_group.draw(screen)
        statistics()
        pygame.display.update()

        for i, bi in enumerate(bird):
            output = nets[i].activate(bi.getrelativepos(pos))
            if output[0] > 0.5:
                bi.bump()

            if bi.isOffScreen():
                ge[i].fitness -= 10000
                remove(i)

            if pygame.sprite.groupcollide(bird_group[bi.index], ground_group, False, False, pygame.sprite.collide_mask):
                ge[i].fitness -= 1000
                remove(i)
                
            if pygame.sprite.groupcollide(bird_group[bi.index], pipe_group, False, False, pygame.sprite.collide_mask):
                ge[i].fitness -= abs(bi.getrelativepos(pos)[1])/ 10
                remove(i)
        



def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 1000)


if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__),'config.txt')
    run(config_path)




