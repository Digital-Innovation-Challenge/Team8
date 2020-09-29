import unittest

import mock

from bots.lib.udp import MaexchenUdpClient, MaexchenConnectionError


class TestUdpClient(unittest.TestCase):
    IP = "127.0.0.1"
    PORT = 9000
    MESSAGE_STRING = "REGISTER;p1;p2;p3"
    DATA = b"REGISTER;p1;p2;p3"
    ERROR_MSG = "error"

    def setUp(self):
        with mock.patch("src.udp.socket.socket") as socket_mock:
            self.socket_mock = socket_mock
            self.client = MaexchenUdpClient(self.IP, self.PORT)

    def test_send_message(self):
        self.client.send_message(self.MESSAGE_STRING)
        self.client._socket.sendto.assert_called_with(self.DATA, (self.IP, self.PORT))

    def test_send_message_socket_error(self):
        with self.assertRaises(MaexchenConnectionError) as assertion_context:
            self.socket_mock.return_value.sendto.side_effect = OSError(self.ERROR_MSG)
            self.client.send_message(self.MESSAGE_STRING)
        self.assert_correct_error_msg(assertion_context)

    def test_await_message(self):
        self.socket_mock.return_value.recvfrom.return_value = (self.DATA, (self.IP, self.PORT))
        self.assertEqual(self.client.await_message(), self.MESSAGE_STRING)

    def test_await_message_socket_error(self):
        with self.assertRaises(MaexchenConnectionError) as assertion_context:
            self.socket_mock.return_value.recvfrom.side_effect = OSError(self.ERROR_MSG)
            self.client.await_message()
        self.assert_correct_error_msg(assertion_context)

    def assert_correct_error_msg(self, assertion_context):
        error_msg = str(assertion_context.exception)
        self.assertTrue(self.IP in error_msg)
        self.assertTrue(str(self.PORT) in error_msg)
