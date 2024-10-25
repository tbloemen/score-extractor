# Score-extractor

This project aims to solve an issue with scores for large bands.
Usually, scores are listed per song, with all the individual instrument parts being in that folder.
What is more useful, is to have a folder per instrument, where all of your songs go.
This way, you also prevent people who just need to see the parts of their instrument, to get access to all the parts.

## Installation

To install this project, clone this repository to your local machine using `git clone`.
Next, create a directory in this project called "resources", this is where you will put your scores into.
You can also run the script once to let the program generate it for you.
You can place the full folder of scores in this directory, it will automatically handle subdirectories.

[Pipenv](https://pipenv.pypa.io/en/latest/) houses all the dependencies necessary for this project,
and makes sure they are loaded before you run the main file.
To install all dependencies, run the following commands
(assuming you have [pip](https://pypi.org/project/pip/) installed):

```shell
pip install pipenv
pipenv install
```

## Usage

To run the script, run the following:

```shell
pipenv run python main.py
```

The script will create a `results` directory, where the final results will be put.
This script is not perfect, so some instruments won't be recognized.
These parts are put in a separate folder.
