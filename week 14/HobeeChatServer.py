import socket
from threading import Thread
import time


class CONFIG:
    """

    """
    HOST = 7240
    RSIZE = 1024

    def __init__(self):
        pass


class AutoShutDown(Thread):
    """

    """

    def __init__(self):
        super().__init__()
        pass

    def heartbeat(self):
        """

        :return:
        """
        pass

    def run(self):
        pass


class UserDock(Thread):
    """

    """

    def __init__(self):
        super().__init__()
        pass

    def send(self):
        """

        :return:
        """
        pass

    def receive(self):
        """

        :return:
        """
        pass

    def run(self):
        pass


class Manager:
    """
    """

    def __init__(self, port, maxconn=5):
        self._port = port
        self._maxconn = maxconn
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    @property
    def server(self):
        return self._server

    @property
    def port(self):
        return self._port

    @property
    def maxconn(self):
        return self._maxconn

    def broadcast(self):
        """
        :return:
        """
        pass

    def mention(self):
        """

        :return:
        """
        pass

    def start(self):
        """

        :return:
        """
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(CONFIG.HOST, self.port)
        self.server.listen(self.maxconn)
        print('SERVER is listening on %s' % self.port)
        while True:
            conn, addr = self.server.accept()
            while True:
                try:
                    data = conn.recv(CONFIG.RSIZE)
                    if not data:
                        break
                    print('CLIENT: %s' % data.decode('utf-8'))
                    if data.decode('utf-8') == 'bye':
                        conn.send('再见'.encode('utf-8'))
                        break
                    else:
                        conn.send('收到！'.encode('utf-8'))
                except Exception as e:
                    print('SERVER ERROR: %s' % e)
                    break
            conn.close()
        self.server.close()


def main():
    pass


if __name__ == '__main__':
    pass
