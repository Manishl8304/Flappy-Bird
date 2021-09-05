import random
import sys
import pygame
from pygame.locals import *
import time

FPS = 32
SCREENWIDTH = 300
SCREENHEIGHT = 500
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
audio_s = {}
images_s = {}


def welcomescreen():

    playerx = int(SCREENWIDTH/15)
    basex = int(0)
    basey = int(SCREENHEIGHT * 0.8)
    playery = int((basey-images_s['player'].get_height())/2)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE):
            maingame()

        else:
            SCREEN.blit(images_s['background'], (0, 0))
            SCREEN.blit(images_s['player'], (playerx, playery))

            SCREEN.blit(images_s['base'], (basex, basey))
            SCREEN.blit(images_s['message'], (70, 100))
            textx = 40
            texty = 450
            font = pygame.font.Font('freesansbold.ttf', 20)
            score = font.render("PRESS SPACE / UP KEY", True, (0, 0, 0))
            SCREEN.blit(score, (textx, texty))
            pygame.display.update()
            FPSCLOCK.tick(FPS)


def maingame():
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerAccY = 1
    playerFlapped = False

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    score = 0

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - images_s['player'].get_height()) / 2)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = -8
                    playerFlapped = True
                    audio_s['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        playerMidPos = playerx + images_s['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + images_s['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                audio_s['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        groundy = int(SCREENHEIGHT * 0.8)

        if playerFlapped:
            playerFlapped = False

        playerHeight = images_s['player'].get_height()
        playery = playery + min(playerVelY, groundy - playery - playerHeight)
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -images_s['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(images_s['background'], (0, 0))

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(images_s['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(images_s['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(images_s['base'], (0, SCREENHEIGHT * 0.8))
        SCREEN.blit(images_s['player'], (playerx, playery))
        myDigits = list(str(score))
        width = 0

        for digit in myDigits:
            width += images_s['number'][int(digit)].get_width()

        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(images_s['number'][int(digit)], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += images_s['number'][int(digit)].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandomPipe():
    pipeHeight = images_s['pipe'][0].get_height()
    offset = SCREENHEIGHT // 3
    y2 = random.randrange(offset, int(SCREENHEIGHT - images_s['base'].get_height()))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
     ]
    return pipe


def isCollide(playerx, playery, upperpipes, lowerpipes):
    pipeHeight = images_s['pipe'][0].get_height()
    pipewidth = images_s['pipe'][0].get_width()

    if playery - 5 < 0 or playery + images_s['player'].get_height() - 5 > (SCREENHEIGHT-images_s['base'].get_height()):
        audio_s['hit'].play()
        time.sleep(2)
        return True

    for pipe in upperpipes:
        if playery < (pipeHeight+pipe['y']) and abs(playerx-pipe['x']) < pipewidth-20:
            audio_s['hit'].play()
            time.sleep(2)

            return True

    for pipe in lowerpipes:
        if playery+images_s['player'].get_height() > pipe['y'] and abs(playerx-pipe['x']) < pipewidth-20:
            audio_s['hit'].play()
            time.sleep(2)

            return True


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird')
    pygame.display.set_icon(pygame.image.load('images_used\\bird.png'))

    audio_s['hit'] = pygame.mixer.Sound('audio_used\\hit.mp3')
    audio_s['point'] = pygame.mixer.Sound('audio_used\\point.mp3')
    audio_s['wing'] = pygame.mixer.Sound('audio_used\\wing.mp3')

    images_s['number'] = (
        pygame.image.load('images_used\\0.png').convert_alpha(),
        pygame.image.load('images_used\\1.png').convert_alpha(),
        pygame.image.load('images_used\\2.png').convert_alpha(),
        pygame.image.load('images_used\\3.png').convert_alpha(),
        pygame.image.load('images_used\\4.png').convert_alpha(),
        pygame.image.load('images_used\\5.png').convert_alpha(),
        pygame.image.load('images_used\\6.png').convert_alpha(),
        pygame.image.load('images_used\\7.png').convert_alpha(),
        pygame.image.load('images_used\\8.png').convert_alpha(),
        pygame.image.load('images_used\\9.png').convert_alpha()
    )
    images_s['background'] = pygame.image.load('images_used\\background1.png').convert()
    images_s['base'] = pygame.image.load('images_used\\base.png').convert_alpha()
    images_s['player'] = pygame.image.load('images_used\\bird.png').convert_alpha()
    images_s['message'] = pygame.image.load('images_used\\message5.jpg').convert_alpha()
    images_s['pipe'] = (
        pygame.transform.rotate(pygame.image.load('images_used\\pipe.png').convert_alpha(), 180),
        pygame.image.load('images_used\\pipe.png').convert_alpha()
    )

    while True:
        welcomescreen()
