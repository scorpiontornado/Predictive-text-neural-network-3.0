# Predictive-text-neural-network-3.0
Awww yeahhh

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

### Running main.py:

Run main.py:

```
python3 main.py
```

Depending on your computer's specifications, this code could take more than a minute and a half to run. After this time, it will launch a pygame window.

### Using the product
Upon running the application, you will be greeted with an image of a hand-drawn letter (by default, the application will be set to letters mode), as well as a collection of buttons. From here, you have a few choices:
- If the letter is not the one you desire, click cyan "new image" button.
- If you wish to select the image, adding the letter onto your current word, click the cyan "select image" button.
- If you wish to finish the word as it currently is and start a new word, click the cyan "finish word" button.
- If your desired word is in one of the three grey buttons in the middle of the screen, click that button to automatically complete your word to the prediction.
- If you wish to toggle your case (change from lowercase to uppercase or vice versa), click the grey "shift". Note: the first 
- If you wish to switch from letters mode to numbers mode (or vice versa), click the "123" button. This will show images of hand-drawn numbers instead of letters, and the model make predictions accordingly.

## Check references.txt for more info
