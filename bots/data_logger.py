#! /usr/bin/env python3
import yaml
from datetime import datetime
from lib.udp import MaexchenUdpClient, MaexchenConnectionError

class Move():
    def __init__(self):
        self._truth = None
        self._announced = None
        self._lied = None
        self._accused = None

    def set_truth(self, truth):
        self._truth = truth

    def set_announced(self, announced):
        self._announced = announced

    def set_lied(self, lied):
        self._lied = lied

    def set_accused(self, accused):
        self._accused = accused

    def get_truth(self):
        return self._truth

    def get_announced(self):
        return self._announced

    def get_lied(self):
        return self._lied

    def get_accused(self):
        return self._accused

    def serialize(self):
        return {
            "truth": truth,
            "announced": announced,
            "lied": lied,
            "accused": accused,
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

    def get_players(self)
        return self._players

    def get_moves(self):
        return self._moves

    def serialize(self):
        moves = [move.serialize() for move in self._moves]
        return {
            "round_number": self._idx,
            "time": self._time,
            "players": self._players,
            "moves": self._moves,
        }


class GameLogger():
    def __init__(self, save_path, spectator_name="Team8", server_ip="35.159.50.117", server_port=9000, buffer_size=1024):
        """
        Creates a GameLogger.

        :param spectator_name: The name of the spectator.
        :param server_ip: IP of the server.
        :param server_port: Port of the server.
        :param buffer_size: Size of the Buffer.
        """
        self.save_file = open(save_path, 'rw')

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

    def start(self):
        """ 
        Start the game for your spectator (non blocking).
        It joins the game on the next possibility.
        """
        self._udp_client.send_message(f"REGISTER_SPECTATOR;{self._spectator_name}")
        self._main_loop()

    def close(self):
        """
        Closes the Bots connection.
        """
        self._udp_client.send_message("UNREGISTER")
        self._udp_client.close()

    def _await_commands(self, cmds):
        if while True:
            message = self._udp_client.await_message()
            start = message.split(";")[0]
            if start in cmds:
                return message

    def _listen_move(self):
        message = self._await_commands(["YOUR TURN"])
        self._logger.debug(message)
        player = players[current_player_counter]
        current_player_counter = (current_player_counter + 1) % len(players)

        message = self._await_commands(["ROLLED", "SEE"])
        self._logger.debug(message)
        split = message.split(";")
        cmd = split[0]
        if cmd == "ROLLED":
            truth = tuple(split[1].split(","))
            message = self._await_commands(["ANNOUNCED"])
            announced = tuple(message.split(";")[2].split(","))
            lied = truth != announced
            self._round].add_move(truth, announced, lied, False)
            self._listen_move()
        elif cmd == "SEE":
            moves = self._round.get_moves()
            if len(moves) > 0:
                moves[-1]["accused"] = True

    def _main_loop(self):
        """
        Runs the main loop which listens for messages from the server.
        """
        while True:
            message = self._await_commands(["ROUND STARTED"])  # Round started
            self._logger.debug(message)
            idx = message.split(";")[1]
            players = message.split(";")[2].split(",")
            self._round = Round(idx, players)
            current_player_counter = 0

            self._listen_move()

            if message.startswith("SCORE"):  # Round has ended
                self._logger.debug(message)

                if len(self._rounds) > 0:
                    round_data = self._round.serialize()
                    data = yaml.load(self.save_file)
                    data["rounds"].append(round_data)
                    yaml.dump(data, self._save_file)


if __name__ == "__main__":
    GameLogger("/tmp/mia.yaml")
