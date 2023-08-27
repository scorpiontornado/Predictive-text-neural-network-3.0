# Predictive-text-neural-network-3.0
Year 10 IST capstone project, combining a neural network to recognise handwritten digits with a markov chain model to predict the current and next words. Originally intended to help individuals that struggle with using a keyboard, but are familiar with handwriting.

FOR BEST PERFORMANCE - replace words_test.txt with a data file of your own, with each word on a separate line. More occurences means the model is more likely to predict that word.
I downloaded my messages from instagram and wrote a simple script to create the required data file, but you could use your own wordlist if wanted. For privacy reasons, I haven't included my instagram messages data file.

## Prerequisites:

- Install python
- Install pip

### Installing python

Optionally, if you have a mac, you can install python with Homebrew, which can be done by following [this guide](https://docs.python-guide.org/starting/install3/osx/).

Homebrew is a useful package manager, and will simplify the install process by automatically installing pip (python's package manager) as well, however macOS should already come with a version of python installed so this is not absolutely necessary.

If you're lazy, this should do it:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python
```

### Installing pip

If you do not install python using Homebrew, you will need to manually install pip.

This can be accomplished by following [this guide](https://ahmadawais.com/install-pip-macos-os-x-python/), but note that easyinstall has been depreciated, so you should follow the updated section up the top of the guide instead.

If you're lazy, this should do it:

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

## Cloning the repo
Follow [this guide](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

TL;DR: navigate to the folder you want to install it into, then run: ```git clone https://github.com/scorpiontornado/Corona-Virus-Website.git``` (note - it will create a project folder for you)

## How to use:

See below for detailed steps

1. Set up a virtual environment
2. run main.py
3. Navigate to the URL given in the terminal

### Setting up a virtual environment:

If it is your first time setting up the virtual environment, run the following to create and activate a virtual environment and install the necessary packages:

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

After the first time - run the following to activate the virtual environment:

```
. venv/bin/activate
```

### Running the project:
Note: main.py is currently outdated. Use draw_pygame.py for the ability to hand-write characters instead of searching for the right image of the character you want.

#### Running draw_pygame.py:
If you want to view the improved version of the project, run draw_pygame.py:

```
python3 draw_pygame.py
```

Depending on your computer's specifications, this code could take more than a minute and a half to run. After this time, it will launch a pygame window.
Press and hold the mouse and move the cursor over the grid to draw the desired character. Due to limitations with pygame, you may need to move the cursor slower than expected in order to avoid gaps in the drawing.

#### Running main.py:
If you want to view the legacy version of the project, run main.py:

```
python3 main.py
```

Depending on your computer's specifications, this code could take more than a minute and a half to run. After this time, it will launch a pygame window.

### Using the product
#### draw_pygame.py (improved)
Upon running the application, you will be greeted with an empty grid, as well as a collection of buttons. From here, you have a few choices:
- To draw a character, press and hold the mouse and move the cursor over the grid.
- When you are finished drawing the character, click the cyan "select image" button to append the letter onto your current word.
- To clear the grid, allowing you to draw a new character, click the cyan "clear" button.
- If you wish to finish the word as it currently is and start a new word, click the cyan "finish word" button.
- If your desired word is in one of the three grey buttons in the middle of the screen, click that button to automatically complete your word to the prediction.
- If you wish to toggle your case (change from lowercase to uppercase or vice versa), click the grey "shift". Note: the first letter will be in uppercase by default, then it will automatically toggle to lowercase.
- If you wish to switch from letters mode to numbers mode (or vice versa), click the "123" button. This will make the model predict numbers rather than letters when you press the cyan "select image" button. Note: by default, the application will be set to letters mode.

#### FOR BEST PERFORMANCE - replace words_test.txt with a data file of your own, with each word on a separate line. More occurences means the model is more likely to predict that word.
I downloaded my messages from instagram and wrote a simple script to create the required data file, but you could use your own wordlist if wanted. For privacy reasons, I haven't included my instagram messages data file.

#### main.py (legacy)
Upon running the application, you will be greeted with an image of a hand-drawn letter (by default, the application will be set to letters mode), as well as a collection of buttons. From here, you have a few choices:
- If the letter is not the one you desire, click cyan "new image" button.
- If you wish to select the image, adding the letter onto your current word, click the cyan "select image" button.
- If you wish to finish the word as it currently is and start a new word, click the cyan "finish word" button.
- If your desired word is in one of the three grey buttons in the middle of the screen, click that button to automatically complete your word to the prediction.
- If you wish to toggle your case (change from lowercase to uppercase or vice versa), click the grey "shift". Note: the first letter will be in uppercase by default, then it will automatically toggle to lowercase.
- If you wish to switch from letters mode to numbers mode (or vice versa), click the "123" button. This will show images of hand-drawn numbers instead of letters, and the model make predictions accordingly.

## Check references.txt for more info
