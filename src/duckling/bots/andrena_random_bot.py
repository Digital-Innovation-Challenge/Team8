import random

import sys
from duckling.lib.udp import MaexchenUdpClient, MaexchenConnectionError

if __name__ == "__main__":

    random_name = "python-bot-" + str(random.randint(100, 9999))

    udp_client = MaexchenUdpClient()
    register_msg = "REGISTER;" + random_name
    udp_client.send_message(register_msg)
    print("CLIENT->SERVER: ", register_msg)

    while True:
        try:
            message = udp_client.await_message()
            print("SERVER->CLIENT: ", message)

            if message.startswith("ROUND STARTING"):
                token = message.split(";")[1]
                answer = "JOIN;" + token
                udp_client.send_message(answer)
                print("CLIENT->SERVER: ", answer)

            if message.startswith("YOUR TURN"):
                token = message.split(";")[1]
                answer = "SEE;" + token
                udp_client.send_message(answer)
                print("CLIENT->SERVER: ", answer)

        except MaexchenConnectionError as e:
            print(e)

        except KeyboardInterrupt:
            udp_client.send_message("UNREGISTER")
            udp_client.close()
            sys.exit()
