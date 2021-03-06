import asyncio

g_storage = {}


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.transport.write(
            self._process(data.decode('utf-8').strip('\r\n')).encode('utf-8')
        )

    def _process(self, command):
        try:
            status, chunks = command.split(' ', 1)
            print(chunks)
            if status == 'get':
                return self._process_get(chunks)
            elif status == 'put':
                return self._process_put(chunks)
            else:
                return 'error\nwrong command\n\n'
        except Exception:
            return 'error\nwrong command\n\n'

    def _process_get(self, chunks):
        key = chunks.split(' ')
        self.check_key(key)
        key = key[0]
        res = 'ok\n'
        if key == '*':
            for key, values in g_storage.items():
                for value in values:
                    res = f'{res}{key} {value[1]} {value[0]}\n'
        else:
            if key in g_storage:
                for value in g_storage[key]:
                    res = f'{res}{key} {value[1]} {value[0]}\n'

        return res + '\n'

    def _process_put(self, chunks):
        key, value, timestamp = chunks.split(' ')
        tr = isinstance(key, str) and isinstance(float(value), float)
        tr = tr and isinstance(int(timestamp), int)
        if not tr:
            return 'error\nwrong command\n\n'
        timestamp = int(timestamp)
        value = float(value)
        if key == '*':
            return 'error\nkey cannot contain *\n\n'
        if key not in g_storage:
            g_storage[key] = list()
        if (timestamp, value) not in g_storage[key]:
            for i in g_storage[key]:
                if timestamp in i:
                    del g_storage[key][g_storage[key].index(i)]
            g_storage[key].append((timestamp, value))
            g_storage[key].sort(key=lambda tup: tup[0])
        return 'ok\n\n'

    def check_key(self, key):
        if not isinstance(key[0], str) or not key[0]:
            raise Exception
        if len(key) > 1:
            raise Exception


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
