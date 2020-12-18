import sys
import socket
import time
from threading import Thread


class ClientConnectError(OSError):
    pass


class CONFIG:
    """
    some global config and variables
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
        get the local time with the specific format
        :return: the local time with the specific format
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return now_time


class Sender(Thread):
    """
    a class which used to send message to server
    """
    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client
        self.curmessage = None
        pass

    def get_message(self, delay=0.1):
        """
        get message from command line.
        :return: None
        """
        time.sleep(delay)
        msg = ''
        while msg == '':
            print('\r>>>:', end='', flush=True)
            msg = input()
        self.curmessage = msg
        pass

    def send(self):
        """
        send message to server
        :return: None
        """
        data = self.curmessage.encode(CONFIG.CODE)
        self.client.send(data)
        pass

    def log(self):
        """
        log the process
        :return: None
        """
        with open('client.log', 'a+') as f:
            f.write('[{}][ME]'.format(CONFIG.time()) + self.curmessage)
            f.write('\n')
        pass

    def run(self):
        while True:
            self.get_message()
            self.log()
            self.send()
            if self.curmessage == '@exit':
                break
        print('The sender has stopped working...')
        pass


class Receiver(Thread):
    """
    a class used to receive message from server.
    """
    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client
        self.curmessage = None
        pass

    def recv(self):
        """
        receive message from server
        :return: None
        """
        data = self.client.recv(CONFIG.RSIZE)
        self.curmessage = data.decode(CONFIG.CODE)
        pass

    def show(self):
        """
        show message to command line
        :return: None
        """
        print('\r', end='')
        self.log('[{}]'.format(CONFIG.time()) + self.curmessage)
        print('>>>:', end='', flush=True)
        pass

    @staticmethod
    def log(message):
        """
        log the process
        :message: the information you want to log
        :return: None
        """
        print(message)
        with open('client.log', 'a+') as f:
            f.write(message)
            f.write('\n')
        pass

    def run(self):
        while True:
            try:
                self.recv()
            except ConnectionResetError:
                print('The receiver closed by Server...')
                break
            self.show()
            if self.curmessage == '':
                print('The receiver has stopped working...')
                break
        pass


class Chatter:
    """
    Main thread of program
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
        creat a instance for Sender and start it.
        creat a instance for Receiver and start it.
        :return: None
        """
        self.sender = Sender(self.client)
        self.receiver = Receiver(self.client)
        self.sender.start()
        self.receiver.start()
        self.sender.join()
        self.receiver.join()

    def start(self):
        """
        start the client
        :return: None
        """
        print(CONFIG.WELCOME)
        print('>>>:', end='')
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
