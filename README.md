# Digital Innovation Challenge 2020 - andrena objects ag 

## The Game

The rules for the game "Mäxchen" (aka Mia) are explained in Detail [here](https://en.wikipedia.org/wiki/Mia_(game)).

## Technical Infrastructure
The game runs on a remote server (IP: `35.159.50.117`, port: `9000`). 
The players communicate with the server using a simple text-based protocol over UDP (using UTF-8 encoded strings).
You find a more detailed description of the messages sent between client and server [here](./protocol.md). 

## How to join the game?
To join the game, a bot must first register itself with a name. The name must not contain whitespaces, colons, 
semicolons, or commas and can have up to 20 characters. From then on, the bot will receive server messages continuously and can respond to them. 
The server will only accept answers within a narrow time frame (250 ms).

### Join with example bots
We provide you with two very simple bots written in [Java](example-bots/java/README.md) and [Python](example-bots/python/README.md).
How to fire up these bots is described in the respective README.mds. 
<b>Please note that the code in the example bots does not conform to our standards of clean code. If you want to build upon these examples, 
please be aware that the code needs to be refactored.<b>

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