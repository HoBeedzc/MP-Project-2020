import sys
import socket
import time
from threading import Thread


class ClientConnectError(OSError):
    pass


class CONFIG:
    """

    """
    WELCOME = """\nWelcome to HoBeeChat alpha 0.0.1\nhttps://www.github.com/HoBeedzc\nHave fun!"""
    PORT = 7240
    RSIZE = 1024
    CODE = 'utf-8'
    IP = r'127.0.0.1'

    def __init__(self):
        pass

    @staticmethod
    def time():
        """

        :return:
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return now_time


class Sender(Thread):
    """

    """

    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client
        self.curmessage = None
        pass

    def get_message(self,delay = 0.1):
        """

        :return:
        """
        time.sleep(delay)
        msg = ''
        while msg == '':
            msg = input('>>>:')
        self.curmessage = msg
        pass

    def send(self):
        """

        :return:
        """
        data = self.curmessage.encode(CONFIG.CODE)
        self.client.send(data)
        pass

    def run(self):
        while True:
            self.get_message()
            self.send()
            if self.curmessage == '@exit':
                break
        print('The sender has stopped working...')
        pass


class Receiver(Thread):
    """

    """

    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client
        self.curmessage = None
        pass

    def recv(self):
        """

        :return:
        """
        data = self.client.recv(CONFIG.RSIZE)
        self.curmessage = data.decode(CONFIG.CODE)
        pass

    def show(self):
        """

        :return:
        """
        print(CONFIG.time(), end=' -> ')
        print(self.curmessage)
        pass

    def run(self):
        while True:
            self.recv()
            self.show()
            if self.curmessage == 'SYSTEM: Goodbye.':
                break
        print('The receiver has stopped working...')
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
        print('Client will exit in 0 second.')
        self.client.close()
        pass


def main():
    try:
        ip = sys.argv[1]
    except IndexError:
        ip = CONFIG.IP
    try:
        port = sys.argv[2]
        port = int(port)
    except IndexError:
        port = CONFIG.PORT
    one_client = Chatter(ip, port)
    one_client.start()
    pass


if __name__ == '__main__':
    main()
    pass
