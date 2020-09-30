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

- `python3 bla.py` to run the bla bot
- `python3 bla.py` to run the bla bot


## Technical Infrastructure
The game runs on a remote server (IP: `35.159.50.117`, port: `9000`). 
The players communicate with the server using a simple text-based protocol over UDP (using UTF-8 encoded strings).
You find a more detailed description of the messages sent between client and server [here](./protocol.md). 

## How to join the game?
To join the game, a bot must first register itself with a name. The name must not contain whitespaces, colons, 
semicolons, or commas and can have up to 20 characters. From then on, the bot will receive server messages continuously and can respond to them. 
The server will only accept answers within a narrow time frame (250 ms).

### Join with example bots
We provide you with two very simple bots written in [Java](bots/java/README.md) and [Python](bots/README.md).
How to fire up these bots is described in the respective README.mds. 
Please note that the code of the example bots is not an example for clean code. 
Hence, if you want to build upon it, you should better do some refactorings.

### Join with your own bot
**Here comes the challenge:**
Implement a bot that beats all the others.
You are free to implement your bot using any language of your choice. 
Happy coding!

## How do I know if my bot beats the others?
Every time a bot looses, all other bots earn one point.

We provide you with an example [visualisation](http://andrena.maexchen.spectator.s3-website.eu-central-1.amazonaws.com/build/#/)
of the average points per minute of every participating bot.

Feel free to implement your own graphical representation of the player scores. 
To do this you can register a client as spectator (see [here](./protocol.md)). 
Spectators are not able to actively participate in the game. Yet they will receive all messages every other client would receive.


## References
The idea for this challenge as well as slightly modified code for the server is adapted from https://github.com/conradthukral/maexchen
