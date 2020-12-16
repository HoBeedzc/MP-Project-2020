import socket
from threading import Thread, active_count
import queue
import re
import sys
import time
from functools import wraps


def show_run_state(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Creat a Thread {}'.format(args[0].__class__))
        fun_res = func(*args, **kwargs)
        print('Delete a Thread {}'.format(args[0].__class__))
        return fun_res

    return wrapper


class CONFIG:
    """

    """
    PORT = 7240
    HOST = r'127.0.0.1'
    RSIZE = 1024
    CODE = 'utf-8'
    WAITTIME = 1
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
    def __init__(self, content, type_, subtype, from_, to_=None):
        self._type = type_
        self._subtype = subtype
        self._from = from_
        self._to = to_
        self._content = content
        self._time = CONFIG.time()

    @property
    def type_(self):
        return self._type

    @property
    def subtype(self):
        return self._subtype

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

    # @show_run_state
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
        temp.start()
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

    @staticmethod
    def put_none():
        """

        :return:
        """
        CONFIG.MESSAGE_QUEUE.put(None)
        pass

    def process(self):
        """
        """
        data = self.curdata
        if data == 'bye':
            self.send('[SYSTEM]send @exit to exit.')
            self.put(Message(self.curdata, 'ordinary', 'message', self.name))
            pass
        elif data[0] == '@':  # 交互式指令
            data_list = data.split()
            if data_list[0] == '@help':
                self.send(CONFIG.HELP)
                self.put(Message(self.curdata, 'option', 'help', self.name))
                pass
            elif data_list[0] == '@name':
                try:
                    self.name = data_list[1]
                    self.send(
                        '[SYSTEM]Successfully change name to {}...'.format(
                            self.name))
                    self.put(Message(self.curdata, 'option', 'name',
                                     self.name))
                except IndexError:
                    self.send('[SYSTEM]Name change failed! Please try again.')
                    self.put(
                        Message(self.curdata, 'option', 'failname', self.name))
                pass
            elif data_list[0] == '@exit':
                self.send('[SYSTEM]Goodbye.')
                self.put(Message(self.curdata, 'option', 'exit', self.name))
                self.put_none()
                return -1
            elif data_list[0] == '@check_in':
                self.send('[SYSTEM]Check in successfully!')
                self.put(Message(self.curdata, 'option', 'checkin', self.name))
                pass
            elif data_list[0] == '@all':
                all_message = data_list[1]
                self.send('[SYSTEM]Successfully send a message to everyone!')
                self.put(Message(all_message, 'ordinary', 'all', self.name))
                pass
            elif data_list[0] == '@important':
                im_message = data_list[1]
                self.send(
                    '[SYSTEM]Successfully send an important message to everyone!'
                )
                self.put(
                    Message(im_message, 'ordinary', 'important', self.name))
                pass
            else:
                to_name = data_list[0][1:]
                try:
                    to_message = data_list[1]
                except IndexError:
                    to_message = ''
                self.put(
                    Message(to_message, 'ordinary', 'mention', self.name,
                            to_name))
                pass
        else:
            self.send('[SYSTEM]Successfully send a message to group chat!')
            self.put(Message(self.curdata, 'ordinary', 'message', self.name))
            pass
        pass

    # @show_run_state
    def run(self):
        while True:
            try:
                self.receive()
                flag = self.process()
                if flag == -1:
                    break
            except Exception as e:
                self.send('[SYSTEM]SERVER ERROR: %s' % e)
                self.send('[SYSTEM]The connection will close in 0 second...')
                self.put(Message('@exit', 'option', 'exit', self.name))
                self.put_none()
                break
        pass


class Master(Thread):
    """

    """
    def __init__(self, server: socket.socket, manager):
        super().__init__()
        self._server = server
        self._users = []
        self._manager = manager
        self.curmessage = None
        pass

    @property
    def server(self):
        return self._server

    @property
    def users(self):
        return self._users

    @property
    def manager(self):
        return self._manager

    def curuser(self):
        return len(self.users)

    def broadcast(self, user: UserDock.name, message):
        """

        :param user:
        :param message:
        :return:
        """
        message = '[{}]'.format(user) + message
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
        flag = 1
        message = '[{}]'.format(from_) + message
        for i in self.users:
            if i.name == to_:
                flag = 0
                i.send('[SYSTEM]{} @ you in group chat...'.format(from_))
                i.send(message)
        if flag:
            re_msg = '[SYSTEM]No such user named {}! Please check your input!'.format(
                to_)
        else:
            re_msg = '[SYSTEM]Successfully send a message to {} '.format(to_)
        for i in self.users:
            if i.name == from_:
                i.send(re_msg)
        pass

    def get(self):
        """

        :return:
        """
        msg = CONFIG.MESSAGE_QUEUE.get()
        if msg is None:
            if self.curuser() == 0:
                return -1
            else:
                return 1
        self.curmessage = msg
        pass

    def process(self):
        """

        :return:
        """
        type_ = self.curmessage.type_
        subtype = self.curmessage.subtype
        from_ = self.curmessage.from_
        to_ = self.curmessage.to_
        content = self.curmessage.content
        time_ = self.curmessage.time
        if type_ == 'option':
            if subtype == 'name':
                self.log('[{}][{}] changed name successfully.'.format(
                    time_, from_))
                pass
            elif subtype == 'failname':
                self.log('[{}][{}] failed to change name.'.format(
                    time_, from_))
                pass
            elif subtype == 'help':
                self.log('[{}][{}] viewed help documents.'.format(
                    time_, from_))
                pass
            elif subtype == 'exit':
                self.log('[{}][{}] left the group chat...'.format(
                    time_, from_))
                self.manager.suspend(from_)
                pass
            elif subtype == 'checkin':
                self.log('[{}][{}] checked in...'.format(time_, from_))
                pass
            else:
                self.log('[{}][{}] send an invalid option message subtype: {}'.
                         format(time_, from_, subtype))
                pass
            pass
        elif type_ == 'ordinary':
            if subtype == 'all':
                self.log('[{}][{}] send a message to everyone : {}'.format(
                    time_, from_, content))
                for i in self.users:
                    self.mention(from_, i.name, content)
                pass
            elif subtype == 'important':
                self.log(
                    '[{}][{}] send an important message to group chat : {}'.
                    format(time_, from_, content))
                for _ in range(3):
                    self.broadcast(from_, content)
                pass
            elif subtype == 'mention':
                self.log('[{}][{}] send a message to {} : {}'.format(
                    time_, from_, to_, content))
                self.mention(from_, to_, content)
                pass
            elif subtype == 'message':
                self.log('[{}][{}] send a message to group chat : {}'.format(
                    time_, from_, content))
                self.broadcast(from_, content)
                pass
            else:
                self.log(
                    '[{}][{}] send an invalid ordinary message subtype: {}'.
                    format(time_, from_, subtype))
                pass
            pass
        else:
            self.log('[{}][{}] send an invalid message type: {}'.format(
                time_, from_, type_))
            pass
        pass

    @staticmethod
    def log(message):
        """

        :return:
        """
        print(message)
        with open('.log', 'a+') as f:
            f.write(message)
            f.write('\n')
        pass

    # @show_run_state
    def run(self):
        while True:
            flag = self.get()
            if flag == -1:
                break
            elif flag == 1:
                continue
            self.process()
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

    @staticmethod
    def log(message):
        """

        :return:
        """
        message = '[{}]'.format(CONFIG.time()) + message
        print(message)
        with open('.log', 'a+') as f:
            f.write(message)
            f.write('\n')
        pass

    def deliver(self):
        """

        :return:
        """
        self.master = Master(self.server, self)
        self.master.start()
        pass

    def access(self, conn: socket.socket, addr: tuple) -> None:
        """

        :param conn:
        :param addr:
        :return:
        """
        temp_user = UserDock(conn, addr)
        temp_user.start()
        self.master.users.append(temp_user)
        self.master.broadcast(
            temp_user.name,
            '[SYSTEM]{} joins group chat1...'.format(temp_user.name))
        self.log('[SYSTEM]{} joins group chat...'.format(temp_user.name))
        self.curuser += 1
        if self.curuser == 1:
            if self.timer is None:
                pass
            else:
                print('[SYSTEM]Client access, timer will be suspended...')
                self.timer.flag = False
                del self.timer
                self.deliver()
        pass

    def suspend(self, name: str):
        """

        :return:
        """
        self.master.broadcast(name,
                              '[SYSTEM]{} left the group chat...'.format(name))
        for i in range(len(self.master.users)):
            if self.master.users[i].name == name:
                self.master.users[i].conn.close()
                self.master.users[i].join()
                del self.master.users[i]
                break
        self.curuser -= 1
        if self.curuser == 0:
            print(
                '[SYSTEM]No client connect now! Server will exit in {} seconds.'
                .format(CONFIG.WAITTIME))
            self.timer = AutoShutDown.timer(self.server)
        pass

    def start(self):
        """

        :return:
        """
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(self.maxconn)
        self.log('[SYSTEM]SERVER is listening on %s' % self.port)
        self.deliver()
        while True:
            try:
                conn, addr = self.server.accept()
            except OSError:
                print('[SYSTEM]SERVER will exit in 0 second.')
                break
            self.access(conn, addr)
        pass


def main():
    try:
        host = sys.argv[1]
    except IndexError:
        host = CONFIG.HOST
    try:
        port = sys.argv[2]
        port = int(port)
    except IndexError:
        port = CONFIG.PORT
    one_server = Manager(host, port)
    one_server.start()
    # print(active_count())
    pass


if __name__ == '__main__':
    main()
    # test
    pass
