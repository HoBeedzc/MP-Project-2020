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
    MESSAGE_QUEUE = queue.Queue()
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


class Message:
    """

    """

    def __init__(self, content, type_, from_, to_=None):
        self._type = type_
        self._from = from_
        self._to = to_
        self._content = content
        self._time = CONFIG.time()

    @property
    def type_(self):
        return self._type

    @property
    def from_(self):
        return self._from

    @property
    def to_(self):
        return self._to

    @property
    def content(self):
        return self._content

    @property
    def time(self):
        return self._time


class AutoShutDown(Thread):
    """

    """

    def __init__(self, server: socket.socket):
        super().__init__()
        self._flag = True
        self._server = server
        pass

    @property
    def server(self):
        return self._server

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
        self.heartbeat()
        if self.flag:
            print('AutoShutDown: SERVER will exit in 0 second.')
            self.server.close()
        pass

    @classmethod
    def timer(cls, server):
        """

        :return:
        """
        temp = cls(server)
        temp.run()
        return temp


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

    @staticmethod
    def put(message: Message):
        """

        :return:
        """
        CONFIG.MESSAGE_QUEUE.put(message)
        pass

    def process(self):
        """
        """
        data = self.curdata
        if data == 'bye':
            self.send('SYSTEM: send @exit to exit.')
            self.put(Message(self.curdata, 'ordinary', self.name))
        elif data[0] == '@':  # 交互式指令
            data_list = data.split()
            if data_list[0] == '@help':
                self.send(CONFIG.HELP)
                self.put(Message(self.curdata, 'option', self.name))
            elif data_list[0] == '@name':
                try:
                    self.name = data_list[1]
                    self.send('SYSTEM: Successfully change name to {}...'.format(self.name))
                    self.put(Message(self.curdata, 'option', self.name))
                except AttributeError:
                    self.send('SYSTEM: Name change failed! Please try again.')
                    self.put(Message(self.curdata, 'option', self.name))
            elif data_list[0] == '@exit':
                self.send('SYSTEM: Goodbye.')
                self.put(Message(self.curdata, 'option', self.name))
            elif data_list[0] == '@check_in':
                self.send('SYSTEM: Check in successfully!')
                self.put(Message(self.curdata, 'option', self.name))
            elif data_list[0] == '@all':
                all_message = data_list[1]
                self.send('SYSTEM: Successfully send a message to everyone!')
                self.put(Message(all_message, 'all', self.name))
            elif data_list[0] == '@important':
                im_message = data_list[1]
                self.send('SYSTEM: Successfully send an important message to everyone!')
                for _ in range(3):
                    self.put(Message(im_message, 'important', self.name))
            else:
                to_name = data_list[0][1:]
                to_message = data_list[1]
                self.send('SYSTEM: Successfully send a message to {} '.format(to_name))
                self.put(Message(to_message, 'mention', self.name, to_name))
        else:
            self.send('SYSTEM: Successfully send a message to group chat!')
            self.put(Message(self.curdata, 'ordinary', self.name))
        pass

    def run(self):
        while True:
            try:
                self.receive()
                self.process()
            except Exception as e:
                print('SYSTEM: SERVER ERROR: %s' % e)
                print('SYSTEM: The connection will close in 1 second...')
                break
        self.put(Message('@exit', 'option', self.name))
        # TODO 在最后一条message发送完成之后再发一个None
        pass


class Master(Thread):
    """

    """

    def __init__(self, server: socket.socket):
        super().__init__()
        self._server = server
        self._users = []
        self.curmessage = None
        pass

    @property
    def server(self):
        return self._server

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

    def get(self):
        """

        :return:
        """
        msg = CONFIG.MESSAGE_QUEUE.get()
        if msg is None:
            return -1
        self.curmessage = msg
        pass

    def process(self):
        """

        :return:
        """
        pass

    def log(self):
        """

        :return:
        """
        pass

    def run(self):
        while True:
            flag = self.get()
            if flag == -1:
                break
            self.process()
            self.log()
        pass


class Manager:
    """

    """

    def __init__(self, host, port, maxconn=5):
        self._port = port
        self._host = host
        self._maxconn = maxconn
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._master = None
        self._timer = None
        self._curuser = 0
        pass

    @property
    def server(self):
        return self._server

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def maxconn(self):
        return self._maxconn

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, new_master):
        self._master = new_master

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, new_timer: AutoShutDown):
        self._timer = new_timer

    @timer.deleter
    def timer(self):
        self._timer = None

    @property
    def curuser(self):
        return self._curuser

    @curuser.setter
    def curuser(self, new_cur):
        self._curuser = new_cur

    def deliver(self):
        """

        :return:
        """
        self.master = Master(self.server)
        self.master.start()
        pass

    def access(self, conn: socket.socket, addr: tuple) -> None:
        """

        :param conn:
        :param addr:
        :return:
        """
        temp_user = UserDock(conn, addr)
        temp_user.run()
        self.master.users.append(temp_user)
        self.master.broadcast('SYSTEM: {} joins group chat...'.format(temp_user.name))
        self.curuser += 1
        if self.curuser == 1:
            print('SYSTEM: Client access, timer will be suspended...')
            self.timer.flag = False
            del self.timer
            self.deliver()
        pass

    def suspend(self, name: str):
        """

        :return:
        """
        self.master.broadcast('SYSTEM: {} left the group chat...'.format(name))
        for i in range(len(self.master.users)):
            if self.master.users[i].name == name:
                self.master.users[i].conn.close()
                self.master.users[i].join()
                del self.master.users[i]
        self.curuser -= 1
        if self.curuser == 0:
            print('SYSTEM: No client connect now! Server will exit in {} seconds.'.format(CONFIG.WAITTIME))
            self.timer = AutoShutDown.timer(self.server)
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
        pass


def main():
    pass


if __name__ == '__main__':
    pass
