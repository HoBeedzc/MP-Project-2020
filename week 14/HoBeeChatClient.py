import socket
from threading import Thread


class ClientConnectError(OSError):
    pass


class CONFIG:
    """

    """
    WELCOME = """\nWelcome to HoBeeChat alpha 0.0.1\nhttps://www.github.com/HoBeedzc\nHave fun!"""
    PORT = 7240
    IP = r'127.0.0.1'

    def __init__(self):
        pass


class Sender(Thread):
    """

    """

    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client
        pass

    def run(self):
        pass


class Receiver(Thread):
    """

    """

    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client
        pass

    def run(self):
        pass


class Master(Thread):
    """

    """

    def __init__(self):
        super().__init__()
        pass


class Chatter:
    """
    """

    def __init__(self, ip, port):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ip = ip
        self._port = port
        self.sender = None
        self.receiver = None
        pass

    @property
    def client(self):
        return self._client

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    def deliver(self):
        """

        :return:
        """
        self.sender = Sender(self.client)
        self.receiver = Receiver(self.client)
        self.sender.start()
        self.receiver.start()
        self.sender.join()
        self.receiver.join()

    def start(self):
        """

        :return:
        """
        self.client.connect((self.ip, self.port))
        self.deliver()
        self.client.close()
        pass


def main():
    print(CONFIG.WELCOME)
    print('start')
    pass


if __name__ == '__main__':
    main()
    pass
