import socket
from threading import Thread
import re
import time


class CONFIG:
    """

    """
    HOST = 7240
    RSIZE = 1024
    CODE = 'utf-8'

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
    def __init__(self, conn, addr):
        super().__init__()
        self._name = "client-" + addr[0] + "-" + str(addr[1])
        self._conn = conn
        self._addr = addr
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name
        pass

    @property
    def conn(self):
        return self._conn

    @property
    def addr(self):
        return self._addr

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
        pass


class Manager:
    """
    """
    def __init__(self, port, maxconn=5):
        self._port = port
        self._maxconn = maxconn
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._users = []
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

    @property
    def users(self):
        return self._users

    def broadcast(self, user: UserDock.name, message):
        """

        :param user:
        :param message:
        :return:
        """
        message = '{}: '.format(user) + message
        print(message)
        for i in self.users:
            if i.name == user:
                continue
            i.conn.send(message.encode(CONFIG.CODE))
        pass

    def mention(self, from_: UserDock.name, to_: UserDock.name, message: str):
        """

        :param from_:
        :param to_:
        :param message:
        :return:
        """
        message = '{}: '.format(from_) + message
        print(message)
        for i in self.users:
            if i.name == to_:
                i.conn.send(
                    'SYSTEM: {} @ you in group chat...'.format(from_).encode(
                        CONFIG.CODE))
                i.conn.send(message.encode(CONFIG.CODE))
        pass

    def access(self, conn: socket.socket, addr: tuple) -> None:
        """

        :param conn:
        :param addr:
        :return:
        """
        temp_user = UserDock(conn, addr)
        temp_user.run()
        self.users.append(temp_user)
        self.broadcast('SYSTEM: {} joins group chat...'.format(temp_user.name))
        pass

    def suspend(self, name: str):
        """

        :return:
        """
        self.broadcast('SYSTEM: {} left the group chat...'.format(name))
        for i in range(len(self.users)):
            if self.users[i].name == name:
                self.users[i].conn.close()
                self.users[i].join()
                del self.users[i]
        pass

    def start(self):
        """

        :return:
        """
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((CONFIG.HOST, self.port))
        self.server.listen(self.maxconn)
        print('SYSTEM: SERVER is listening on %s' % self.port)
        while True:
            conn, addr = self.server.accept()
            self.access(conn, addr)
        # TODO heartbeat
        self.server.close()


class Master(Thread):
    """

    """
    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass


def main():
    pass


if __name__ == '__main__':
    pass
