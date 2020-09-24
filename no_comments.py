# https://www.kaggle.com/scorpiontornado/predictive-text-neural-network

### line 3 imports
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
import cv2 as cv


import pickle

import random
###

class Digit:
  def __init__(self, x, y, width, colour, data, height=None, border_width=5):
    self.x = x
    self.y = y
    self.width = width
    self.colour = colour
    self.data = data
    self.height = height # later on, if height is None, it is assigned based on the aspect ratio and the width
    self.border_width = border_width
    
    self.gen_img()

  def gen_img(self):
    self.index = random.choice(range(len(test_x)))
    self.cur_digit = self.data[self.index].reshape([28,28])
    self.cur_digit = self.cur_digit.transpose()

    plt.imshow(self.cur_digit,cmap="Greys") 
    plt.axis("off")
    plt.title(chr(mapping[int(test_y[self.index])]), y=-0.15,color="green")
    plt.savefig("images/transposed_digit.png")

    self.cur_dig_img = pygame.image.load('images/transposed_digit.png').convert()
    self.rect = self.cur_dig_img.get_rect()
    self.cur_dig_img = pygame.transform.scale(self.cur_dig_img, (self.width-self.border_width*2, int((self.rect[3]/self.rect[2])*self.width)-self.border_width*2))
    if not self.height: self.height = int((self.rect[3]/self.rect[2])*self.width) # ternary operator needs an else statement, so I used a single line if statement

    self.rect = self.cur_dig_img.get_rect()
    self.rect = self.rect.move(int(self.x+self.border_width), int(self.y+int((self.height-self.rect[3])/2))) if int((self.height-self.rect[3])/2) > self.border_width else self.rect.move(int(self.x+self.border_width), int(self.y+self.border_width)) # a = b + 2c, c = (a-b)/2 

  def draw(self):
    pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
    screen.blit(self.cur_dig_img, self.rect)

class Button:
  def __init__(self, x, y, width, height, r, colour, string, font, text_colour):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.r = r
    self.colour = colour
    self.string = string
    self.font = font
    self.text_colour = text_colour

    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

  def is_pressed(self, mosuex, mousey, method_to_run, *args, **kwargs):
    self.mousex, self.mousey = mousex, mousey
    if self.rect.collidepoint((self.mousex, self.mousey)):
      method_to_run(*args, **kwargs)
  
  def draw(self):
    pygame.draw.rect(screen, self.colour, (self.rect[0], self.rect[1]+self.r, self.rect[2], self.rect[3]-2*self.r)) #vertically short rect
    pygame.draw.rect(screen, self.colour, (self.rect[0]+self.r, self.rect[1], self.rect[2]-2*self.r, self.rect[3])) #vertically tall rect

    pygame.draw.circle(screen, self.colour, (self.x+self.r, self.y+self.r), self.r) #top left
    pygame.draw.circle(screen, self.colour, (self.x+self.width-self.r, self.y+self.r), self.r) #top right
    pygame.draw.circle(screen, self.colour, (self.x+self.width-self.r, self.y+self.height-self.r), self.r) #bottom right
    pygame.draw.circle(screen, self.colour, (self.x+self.r, self.y+self.height-self.r), self.r) #bottom left

    self.text = self.font.render(self.string, True, self.text_colour)

    self.text = pygame.transform.scale(self.text, (int(self.width*0.8), int(self.height*0.5))) # TODO: keep aspect ratio

    self.text_rect = self.text.get_rect()
    
    self.text_rect.center = (self.x + self.x+self.width)//2, (self.y + self.y+self.height)//2

    screen.blit(self.text, self.text_rect)


### start data science code ###

# Loading and Visualizing Dataset
## Loading emnist-balanced-mapping.txt

mapping = {}

with open("data/emnist-balanced-mapping.txt") as f:
    for line in f.read().split("\n")[:-1]:
        split = line.split()
        mapping[int(split[0])] = int(split[1])
      
## Loading testShort.csv
df_test = pd.read_csv("data/testShort.csv", names=["label"]+["pixel"+str(x) for x in range(784)])

test_x = np.asarray(df_test.iloc[:,1:]).reshape([-1,28,28,1])
test_y = np.asarray(df_test.iloc[:,0]).reshape([-1,1])

## Normalise Pixel Data
# converting pixel values in range [0,1]
test_x = test_x/255


### start pygame code ###
import pygame

pygame.init()

screen_x, screen_y = 420,560

screen = pygame.display.set_mode((screen_x, screen_y)) # iPad Pro 12.9 resolution 3:4
clock = pygame.time.Clock()

done = False

digit = Digit(int((screen_x-200)/2), 100, 200, (0, 0, 0), test_x)
button = Button(int((screen_x-150)/2), digit.y + digit.height + 20, 150, 50, 10, (0, 139, 139), "NEW IMAGE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255))

while not done:
  screen.fill((255, 255, 255))
  # Blit everything to the screen
  digit.draw()
  button.draw()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True 
    elif event.type == pygame.MOUSEBUTTONUP:
      mousex, mousey = event.pos
      button.is_pressed(mousex, mousey, digit.gen_img)

  pygame.display.flip()
  clock.tick(60)