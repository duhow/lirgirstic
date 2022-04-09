import threading
from time import sleep
from lirgirstic.server import BaseServer, BaseHandler
from lirgirstic import SERVER

class LIRCHandler(BaseHandler):
    def _log_command(self):
        print("{}@LIRC: {}".format(self.client_address[0], self.data))

    def _handle_command(self):
        command = self.data.split(' ')[0].lower()
        if not command:
            return self._response(False, "bad send packet")
        if (
            not command.startswith('_') and
            hasattr(self, command) and
            callable(getattr(self, command))
        ):
            args = self.data.split(' ')[1:]
            #print(f"Calling {command}")
            success, response = getattr(self, command)(args)
            return self._response(success, response)
        #print(f"Command not found: {command}")
        return self._response(False, f'unknown directive: "{self.data}"')

    def _response(self, success: bool = True, data=None):
        self._writeline('BEGIN')

        # LIRC protocol response joins all data
        response = list()
        response.append(self.data)
        response.append('SUCCESS' if success else 'ERROR')
        if data:
            response.append('DATA')
            if not isinstance(data, list):
                data = [data]
            response.append(str(len(data)))
            for line in data:
                response.append(line)
        response.append('END')

        self._writeline('\n'.join(response))

    def version(self, args) -> (bool, str):
        """ Returns the server version """
        return True, SERVER

    def list(self, args) -> (bool, str):
        """ List all the hardware that is available """
        return True, ["example-1", "example-2"]

    def send_once(self, args) -> (bool, str):
        """ Send an IR code """
        if len(args) < 2:
            return False, "Invalid arguments"
        device_id = args[0]
        command   = args[1]
        repeat    = int(payload[2]) if len(payload) > 2 else None
        return self._send_ir_device(device_id, command, repeat)

    def send_ccf_once(self, args) -> (bool, str):
        if len(args) < 2:
            return False, "Invalid arguments"
        repeat = int(args[0])
        command = " ".join(args[1:])
        return self._send_ir_device('default', command, repeat)
        
    def _send_ir_device(self, device, command, repeat):
        return True, ""

        #device  = REGISTRY.find_device(device_id)
        #if device and command:
        #    try:
        #        device.transmit(command, repeat)
        #        self.reply()
        #        return
        #    except ValueError:
        #        pass

def lircd_start(port: int = 8765) -> bool:
    """ Start LIRC thread server """

    lircd = BaseServer(('', port), LIRCHandler, bind_and_activate=False)
    lircd.allow_reuse_address = True
    lircd.server_bind()
    lircd.server_activate()

    lircd_thread = threading.Thread(target=lircd.serve_forever)
    lircd_thread.daemon = True
    lircd_thread.start()

    print(f'LIRC server started on {port=}')
    return True

def main():
    lircd_start()
    while True:
        sleep(0.1)

if __name__ == '__main__':
    main()
