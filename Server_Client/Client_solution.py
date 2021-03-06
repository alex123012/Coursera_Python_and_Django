import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)

    def put(self, metric, value, timestamp=None):
        try:
            self.send(metric, value, timestamp)
        except Exception:
            raise ClientError
        data = self.sock.recv(1024).decode('utf8')
        self.check(data)

    def get(self, metric):
        self.sock.send(f'get {metric}\n'.encode('utf8'))
        data = self.sock.recv(1024).decode('utf8')
        exx = data.split('\n')
        # print(exx, exx[0])
        if self.check(data):
            dictir = Client.convert(exx)
            return dictir
        # print(data.decode("utf8"))

    def close(self):
        self.sock.close()

    @staticmethod
    def convert(splt):
        d = {}
        if not splt[1]:
            return d
        splt = splt[1:-2]
        for i in splt:
            tmp = i.split(' ')
            try:
                tup = (int(tmp[2]), float(tmp[1]))
                if tmp[0] in d:
                    d[tmp[0]].append(tup)
                else:
                    d[tmp[0]] = [tup]
            except IndexError:
                raise ClientError
            except TypeError:
                raise ClientError
            except ValueError:
                raise ClientError
        for i in d:
            d[i].sort(key=lambda y: y[0])
        return d

    def send(self, metric, value, timestamp):
        if timestamp is None:
            self.sock.sendall(
                f'put {metric} {value} {int(time.time())}\n'.encode('utf8')
            )
        else:
            self.sock.sendall(
                f'put {metric} {value} {timestamp}\n'.encode('utf8')
            )

    def check(self, data):
        # data = self.sock.recv(1024).decode('utf8').split('\n')
        if data.split('\n')[0] == 'ok':
            return True
        else:
            raise ClientError


class ClientError(Exception):
    pass
