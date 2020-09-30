import socket


class MaexchenUdpClient:

    def __init__(self, server_ip="35.159.50.117", server_port=9000, buffer_size=1024):
        self.__server_port = server_port
        self.__server_ip = server_ip
        self.__buffer_size = buffer_size
        self._socket = socket.socket(
            socket.AF_INET,  # Internet
            socket.SOCK_DGRAM)  # UDP

    def send_message(self, message_string):
        try:
            data = message_string.encode("utf-8")
            address = self.__server_ip, self.__server_port
            self._socket.sendto(data, address)
        except OSError as error:
            raise MaexchenConnectionError(self.__server_ip, self.__server_port, error)

    def await_message(self):
        try:
            data, _ = self._socket.recvfrom(self.__buffer_size)
        except OSError as error:
            raise MaexchenConnectionError(self.__server_ip, self.__server_port, error)

        return data.decode('utf-8')

    def await_commands(self, cmds):
        """
        Waits for one of the given commands. Returns incoming message.

        :param [] cmds: List of commands to wait for
        :return str: Message
        """
        while True:
            message = self.await_message()
            print(message)
            start = message.split(";")[0]
            if start in cmds:
                return message

    def close(self):
        return self._socket.close()


class MaexchenConnectionError(Exception):

    def __init__(self, server_ip, server_port, error):
        message = "Server connection for {}:{} returned error: {}".format(server_ip, server_port, error)
        super().__init__(message)
