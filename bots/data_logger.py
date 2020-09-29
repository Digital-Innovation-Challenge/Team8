#! /usr/bin/env python3
import yaml
import logging
from datetime import datetime
from lib.udp import MaexchenUdpClient, MaexchenConnectionError

class Move():
    def __init__(self):
        self._truth = None
        self._announced = None
        self._accused = False
        self._player = None

    def set_truth(self, truth):
        self._truth = truth

    def set_announced(self, announced):
        self._announced = announced

    def set_accused(self, accused):
        self._accused = accused

    def set_player(self, players):
        self._player = players

    def get_truth(self):
        return self._truth

    def get_announced(self):
        return self._announced

    def get_accused(self):
        return self._accused

    def get_player(self):
        return self._player

    def get_lied(self):
        if self.get_truth() is not None and self.get_announced() is not None:
            return self.get_truth() != self.get_announced()

    def serialize(self):
        return {
            "truth": self.get_truth(),
            "announced": self.get_announced(),
            "lied": self.get_lied(),
            "accused": self.get_accused(),
            "player": self.get_player(),
        }


class Round():
    def __init__(self, idx, players):
        self._idx = idx
        self._time = datetime.now()
        self._players = players
        self._moves = []

    def add_move(self, move):
        self._moves.append(move)

    def get_idx(self):
        return self._idx

    def get_time(self):
        return self._time

    def get_players(self):
        return self._players

    def get_moves(self):
        return self._moves

    def serialize(self):
        moves = [move.serialize() for move in self.get_moves()]
        return {
            "round_number": self.get_idx(),
            "time": self.get_time(),
            "players": self.get_players(),
            "moves": moves,
        }


class GameLogger():
    def __init__(self, save_path, spectator_name="Spectator", server_ip="35.159.50.117", server_port=9000, buffer_size=1024):
        """
        Creates a GameLogger.

        :param spectator_name: The name of the spectator.
        :param server_ip: IP of the server.
        :param server_port: Port of the server.
        :param buffer_size: Size of the Buffer.
        """
        self._save_path = save_path
        with open(self._save_path, 'w') as save_file:
                    yaml.dump([], save_file)

        self._udp_client = MaexchenUdpClient()

        # Placeholders
        self._round = None

        # Set or generate the bot name
        if spectator_name:
            self._spectator_name = spectator_name
        else:
            self._spectator_name = \
                ''.join(random.choice(string.ascii_lowercase) for i in range(6))

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

        self.start()

    def start(self):
        """ 
        Start the game for your spectator (non blocking).
        It joins the game on the next possibility.
        """
        print(f"LOGGING DATA to '{self._save_path}'...")
        self._udp_client.send_message(f"REGISTER_SPECTATOR;{self._spectator_name}")
        self._main_loop()

    def close(self):
        """
        Closes the Bots connection.
        """
        print("CLOSING CONNECTION...")
        self._udp_client.send_message("UNREGISTER")
        self._udp_client.close()
        print("CONNECTION CLOSED")
        print(f"LOG DATA saved to '{self._save_path}'")

    def _await_commands(self, cmds):
        while True:
            message = self._udp_client.await_message()
            print(message)
            start = message.split(";")[0]
            if start in cmds:
                return message

    def _listen_move(self):
        message = self._await_commands(["ANNOUNCED", "SCORE"])
        print(message)
        split = message.split(";")
        if split[0] == "SCORE":
            return
        move = Move()
        self._round.add_move(move)
        players = self._round.get_players()
        move.set_player(players[self._current_player_counter])
        move.set_announced(tuple([int(i) for i in split[2].split(",")]))
        self._current_player_counter = (self._current_player_counter + 1) % len(players)

        message = self._await_commands(["ACTUAL DICE", "PLAYER ROLLS", "SCORE"])
        split = message.split(";")
        cmd = split[0]
        if cmd == "SCORE":
            return
        elif cmd == "ACTUAL DICE":
            move.set_accused(True)
            move.set_truth(tuple([int(i) for i in split[1].split(",")]))

        elif cmd == "PLAYER ROLLS":
            self._listen_move()

    def _main_loop(self):
        """
        Runs the main loop which listens for messages from the server.
        """
        while True:
            try:
                message = self._await_commands(["ROUND STARTED"])  # Round started
                print(message)
                idx = message.split(";")[1]
                players = message.split(";")[2].split(",")
                self._round = Round(idx, players)
                self._current_player_counter = 0

                self._listen_move()

                # Round has ended
                round_data = self._round.serialize()
                with open(self._save_path, 'r') as load_file:
                    data = yaml.full_load(load_file)
                data.append(round_data)
                with open(self._save_path, 'w') as save_file:
                    yaml.dump(data, save_file)
            except KeyboardInterrupt:
                self.close()
                exit(0)

if __name__ == "__main__":
    GameLogger("/tmp/mia.yaml", "SpectatorTeam8")
