import socket
from threading import Thread
import queue
import re
import time


class CONFIG:
    """

    """
    PORT = 7240
    HOST = r'127.0.0.1'
    RSIZE = 1024
    CODE = 'utf-8'
    WAITTIME = 60
    MAEEAGE_QUEUE = queue.Queue()
    HELP = '''Tips for HoBeeChat...'''

    def __init__(self):
        pass

    @staticmethod
    def time():
        """

        :return:
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return now_time


class AutoShutDown(Thread):
    """

    """

    def __init__(self):
        super().__init__()
        self._flag = True
        pass

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, new_flag: bool):
        self._flag = new_flag

    def heartbeat(self):
        """

        :return:
        """
        time.sleep(CONFIG.WAITTIME)
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
        self.curdata = None
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

    def send(self, message):
        """

        :return:
        """
        self.conn.send(message.encode(CONFIG.CODE))
        pass

    def receive(self):
        """

        :return:
        """
        self.curdata = self.conn.recv(CONFIG.RSIZE).decode(CONFIG.CODE)
        pass

    def process(self):
        """
        """
        data = self.curdata
        if data == 'bye':
            self.send('再见')
        elif data[0] == '@':  # 交互式指令
            data_list = data.split()
            if data_list[0] == '@help':
                self.send(CONFIG.HELP)
            elif data_list[0] == '@name':
                try:
                    self.name = data_list[1]
                    self.send('SYSTEM: Successfully change name to {}...'.format(self.name))
                except AttributeError:
                    self.send('SYSTEM: Name change failed! Please try again.')
            elif data_list[0] == '@exit':
                self.send('SYSTEM: Goodbye.')
            elif data_list[0] == '@check_in':
                self.send('SYSTEM: Check in successfully!')
            elif data_list[0] == '@all':
                # TODO send all message
                all_message = data_list[1]
                self.send('SYSTEM: Successfully send a meaasge to everyone!')
            elif data_list[0] == '@important':
                # TODO send important message
                im_message = data_list[1]
                self.send('SYSTEM: Successfully send an important message to everyone!')
            else:
                to_name = data_list[0][1:]
                to_message = data_list[1]
                self.send('SYSTEM: Successfully send a message to {} '.format(to_name))
                # TODO send_message
        else:
            # TODO send  message
            self.send('SYSTEM: Successfully send a message to group chat!')
        pass

    def run(self):
        while True:
            try:
                self.receive()
                self.process()
            except Exception as e:
                print('SYSTEM: SERVER ERROR: %s' % e)
                break
        pass


class Master(Thread):
    """

    """

    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass


class Manager:
    """
    """

    def __init__(self, host, port, maxconn=5):
        self._port = port
        self._host = host
        self._maxconn = maxconn
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._users = []
        self.curuser = 0
        pass

    @property
    def server(self):
        return self._server

    @property
    def port(self):
        return self._port

    @property
    def host(self):
        return self._host

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
            i.send(message)
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
                i.send('SYSTEM: {} @ you in group chat...'.format(from_))
                i.send(message)
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
        self.curuser += 1
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
        self.curuser -= 1
        pass

    def start(self):
        """

        :return:
        """
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(self.maxconn)
        print('SYSTEM: SERVER is listening on %s' % self.port)
        while True:
            conn, addr = self.server.accept()
            self.access(conn, addr)
        # TODO heartbeat
        self.server.close()


def main():
    pass


if __name__ == '__main__':
    pass
