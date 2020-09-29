Mia protocol
============

Registration
------------
- client->server: `REGISTER;name`
- client->server: `REGISTER_SPECTATOR;name`

Valid names need to satisfy the following criteria:
- no whitespace
- no colons, semicolons, or commas
- up to 20 characters

The server accepts the registration (server->client: `REGISTERED`) if the name is valid and either
- a new client registers for the first time, or
- an existing client re-registers from the same client IP as before (but possibly with a different port; see below).

In case of a successful registration all spectators will be sent the latest score, 0 scores included:

  - server->spectators: `SCORE;playerpoints*` (see below)

In all other cases, the server rejects the registration request (server->client: `REJECTED`).

After a successful registration, the server will send messages to the client using the IP and the port from which the registration message was sent.

Unregistration
--------------
- client->server: `UNREGISTER`
- server->client: `UNREGISTERED`

Heartbeat
---------
Every 2 seconds each client will be sent a "heartbeat" signal from the server, so that it can react when the server (or the communication) dies:

- server->client: `HEARTBEAT`


Round start
-----------

- server->clients: `ROUND STARTING;token`
- client->server: `JOIN;token`

If at least one player participates:
- the server shuffles the participating players
- server->clients: `ROUND STARTED;roundnumber;playernames` (where `playernames` is a ordered, comma separated list of all participating players. The lists order corresponds to how the round is going to be played.)

Else:
- server->clients: `ROUND CANCELED;NO_PLAYERS` (a new round is started immediately)

Rounds with just one player are canceled right after their start: `ROUND CANCELED;ONLY_ONE_PLAYER`


Round actions
-------------
In adherence to the previously announced order:
- server->client: `YOUR TURN;token`
- client->server: `command;token` (where `command` has to be either `ROLL` or `SEE`)

On `ROLL`:
- server->clients: `PLAYER ROLLS;name`
- server->client: `ROLLED;dice;token`
- client->server: `ANNOUNCE;dice';token`
- server->clients: `ANNOUNCED;name;dice`

When Mia is announced, the round ends and the dice are shown. Given Mia was indeed rolled, all players but the announcer lose, otherwise the announcer loses.
- server -> clients: `PLAYER LOST;names;reason` (where `names` is a comma separated list)

On `SEE`:
- Server checks if last announced dice are valid and determines the losing players
- server->clients: `PLAYER WANTS TO SEE;name`
- server->clients: `ACTUAL DICE;dice`
- server->clients: `PLAYER LOST;name;reason`

Whenever a players does not respond in time or does something wrong:
- server->clients: `PLAYER LOST;name;reason`

Every player that has NOT LOST gets a point added to their score.

At the end of each round:
- server->clients: `SCORE;playerpoints` (where `playerpoints` is a comma separated list with entries in the form of `name:points`)

Reasons for losing a round
--------------------------
- `SEE_BEFORE_FIRST_ROLL`: Player wanted to `SEE`, but was first to act (no dice were announced before)
- `LIED_ABOUT_MIA`: Player announced Mia without actually having rolled Mia
- `ANNOUNCED_LOSING_DICE`: Player announced dice that were lower than the previously announced ones
- `DID_NOT_ANNOUNCE`: Player did not announce (in time)
- `DID_NOT_TAKE_TURN`: Player did not announce turn (in time)
- `INVALID_TURN`: Player commanded an invalid turn
- `SEE_FAILED`: Player wanted to `SEE`, but previous player announced dice correctly
- `CAUGHT_BLUFFING`: Player announced higher dice than actually given and the next player wanted to `SEE`
- `MIA`: Mia was announced

