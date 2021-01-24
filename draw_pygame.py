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

    # w stands for wallaby
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
    def __init__(self, start_x, start_y, cols, rows, cell_width, cell_height, model_letters, model_digits, mapping_letters, mapping_digits, surface):
        self.start_x = start_x
        self.start_y = start_y
        self.cols = cols
        self.rows = rows
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.model_letters = model_letters
        self.model_digits = model_digits
        self.mapping_letters = mapping_letters
        self.mapping_digits = mapping_digits
        self.surface = surface

        # self.state = "letters"
        self.letters = True
        self.uppercase = True
        self.prediction = " "

        self.end_x = self.start_x + self.cols * \
            self.cell_width  # should equal 200 for this example
        self.end_y = self.start_y + self.rows * self.cell_height

        self.width = self.start_x - self.end_x
        self.height = self.start_y - self.end_y

        # initialise the grid with all 0s
        self.grid = [[0 for i in range(cols)] for i in range(rows)]

    def fill(self, input_x, input_y):
        if (input_x >= self.start_x and input_x <= self.end_x) and (input_y >= self.start_y and input_y <= self.end_y):
            index_x = (input_x - self.start_x) // self.cell_width
            if index_x >= self.cols:
                index_x = self.cols - 1

            index_y = (input_y - self.start_y) // self.cell_height
            if index_y >= self.rows:
                index_y = self.rows - 1

            # set current cell
            self.grid[index_y][index_x] = 1

            # set surrounding cells if not offscreen or already filled
            # left
            if index_x - 1 >= 0 and self.grid[index_y][index_x - 1] == 0:
                self.grid[index_y][index_x - 1] = 0.5
            # right
            if index_x + 1 < self.cols and self.grid[index_y][index_x + 1] == 0:
                self.grid[index_y][index_x + 1] = 0.5
            # up
            if index_y - 1 >= 0 and self.grid[index_y - 1][index_x] == 0:
                self.grid[index_y - 1][index_x] = 0.5
            # down
            if index_y + 1 < self.rows and self.grid[index_y + 1][index_x] == 0:
                self.grid[index_y + 1][index_x] = 0.5

            # print(f"Set ({index_x}, {index_y}) to 1")

    def predict(self):
        print("Predicting...")
        char = np.asarray(self.grid).reshape(
            [1, self.cols, self.rows, 1]).transpose()

        if self.letters:
            prediction = np.argmax(self.model_letters.predict(char), axis=1)
            prediction = chr(self.mapping_letters[int(prediction)])
        else:
            prediction = np.argmax(self.model_digits.predict(char), axis=1)
            prediction = chr(self.mapping_digits[int(prediction)])

        prediction = prediction.upper() if self.uppercase else prediction.lower()

        print(f"prediction: {prediction}")
        self.clear()
        return prediction

    def clear(self):
        # for row in self.grid:
        #     for cell in row:
        #         print(f"Before: {cell}")
        #         cell = 0
        #         print(f"After: {cell}")

        self.grid = [[0 for i in range(self.cols)] for i in range(self.rows)]
        # print("Grid cleared")

        # print the grid # debugging
        # print("[")
        # for row in self.grid:
        #     print(f"  {row},")
        # print("]")

    def change_state(self):
        print(f"Before: {self.letters}")
        self.letters = not self.letters
        print(f"After: {self.letters}")
        # self.gen_img()

    def change_case(self):
        print(f"Before: {self.uppercase}")
        self.uppercase = not self.uppercase
        print(f"After: {self.uppercase}")

    def set_lowercase(self):
        self.uppercase = False

    def draw(self):
        # pygame.draw.rect(self.surface, self.colour,
        #                 (self.x, self.y, self.width, self.height))

        #self.surface.blit(self.cur_dig_img, self.rect)

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                # draw border:
                x = self.start_x + j * self.cell_width
                y = self.start_y + i * self.cell_height
                pygame.draw.rect(self.surface, (0, 0, 0), (x, y,
                                                           self.cell_width, self.cell_height))

                # if cell == 0:
                #     pygame.draw.rect(self.surface, (255, 255, 255), (x + 0.1 * self.cell_width, y + 0.1 *
                #                                                      self.cell_height, self.cell_width * 0.8, self.cell_height * 0.8))
                pygame.draw.rect(self.surface, (255 - (255 * cell), 255 - (255 * cell), 255 - (255 * cell)), (x +
                                                                                                              0.1 * self.cell_width, y + 0.1 * self.cell_height, self.cell_width * 0.8, self.cell_height * 0.8))


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

        # testing
        # pygame.draw.circle(self.surface, (0, 0, 0), (self.x+self.r,
        #                                             self.y+self.height-self.r), self.r)  # bottom left
        # pygame.draw.circle(self.surface, self.colour,
        #                   (0, 400), 50)  # bottom left

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

        #print("Drew button")
        # pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, 100, 100))  # testing

    def __str__(self):
        return self.string


# def append_letter(l, w, *args, method=None, **kwargs):
#     w.append(l)
#     if method:
#         method(*args, **kwargs)

def append_letter(l, w, method_before=None, method_after=None):
    if method_before:
        l = method_before()
    w.append(l)
    if method_after:
        method_after()


def append_word(w1, w2, s):
    if len(w1) > 0:
        s.append("".join(w1))
        w2.clear()


def backspace_word(w, s):
    if w != []:
        w.pop()


def predict_words(node, current_word, screen_size, y_coord, surface):
    p_buttons = []
    try:
        predictions = node.find("".join(current_word)).words()
    except AttributeError:  # if no word is found
        predictions = []

    for i in range(3):
        # TODO: make this a formula
        if i == 0:
            x_coord = 20
        elif i == 1:
            x_coord = int((screen_size[0]-120)/2)
        else:
            x_coord = screen_size[0] - 20 - 120

        try:
            p_buttons.append(Button(x_coord, y_coord, (screen_size[0]-(20*4))/3, ((screen_size[0]-(20*4))/3)/3, 10, (89, 89, 89), predictions[i], pygame.font.Font(
                'freesansbold.ttf', 32), (255, 255, 255), surface))
            print(predictions[i], p_buttons[i])
        except:
            p_buttons.append(Button(x_coord, y_coord, (screen_size[0]-(20*4))/3, ((screen_size[0]-(20*4))/3)/3, 10, (89, 89, 89),
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


# https://www.pygame.org/wiki/TextWrap
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


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
    mouse_down = False

    current_word = []
    sentence = []
    p_buttons = []

    # width: 200
    char = Char(int((screen_x-200)/2), 20, 28, 28, int(200/28), int(200/28),
                model_letters, model_digits, mapping_letters, mapping_digits, screen)

    # new_img = Button(20, char.y + char.height + 20, 120, 40, 10, (0, 139, 139),
    #                  "NEW IMAGE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    # new_img = Button(20, char.start_y + char.height + 20, (screen_size[0]-(20*4))/3, ((screen_size[0]-(20*4))/3)/3, 10, (0, 139, 139),
    #                  "NEW IMAGE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)

    # clear = Button(20, char.start_y + char.height + 20, (screen_size[0]-(20*4))/3, ((screen_size[0]-(20*4))/3)/3, 10, (0, 139, 139),
    #                "CLEAR", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    # select_img = Button(int((screen_size[0]-120)/2), char.start_y + char.height + 20, (screen_size[0]-(20*4))/3, ((screen_size[0]-(20*4))/3)/3, 10, (0, 139, 139),
    #                     "SELECT IMAGE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    # finish_word = Button(screen_size[0] - 20 - 120, char.start_y + char.height + 20, (screen_size[0]-(20*4))/3, ((screen_size[0]-(20*4))/3)/3, 10, (0, 139, 139),
    #                      "FINISH WORD", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)

    # shift = Button(char.start_x/2-90/2, (char.start_y + (char.start_y + char.height))/2 - 30/2, 90, 30, 4, (89, 89, 89),
    #                "SHIFT", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    # to_num = Button((char.start_x+char.width+screen_x)/2-90/2, (char.start_y + (char.start_y + char.height))/2 - 30/2, 90, 30, 4, (89, 89, 89),
    #                 "123", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)

    clear = Button(20, 20 + 200 + 20, (screen_size[0]-(20*4))/3, ((screen_size[0]-(20*4))/3)/3, 10, (0, 139, 139),
                   "CLEAR", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    select_img = Button(int((screen_size[0]-120)/2), 20 + 200 + 20, (screen_size[0]-(20*4))/3, ((screen_size[0]-(20*4))/3)/3, 10, (0, 139, 139),
                        "SELECT IMAGE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    finish_word = Button(screen_size[0] - 20 - 120, 20 + 200 + 20, (screen_size[0]-(20*4))/3, ((screen_size[0]-(20*4))/3)/3, 10, (0, 139, 139),
                         "FINISH WORD", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)

    shift = Button(110/2-90/2, (20 + (20 + 200))/2 - 30/2, 90, 30, 4, (89, 89, 89),
                   "SHIFT", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    backspace = Button(110/2-90/2, (20 + (20 + 200))/2 - 30/2 + 30 + 15, 90, 30, 4, (89, 89, 89),
                       "BACKSPACE", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)
    to_num = Button((110+200+screen_x)/2-90/2, (20 + (20 + 200))/2 - 30/2, 90, 30, 4, (89, 89, 89),
                    "123", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)

    # test = Button(200, 350, 90, 30, 4, (89, 89, 89),
    #              "TEST", pygame.font.Font('freesansbold.ttf', 32), (255, 255, 255), screen)

    return done, mouse_down, screen, clock, current_word, sentence, p_buttons, char, clear, select_img, finish_word, shift, backspace, to_num, model_letters, model_digits, test_x_letters, test_y_letters, test_x_digits, test_y_digits, mapping_letters, mapping_digits, root


def main(screen_size):
    done, mouse_down, screen, clock, current_word, sentence, p_buttons, char, clear, select_img, finish_word, shift, backspace, to_num, model_letters, model_digits, test_x_letters, test_y_letters, test_x_digits, test_y_digits, mapping_letters, mapping_digits, root = setup(
        screen_size)

    ### start main loop ###

    while not done:
        # print(char.uppercase)
        # letter = random.choice(string.ascii_lowercase)

        if not p_buttons:
            p_buttons = predict_words(
                root, current_word, screen_size, clear.y + clear.height + 40, screen)

        screen.fill((255, 255, 255))
        # Blit everything to the screen
        char.draw()
        # new_img.draw()
        clear.draw()
        select_img.draw()
        finish_word.draw()
        shift.draw()
        backspace.draw()
        to_num.draw()
        # test.draw()

        pygame.draw.rect(screen, (192, 192, 192), (0, clear.y +
                                                   clear.height + 20, screen_size[0], 40+40))

        for prediction in p_buttons:
            prediction.draw()

        font = pygame.font.Font('freesansbold.ttf', 16)
        # text = font.render(" ".join(sentence) + " " +
        #                    "".join(current_word), True, (0, 0, 0))
        # text_rect = text.get_rect()
        # text_rect.center = (
        #     int(screen_size[0]/2), new_img.y + new_img.height + 20 + 40+40+20+text_rect[3]/2)
        # screen.blit(text, text_rect)
        drawText(screen, " ".join(sentence) + " " + "".join(current_word), (0, 0, 0), (20, clear.y + clear.height +
                                                                                       20 + 40+40+20, screen_size[0]-20-20, screen_size[1]-clear.y + clear.height + 20 + 40+40+20-20), font)

        mousex, mousey = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                # to be doubly sure.. this is how it was before and idk if changing it to pygame.mouse.get_pos will break the buttons
                mousex, mousey = event.pos
                mouse_down = False
                print("Mouse up")
                clear.is_pressed(mousex, mousey, char.clear)
                # select_img.is_pressed(mousex, mousey, append_letter, letter, current_word)
                select_img.is_pressed(mousex, mousey, append_letter, "",
                                      current_word, method_before=char.predict, method_after=char.set_lowercase)
                # https://datascience.stackexchange.com/questions/13461/how-can-i-get-prediction-for-only-one-instance-in-keras
                finish_word.is_pressed(
                    mousex, mousey, append_word, current_word, current_word, sentence)
                shift.is_pressed(
                    mousex, mousey, char.change_case)
                backspace.is_pressed(
                    mousex, mousey, backspace_word, current_word, sentence)
                to_num.is_pressed(
                    mousex, mousey, char.change_state)

                for prediction in p_buttons:
                    if prediction.string:
                        prediction.is_pressed(
                            mousex, mousey, append_word, str(prediction), current_word, sentence)

                p_buttons = predict_words(
                    root, current_word, screen_size, clear.y + clear.height + 40, screen)

        if mouse_down:
            char.fill(mousex, mousey)

        #pygame.draw.rect(screen, (0, 0, 0), (0, 200, 100, 100))
        pygame.display.flip()
        clock.tick(60)


main((420, 560))
