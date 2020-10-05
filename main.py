# https://www.kaggle.com/scorpiontornado/predictive-text-neural-network
# https://www.kaggle.com/tarunkr/digit-recognition-tutorial-cnn-99-67-accuracy

# most line 2 imports
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
#import cv2 as cv

import pickle

# other line 1 imports
import random

# pygame project imports
import string
import pygame

# import to load the neural network that I made on Kaggle (see line 1)
# from tensorflow import keras
import keras


class Node:
    def __init__(self, prefix):
        """
        Creates a Node with the given string prefix.
        The root node will be given prefix ''.
        You will need to track:
        - the prefix
        - whether this prefix is also a complete word
        - child nodes
        """
        # pass
        self._prefix = prefix
        self._is_word = False
        self.children = {}

    def get_prefix(self):
        """
        Returns the string prefix for this node.
        """
        # pass
        return self._prefix

    def get_children(self):
        """
        Returns a list of child Node objects, in any order.
        """
        # pass
        return [self.children[child] for child in self.children]

    def is_word(self):
        """
        Returns True if this node prefix is also a complete word.
        """
        # pass
        return self._is_word

    def add_word(self, word):
        """
        Adds the complete word into the trie, causing child nodes to be created as needed.
        We will only call this method on the root node, e.g.
        >>> root = Node('')
        >>> root.add_word('cheese')
        """
        # pass
        pointer = len(self._prefix)
        if word[:pointer+1] not in self.children:
            self.children[word[:pointer+1]] = Node(word[:pointer+1])
        if len(word) == pointer+1:
            self.children[word[:pointer+1]]._is_word = True
            return
        else:
            self.children[word[:pointer+1]].add_word(word)

    def find(self, prefix):
        """
        Returns the node that matches the given prefix, or None if not found.
        We will only call this method on the root node, e.g.
        >>> root = Node('')
        >>> node = root.find('te')
        """
        # pass
        pointer = len(self._prefix)
        if prefix == prefix[:pointer+1]:
            # if the child is the word, return the child??
            try:
                return self.children[prefix]
            except KeyError:  # if there is no prefix node
                return None
        if prefix[:pointer+1] not in self.children:
            return None  # if the child is not in the dict, return None
        else:
            # run find on the next child
            return self.children[prefix[:pointer+1]].find(prefix)

    def words(self):
        """
        Returns a list of complete words that start with my prefix.
        The list should be in lexicographical order.
        """
        # pass
        output = []
        if self.is_word():
            # if I am a word, append myself to the output
            output.append(self._prefix)
        if len(self.get_children()) == 0:
            return output  # return the list of words if there are no more children
            # (when it reaches the bottom of recursion)
        for child in self.children:
            output += self.children[child].words()  # otherwise, recurse
            # (add the words of each of the children to the output)

        return sorted(output)


class Char:
    def __init__(self, x, y, width, colour, surface, X_letters, X_digits, y_letters, y_digits, mapping_letters, mapping_digits, height=None, border_width=5):
        self.x = x
        self.y = y
        self.width = width
        self.colour = colour
        self.surface = surface
        self.X_letters = X_letters
        self.X_digits = X_digits
        self.y_letters = y_letters
        self.y_digits = y_digits
        self.mapping_letters = mapping_letters
        self.mapping_digits = mapping_digits
        # later on, if height is None, it is assigned based on the aspect ratio and the width
        self.height = height
        self.border_width = border_width

        # self.state = "letters"
        self.letters = True
        self.uppercase = True
        self.gen_img()

    def gen_img(self):
        if self.letters:
            self.index = random.choice(range(len(self.X_letters)))
            self.cur_digit = self.X_letters[self.index].reshape([28, 28])
            self.cur_digit = self.cur_digit.transpose()
        else:
            self.index = random.choice(range(len(self.X_digits)))
            self.cur_digit = self.X_digits[self.index].reshape([28, 28])
            self.cur_digit = self.cur_digit.transpose()

        plt.imshow(self.cur_digit, cmap="Greys")
        plt.axis("off")
        # plt.title(chr(self.mapping[int(self.predict())]),
        #           y=-0.15, color="green") # removed the values, makes no sense to keep the green label
        plt.savefig("images/transposed_digit.png")

        self.cur_dig_img = pygame.image.load(
            'images/transposed_digit.png').convert()
        self.rect = self.cur_dig_img.get_rect()
        self.cur_dig_img = pygame.transform.scale(
            self.cur_dig_img, (self.width-self.border_width*2, int((self.rect[3]/self.rect[2])*self.width)-self.border_width*2))
        if not self.height:
            # ternary operator needs an else statement, so I used a single line if statement
            self.height = int((self.rect[3]/self.rect[2])*self.width)

        self.rect = self.cur_dig_img.get_rect()
        self.rect = self.rect.move(int(self.x+self.border_width), int(self.y+int((self.height-self.rect[3])/2))) if int(
            (self.height-self.rect[3])/2) > self.border_width else self.rect.move(int(self.x+self.border_width), int(self.y+self.border_width))  # a = b + 2c, c = (a-b)/2

    def predict(self):
        print("Predicting...")
        # return self.data[self.index]
        self.prediction = chr(self.mapping_letters[int(self.y_letters[self.index])]) if self.letters else chr(
            self.mapping_digits[int(self.y_digits[self.index])])
        # return self.prediction.upper() if self.uppercase else self.prediction.lower() # won't allow upper to be set after returning
        self.prediction = self.prediction.upper(
        ) if self.uppercase else self.prediction.lower()
        return self.prediction

    def change_state(self):
        print(f"Before: {self.letters}")
        self.letters = not self.letters
        print(f"After: {self.letters}")
        self.gen_img()

    def change_case(self):
        print(f"Before: {self.uppercase}")
        self.uppercase = not self.uppercase
        print(f"After: {self.uppercase}")

    def set_lowercase(self):
        self.uppercase = False

    def draw(self):
        pygame.draw.rect(self.surface, self.colour,
                         (self.x, self.y, self.width, self.height))
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
            print(f"{self.string} was pressed!")
            method_to_run(*args, **kwargs)

    def draw(self):
        # vertically short rect
        pygame.draw.rect(self.surface, self.colour,
                         (self.rect[0], self.rect[1]+self.r, self.rect[2], self.rect[3]-2*self.r))
        pygame.draw.rect(self.surface, self.colour, (
            self.rect[0]+self.r, self.rect[1], self.rect[2]-2*self.r, self.rect[3]))  # vertically tall rect

        pygame.draw.circle(self.surface, self.colour,
                           (self.x+self.r, self.y+self.r), self.r)  # top left
        pygame.draw.circle(self.surface, self.colour, (self.x +
                                                       self.width-self.r, self.y+self.r), self.r)  # top right
        pygame.draw.circle(self.surface, self.colour, (self.x+self.width -
                                                       self.r, self.y+self.height-self.r), self.r)  # bottom right
        pygame.draw.circle(self.surface, self.colour, (self.x+self.r,
                                                       self.y+self.height-self.r), self.r)  # bottom left
        if self.string:
            self.text = self.font.render(self.string, True, self.text_colour)

            try:
                self.text = pygame.transform.scale(self.text, (int(
                    self.width*0.8), int(self.height*(-1/500*self.text.get_rect()[2]+0.9))))
            except ValueError:
                print("ValueError: Cannot scale to negative size")

            self.text_rect = self.text.get_rect()

            self.text_rect.center = (
                self.x + self.x+self.width)//2, (self.y + self.y+self.height)//2

            self.surface.blit(self.text, self.text_rect)

    def __str__(self):
        return self.string


def append_letter(l, w, *args, method=None, **kwargs):
    w.append(l)
    if method:
        method(*args, **kwargs)


def append_word(w1, w2, s):
    if len(w1) > 0:
        s.append("".join(w1))
        w2.clear()


def predict_words(node, current_word, screen_size, y_coord, surface):
    p_buttons = []
    try:
        predictions = node.find("".join(current_word)).words()
    except AttributeError:  # if no word is found
        predictions = []

    for i in range(3):
        # TODO: make this a formula
        if i == 0:
            x_coord = 15
        elif i == 1:
            x_coord = int((screen_size[0]-120)/2)
        else:
            x_coord = screen_size[0] - 15 - 120

        try:
            p_buttons.append(Button(x_coord, y_coord, 120, 40, 10, (89, 89, 89), predictions[i], pygame.font.Font(
                'freesansbold.ttf', 32), (255, 255, 255), surface))
            print(predictions[i], p_buttons[i])
        except:
            p_buttons.append(Button(x_coord, y_coord, 120, 40, 10, (89, 89, 89),
                                    "", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), surface))
            print(p_buttons[i])
    return p_buttons


def load_map(map_path):
    mapping = {}

    with open(map_path) as f:
        for line in f.read().split("\n")[:-1]:
            split = line.split()
            mapping[int(split[0])] = int(split[1])

    return mapping


def load_data(data_path):
    # df_test = pd.read_csv(data_path, names=["label"]+["pixel"+str(x) for x in range(784)])

    # test_x = np.asarray(df_test.iloc[:, 1:]).reshape([-1, 28, 28, 1])
    # test_y = np.asarray(df_test.iloc[:, 0]).reshape([-1, 1])

    # return test_x, test_y

    df = pd.read_csv(data_path, names=[
                     "label"]+["pixel"+str(x) for x in range(784)])

    X = np.asarray(df.iloc[:, 1:]).reshape([-1, 28, 28, 1])
    y = np.asarray(df.iloc[:, 0]).reshape([-1, 1])

    return X, y


def setup(screen_size):
    ### start data science code ###

    # Loading and Visualizing Dataset
    # Loading emnist-balanced-mapping.txt
    mapping_letters = load_map("data/emnist-letters-mapping.txt")
    mapping_digits = load_map("data/emnist-digits-mapping.txt")

    # Loading testShort.csv
    #test_x, test_y = load_data("data/testShort.csv")

    # Loading training and testing data
    test_x_letters, _ = load_data("data/emnist-letters-test.csv")
    test_x_digits, _ = load_data("data/emnist-digits-test.csv")

    # Normalise Pixel Data
    # converting pixel values in range [0,1]
    test_x_letters = test_x_letters/255
    test_x_digits = test_x_digits/255

    # Load model trained in line 1
    # model = keras.models.load_model('data/model_e20_2')
    model_letters = keras.models.load_model('data/model_letters_e20_2')
    model_digits = keras.models.load_model('data/model_digits_e20_2')
    # test_y = np.argmax(model.predict(test_x),axis =1)
    test_y_letters = np.argmax(model_letters.predict(test_x_letters), axis=1)
    test_y_digits = np.argmax(model_digits.predict(test_x_digits), axis=1)

    ### start predictive text code ###
    with open("data/web2.txt") as f:
        words = f.read().split()
    root = Node('')
    for word in words:
        root.add_word(word)
    print(root.find('friend').words())

    ### start pygame code ###

    pygame.init()

    screen_x, screen_y = screen_size
    # screen_x, screen_y = 435, 580 #looks like the largest possible, but I'm not taking any risks in going off screen

    # iPad Pro 12.9 resolution 3:4
    screen = pygame.display.set_mode((screen_x, screen_y))
    clock = pygame.time.Clock()

    done = False

    current_word = []
    sentence = []
    p_buttons = []

    char = Char(int((screen_x-200)/2), 20, 200, (0, 0, 0),
                screen, test_x_letters, test_x_digits, test_y_letters, test_y_digits, mapping_letters, mapping_digits)

    new_img = Button(15, char.y + char.height + 20, 120, 40, 10, (0, 139, 139),
                     "NEW IMAGE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    select_img = Button(int((screen_size[0]-120)/2), char.y + char.height + 20, 120, 40, 10, (0, 139, 139),
                        "SELECT IMAGE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    finish_word = Button(screen_size[0] - 15 - 120, char.y + char.height + 20, 120, 40, 10, (0, 139, 139),
                         "FINISH WORD", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    shift = Button(char.x/2-90/2, (char.y + (char.y + char.height))/2 - 30/2, 90, 30, 4, (89, 89, 89),
                   "SHIFT", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    to_num = Button((char.x+char.width+screen_x)/2-90/2, (char.y + (char.y + char.height))/2 - 30/2, 90, 30, 4, (89, 89, 89),
                    "123", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)

    return done, screen, clock, current_word, sentence, p_buttons, char, new_img, select_img, finish_word, shift, to_num, model_letters, model_digits, test_x_letters, test_y_letters, test_x_digits, test_y_digits, mapping_letters, mapping_digits, root


def main(screen_size):
    done, screen, clock, current_word, sentence, p_buttons, char, new_img, select_img, finish_word, shift, to_num, model_letters, model_digits, test_x_letters, test_y_letters, test_x_digits, test_y_digits, mapping_letters, mapping_digits, root = setup(
        screen_size)

    ### start main loop ###

    while not done:
        # print(char.uppercase)
        # letter = random.choice(string.ascii_lowercase)

        if not p_buttons:
            p_buttons = predict_words(
                root, current_word, screen_size, new_img.y + new_img.height + 40, screen)

        screen.fill((255, 255, 255))
        # Blit everything to the screen
        char.draw()
        new_img.draw()
        select_img.draw()
        finish_word.draw()
        shift.draw()
        to_num.draw()

        pygame.draw.rect(screen, (192, 192, 192), (0, new_img.y +
                                                   new_img.height + 20, screen_size[0], 40+40))

        for prediction in p_buttons:
            prediction.draw()

        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(" ".join(sentence) + " " +
                           "".join(current_word), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (
            int(screen_size[0]/2), new_img.y + new_img.height + 20 + 40+40+20+text_rect[3]/2)
        screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                print("Mouse up")
                mousex, mousey = event.pos
                new_img.is_pressed(mousex, mousey, char.gen_img)
                # select_img.is_pressed(mousex, mousey, append_letter, letter, current_word)
                select_img.is_pressed(mousex, mousey, append_letter, char.predict(),
                                      current_word, method=char.set_lowercase)
                # https://datascience.stackexchange.com/questions/13461/how-can-i-get-prediction-for-only-one-instance-in-keras
                finish_word.is_pressed(
                    mousex, mousey, append_word, current_word, current_word, sentence)
                shift.is_pressed(
                    mousex, mousey, char.change_case)
                to_num.is_pressed(
                    mousex, mousey, char.change_state)

                for prediction in p_buttons:
                    if prediction.string:
                        prediction.is_pressed(
                            mousex, mousey, append_word, str(prediction), current_word, sentence)

                p_buttons = predict_words(
                    root, current_word, screen_size, new_img.y + new_img.height + 40, screen)
        pygame.display.flip()
        clock.tick(60)


main((420, 560))
