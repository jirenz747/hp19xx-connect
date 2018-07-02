import pexpect


class ConnectHP19xx:

    def __init__(self, ip_device, login, password, factory_password):
        self._ip_device = ip_device
        self._login = login
        self._password = password
        self._factory_password = factory_password
        self._t = None
        self._connect_hp19xx()

    def _connect_hp19xx(self):
        self._t = pexpect.spawn('ssh -l {} {}'.format(self._login, self._ip_device), timeout=60)
        i = self._t.expect([pexpect.TIMEOUT, pexpect.EOF, 'User Name', '[Pp]assword', '\(yes\/no\)'])
        if i == 0:
            print("* {} - not available".format(self._ip_device))
            self.get_status_connect = False
            return False
        elif i == 1:
            print("* {} - You need to clean the ssh key".format(self._ip_device))
            self.get_status_connect = False
            return False
        elif i == 4:
            self._t.sendline("yes")
            i = self._t.expect(['User Name', '[Pp]assword'])
        if i == 3 or i == 2:
            self._t.sendline(self._password)
        i = self._t.expect(['[Pp]assword', '>', '#'])
        if not (i != 1 or i != 2):
            print("Incorrect password!")
            self.get_status_connect = False
            return False
        self._t.sendline('_cmdline-mode on')
        self._t.expect(['\[Y\/N\]'])
        self._t.sendline('y')
        self._t.expect(['password:'])
        self._t.sendline('{}'.format(self._factory_password))
        i = self._t.expect(['<.+>', 'Error'])
        if i == 1:
            print('Invalid factory password')
            self.get_status_connect = False
            return False
        self._t.sendline('screen-length disable ')
        self._t.expect(['<.+>'])
        self.get_status_connect = True

    def send_hp19xx(self, command, show=False):

        out = self._command_send_expect(command)
        if show is True:
            print(out)
        return out

    def _command_send_expect(self, command):
        self._t.sendline(command)
        i = self._t.expect(['#', '\(Y\/N\)', '<.+>'])
        if i == 1:
            self._t.sendline('y')
            self._t.expect('#')
        lines = str(self._t.before)
        lines = lines.replace('\\r\\n\\r\\n', '\\r\\n').replace('\\r\\n', '\n').replace('\\r', '')
        arr = lines.split('\n')
        arr[0] = command
        arr.pop(-1)
        lines = '\n'.join(arr)
        return lines
