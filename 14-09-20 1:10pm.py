# https://www.kaggle.com/scorpiontornado/predictive-text-neural-network
# https://www.kaggle.com/tarunkr/digit-recognition-tutorial-cnn-99-67-accuracy

### most line 2 imports
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
import cv2 as cv

import pickle

### other line 1 imports
import random

### pygame project imports
import string
import pygame

class Digit:
  def __init__(self, x, y, width, colour, surface, data, values, mapping, height=None, border_width=5):
    self.x = x
    self.y = y
    self.width = width
    self.colour = colour
    self.surface = surface #
    self.data = data
    self.values = values #
    self.mapping = mapping #
    self.height = height # later on, if height is None, it is assigned based on the aspect ratio and the width
    self.border_width = border_width
    
    self.gen_img()

  def gen_img(self):
    self.index = random.choice(range(len(self.data)))
    self.cur_digit = self.data[self.index].reshape([28,28])
    self.cur_digit = self.cur_digit.transpose()

    plt.imshow(self.cur_digit,cmap="Greys") 
    plt.axis("off")
    plt.title(chr(self.mapping[int(self.predict())]), y=-0.15,color="green")
    plt.savefig("images/transposed_digit.png")

    self.cur_dig_img = pygame.image.load('images/transposed_digit.png').convert()
    self.rect = self.cur_dig_img.get_rect()
    self.cur_dig_img = pygame.transform.scale(self.cur_dig_img, (self.width-self.border_width*2, int((self.rect[3]/self.rect[2])*self.width)-self.border_width*2))
    if not self.height: self.height = int((self.rect[3]/self.rect[2])*self.width) # ternary operator needs an else statement, so I used a single line if statement

    self.rect = self.cur_dig_img.get_rect()
    self.rect = self.rect.move(int(self.x+self.border_width), int(self.y+int((self.height-self.rect[3])/2))) if int((self.height-self.rect[3])/2) > self.border_width else self.rect.move(int(self.x+self.border_width), int(self.y+self.border_width)) # a = b + 2c, c = (a-b)/2 

  def predict(self):
    return self.values[self.index]
  
  def draw(self):
    pygame.draw.rect(self.surface, self.colour, (self.x, self.y, self.width, self.height))
    self.surface.blit(self.cur_dig_img, self.rect)

class Button:
  def __init__(self, x, y, width, height, r, colour, string, font, text_colour, surface):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.r = r
    self.colour = colour
    self.string = string
    self.font = font
    self.text_colour = text_colour
    self.surface = surface

    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

  def is_pressed(self, mousex, mousey, method_to_run, *args, **kwargs):
    if self.rect.collidepoint((mousex, mousey)):
      method_to_run(*args, **kwargs)
  
  def draw(self):
    pygame.draw.rect(self.surface, self.colour, (self.rect[0], self.rect[1]+self.r, self.rect[2], self.rect[3]-2*self.r)) #vertically short rect
    pygame.draw.rect(self.surface, self.colour, (self.rect[0]+self.r, self.rect[1], self.rect[2]-2*self.r, self.rect[3])) #vertically tall rect

    pygame.draw.circle(self.surface, self.colour, (self.x+self.r, self.y+self.r), self.r) #top left
    pygame.draw.circle(self.surface, self.colour, (self.x+self.width-self.r, self.y+self.r), self.r) #top right
    pygame.draw.circle(self.surface, self.colour, (self.x+self.width-self.r, self.y+self.height-self.r), self.r) #bottom right
    pygame.draw.circle(self.surface, self.colour, (self.x+self.r, self.y+self.height-self.r), self.r) #bottom left

    self.text = self.font.render(self.string, True, self.text_colour)

    try:
      self.text = pygame.transform.scale(self.text, (int(self.width*0.8), int(self.height*(-1/500*self.text.get_rect()[2]+0.9))))
    except ValueError:
      print("ValueError: Cannot scale to negative size")

    self.text_rect = self.text.get_rect()
    
    self.text_rect.center = (self.x + self.x+self.width)//2, (self.y + self.y+self.height)//2

    self.surface.blit(self.text, self.text_rect)

def append_letter(l, w):
  w.append(l)

def append_word(w, s):
  s.append("".join(w))
  w.clear()

def main():
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

  pygame.init()

  screen_x, screen_y = 420,560
  #screen_x, screen_y = 435, 580 #looks like the largest possible, but I'm not taking any risks in going off screen

  screen = pygame.display.set_mode((screen_x, screen_y)) # iPad Pro 12.9 resolution 3:4
  clock = pygame.time.Clock()

  done = False

  word = []
  sentence = []

  digit = Digit(int((screen_x-200)/2), 20, 200, (0, 0, 0), screen, test_x, test_y, mapping)

  new_img = Button(int((screen_x-150)/2), digit.y + digit.height + 20, 150, 50, 10, (0, 139, 139), "NEW IMAGE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
  select_img = Button(50, new_img.y + new_img.height + 20, 150, 50, 10, (0, 139, 139), "SELECT IMAGE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
  finish_word = Button(screen_x-150-50, new_img.y + new_img.height + 20, 150, 50, 10, (0, 139, 139), "FINISH WORD", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)

  while not done:
    letter = random.choice(string.ascii_lowercase)

    screen.fill((255, 255, 255))
    # Blit everything to the screen
    digit.draw()
    new_img.draw()
    select_img.draw()
    finish_word.draw()

    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(" ".join(sentence) + " " + "".join(word), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (int(screen_x/2), 400)
    screen.blit(text, text_rect)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True 
      elif event.type == pygame.MOUSEBUTTONUP:
        mousex, mousey = event.pos
        new_img.is_pressed(mousex, mousey, digit.gen_img)
        select_img.is_pressed(mousex, mousey, append_letter, letter, word)
        finish_word.is_pressed(mousex, mousey, append_word, word, sentence)

    pygame.display.flip()
    clock.tick(60)

main()