import pygame, sys
from pygame.locals import *
import random
import collections

FPS = 10 #frame per secondo
winwidth = 640
winheight = 480
cellsize = 5
assert winwidth % cellsize == 0, "la larghezza della finestra deve essere un multiplo di cellsize!"
assert winheight % cellsize == 0, "l'altezza della finestra deve essere un multiplo di cellsize!"
largincelle = int(winwidth / cellsize)
altincelle = int(winheight / cellsize)
# set up the colours
nero = (0,  0,  0)
bianco = (255,255,255)
grigio = (220,220,220)
verde = (0,128,128)
violenza = (220,20,60) # cremisi (e portare a 255 il rosso?)
ragione = (0,127,255)  # azzurro
fascino = (223,115,255)# eliotropo,viola
elusione = (255,191,0) # ambra,giallo
filename = "test.txt"
atteggiamenti = ['v','r','e','f']


def drawGrid():
  for x in range(0,winwidth, cellsize):
    pygame.draw.line(DISPLAYSURF, grigio, (x,0),(x,winheight))
  for y in range(0,winheight, cellsize):
    pygame.draw.line(DISPLAYSURF, grigio, (0,y),(winwidth,y))

def blankGrid():
  gridDict ={}
  for y in range (altincelle):
    for x in range (largincelle):
      gridDict[x,y] = 0
  return gridDict

def startingGridRandom(lieDict):
  for cella in lieDict:
    lieDict[cella] = random.choice(atteggiamenti)
  return lieDict

def startingDefinito(lieDict):
    #R-pentomino
    lieDict[48,32] = 'v'
    lieDict[49,32] = 'r'
    lieDict[47,33] = 'e'
    lieDict[48,33] = 'f'
    lieDict[48,34] = 'f'
    return lieDict

def memoGrid(lieDict):
  out_file = open(filename, "w")
  out_file.write(str(lieDict))
  out_file.close()

def colourGrid(item, lieDict):
  x =item[0]
  y =item[1]
  y = y * cellsize # traduce l'array in dimensioni di griglia
  x = x * cellsize # traduce l'array in dimensioni di griglia
  if lieDict[item] == 'v':
    pygame.draw.rect(DISPLAYSURF, violenza, (x, y, cellsize, cellsize))
  elif lieDict[item] == 'r':
    pygame.draw.rect(DISPLAYSURF, ragione, (x, y, cellsize, cellsize))
  elif lieDict[item] == 'e':
    pygame.draw.rect(DISPLAYSURF, elusione, (x, y, cellsize, cellsize))
  elif lieDict[item] == 'f':
    pygame.draw.rect(DISPLAYSURF, fascino, (x, y, cellsize, cellsize))
  else:
    pygame.draw.rect(DISPLAYSURF, bianco, (x, y, cellsize, cellsize))
  return None

def getVicini(item,lieDict):
  vicini = []
  for x in range (-1,2):
    for y in range (-1,2):
      checkCell = (item[0]+x,item[1]+y)
      if checkCell[0] < largincelle and checkCell[0] >= 0:
        if checkCell[1] < altincelle and checkCell[1] >= 0:
          vicini.append(lieDict[checkCell])
  return vicini

def trovaDominatore(vicinato):
  swipe = vicinato
  newSet = set(vicinato)
  temporaneo = list(newSet)
  if len(temporaneo) == 4:
#                contesto = atteggiamenti + temporaneo
#                dominatore = random.choice(contesto)
    contatore = collections.Counter(swipe).most_common(1)
    dominatore = contatore[0][0]
  elif len(temporaneo) == 3:
    if 'v' not in temporaneo:    #this piece of code should be fixed...
      dominatore = 'r'
    elif 'r' not in temporaneo:
      dominatore = 'e'
    elif 'e' not in temporaneo:
      dominatore = 'f'
    elif 'f' not in temporaneo:
      dominatore = 'v'
#       elif len(temporaneo) == 2:    #this piece of code should be fixed...            
    else:
      contesto = atteggiamenti + temporaneo   
      dominatore = random.choice(contesto)
  return dominatore

def tick(lieDict):
  newTick = {}
  for item in lieDict:
    tipoVicini = getVicini(item, lieDict)
    scelta = trovaDominatore(tipoVicini)
#   scelta = random.choice(tipoVicini)
    newTick[item] = scelta
  return newTick

def main():
    pygame.init()
    global DISPLAYSURF
    fpsclock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((winwidth,winheight)) 
    pygame.display.set_caption('Game of lie')
    DISPLAYSURF.fill(bianco)
    lieDict = blankGrid()
#   lieDict = startingGridRandom(lieDict)
    lieDict = startingDefinito(lieDict)
    for cella in lieDict:
      colourGrid(cella,lieDict)
    drawGrid()
#       memoGrid(lieDict)
    pygame.display.update()
    while True: #main game loop
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
      lieDict = tick(lieDict)
      for cella in lieDict:
        colourGrid(cella, lieDict)
      drawGrid()
      pygame.display.update()
      fpsclock.tick(FPS)


if __name__=='__main__':
  main()
