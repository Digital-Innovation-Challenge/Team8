# Digital Innovation Challenge 2020 - Team Duckling 
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <img src="https://user-images.githubusercontent.com/62751653/94692773-3b6ac300-0333-11eb-97f3-e245963fea74.jpg" alt="Logo" width="240" height="240">
<h3 align="center">Lecture2Gether</h3>
  <p align="center">
    Bots for the game "Mäxchen" aka Mia.
    <br />
    <br />
    <a href="https://lecture2gether.eu">View Demo</a> <!--TODO DEMO VERLINKEN-->
  </p>
</p>

## About the Project

These are bots for the game "Mäxchen" (aka Mia) developed in the Digital Innovation Challenge 2020. We developed several bots including Machine learning approaches for the lie detection of other players and combining several winning strategies for the announcement of our current roll.

## The Game

The rules for the game "Mäxchen" (aka Mia) are explained in Detail [here](https://en.wikipedia.org/wiki/Mia_(game)).

## Install
You need the [Poetry](https://python-poetry.org/) package manager to install and run our code base.

After you installed Poetry simply type the following commands to clone and install our code:

```
git clone https://github.com/Digital-Innovation-Challenge/Team8.git
cd Team8/src
poetry install
```

After that you are able to join the poetry shell by typing
```
poetry shell
```
or you can run a specific command via
```
poetry run <command>
```

Such commands include

- `python3 bla.py` to run the bla bot TODO
- `python3 bla.py` to run the bla bot TODO


## Technical Infrastructure
The game runs on a remote server (IP: `35.159.50.117`, port: `9000`). 
The players communicate with the server using text-based protocol over UDP (using UTF-8 encoded strings)
We wrapped this protocol to a high level python api.

We also introduced an object oriented hierarchy which allowed us to combine multiple strategies and abstract the server communication on multiple levels. 
Allowing methods like our machine learning based lie detection.

We also added some tools (TODO LINK) to listen to the game traffic, parse it and save them in a structured format. 
This resulted in huge datasets that we used for our machine learning approach.

## Bots

#### Aggressive
- Never accuse except when the previous bot announced 21
- Always announce the maximum of 54, our roll, 
### Weighted Distribution ML
- Use machine learning to determine whether to accuse or not
- If roll is higher than previous, say the truth
- Else choose a random value higher than the previous roll weighted by their probability
### Binomial Distribution ML
- Use machine learning to determine whether to accuse or not
- If roll is higher than previous, say the truth
- Else choose a random value higher than the previous roll based on a binomial distribution


## Machine learning
We used a machine learning model which we created from scratch using [sklearn](https://scikit-learn.org/stable/) and our recorded dataset to predict if the predecessor lies. This worked very well with an accuracy over 0.88 on the test data set (1/3 the size).
The Dataset contains over 100k played rounds. Only game-moves where a player accused another one where used to train the lie detection.  
