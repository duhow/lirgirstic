from socketserver import TCPServer, StreamRequestHandler

class BaseHandler(StreamRequestHandler):
    def _log_command(self):
        print("{}: {}".format(self.client_address[0], self.data))

    def handle(self):
        while True:
            self.data = self.rfile.readline().strip()
            try:
                self.data = self.data.decode('UTF-8')
            except UnicodeDecodeError:
                continue
            if not self.data:
                continue
            self._log_command()
            self._handle_command()
    
    def _write(self, data):
        if isinstance(data, str):
            data = data.encode('UTF-8')
        self.wfile.write(data)
        return self

    def _writeline(self, line: str):
        self._write(f'{line}\n').wfile.flush()

class BaseServer(TCPServer):
    def handle_error(self, request, client_address):
        super().handle_error(request, client_address)
