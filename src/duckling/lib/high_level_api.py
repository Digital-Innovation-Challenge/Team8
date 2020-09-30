import logging
import random
import string
import threading

from duckling.lib.udp import MaexchenUdpClient


class MaexchenHighLevelBotAPI(object):
    def __init__(self, bot_name=None, server_ip="35.159.50.117", server_port=9000, buffer_size=1024):
        """
        Creates a HighLevelBotAPI object.

        :param bot_name: The name of the Bot.
        :param server_ip: IP of the server.
        :param server_port: Port of the server.
        :param buffer_size: Size of the Buffer.
        """
        self._udp_client = MaexchenUdpClient()

        # Set or generate the bot name
        if bot_name:
            self._bot_name = bot_name
        else:
            self._bot_name = \
                ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

        # Placeholders
        self._callback = lambda x: None
        self._main_thread = None
        self._stop_main = False
        self._gameplays = []
        self._token = ""

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

    def start(self):
        """ 
        Start the game for your bot (non blocking).
        It joins the game on the next possibility.
        """
        print("--- Starting")
        self._udp_client.send_message(f"REGISTER;{self._bot_name}")
        self._stop_main = False
        self._main_thread = threading.Thread(target=self._main_loop, args=())
        self._main_thread.start()
        print("--- Started")

    def register_callback(self, func):
        """ 
        Register a callback function which is called when its your turn.
        The callback function is called with a tuple of both claimed dice values.
        """
        print("--- Registering callback for bot " + self._bot_name + " to function " + str(func))
        self._callback = func

    def accuse(self):
        """ 
        Accuse the person before of lying.
        Return if the judgment was wright or wrong.
        This is exclusive to the `roll` function.
        """
        print("--- Accusing")
        self._udp_client.send_message(f"SEE;{self._token}")
        while True:
            message = self._udp_client.await_message()
            if message.startswith("PLAYER LOST;"):
                print(message)
                if message.endswith("CAUGHT_BLUFFING"):
                    return True
                if message.endswith("SEE_FAILED"):
                    return False

    def roll(self):
        """
        Rolls your dice. This is exclusive to the `accuse` function.
        """
        print("--- Rolling")
        self._udp_client.send_message(f"ROLL;{self._token}")
        while True:
            message = self._udp_client.await_message()
            if message.startswith("ROLLED;"):
                print(message)
                self._token = message.split(";")[2]
                dice = tuple([int(num) for num in message.split(";")[1].split(",")])
                return dice

    def announce(self, dice):
        """
        Announses a dice roll or lie.
        """
        print("--- Announcing " + str(dice))
        self._udp_client.send_message(f"ANNOUNCE;{dice[0]}, {dice[1]};{self._token}")

    def get_announced(self):
        """
        Retuns a list of all recently announced gameplays.

        :return: List of Tuples with the name and the value tuple.
        """
        return self._gameplays

    def close(self):
        """
        Closes the Bots connection.
        """
        print("--- Closing")
        self._stop_main = True
        self._main_thread.join()
        self._stop_main = False
        self._udp_client.send_message("UNREGISTER")
        self._udp_client.close()

    def _main_loop(self):
        """
        Runs the main loop which listens for messages from the server.
        """
        while not self._stop_main:
            message = self._udp_client.await_message()
            print(message)
            # Join the round
            if message.startswith("ROUND STARTING"):
                #print(message)
                self._token = message.split(";")[1]
                self._udp_client.send_message(f"JOIN;{self._token}")
                self._gameplays = []

            if message.startswith("ANNOUNCED"):
                #print(message)
                split = message.split(";")
                name = split[1]
                dice = tuple([int(num) for num in split[2].split(",")])
                self._gameplays.append((name, dice))

            if message.startswith("YOUR TURN"):
                #print(message)
                self._token = message.split(";")[1]
                if self._gameplays:
                    self._callback(self._gameplays[-1])
                else:
                    self._callback(None)
