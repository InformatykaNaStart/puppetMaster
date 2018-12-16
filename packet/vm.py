import paramiko
import time


class Vm:
    paramTmpl = {'facility': 'ams1', 'plan': 'baremetal_0', 'operating_system': 'ubuntu_18_04', 'spot_instance': True, 'spot_price_max': 0.07}

    api = None
    id = None
    status = None

    def __init__(self, api):
        self.api = api

    def load(self, id):
        self.id = id
        self.refreshStatus()

    def create(self, project, param, wait = True):
        resp = self.api.call('POST', 'projects/' + project + '/devices', param)
        self.id = resp['id']
        self.status = resp
        if wait:
            while self.status['state'] != 'active':
                time.sleep(1)
                self.refreshStatus()

    def delete(self):
        resp = self.api.call('DELETE', 'devices/' + self.id, {'force_delete': True})

    def refreshStatus(self):
        self.status = self.api.call('GET', 'devices/' + self.id)

    def getIp(self):
        for i in self.status['ip_addresses']:
            if i['address_family'] == 4 and i['public']:
                return i['address']

    def installDocker(self, verbose=False):
        self.execCommand('export DEBIAN_FRONTEND=noninteractive && apt update && apt upgrade -y && apt install -y docker.io', verbose)

    def runDockerContainer(self, image, paramStr='', cmd='', verbose=False, **param):
        for key, val in param.items():
            if len(key) == 1:
                key = '-' + key
            else:
                key = '--' + key
            if not isinstance(val, list):
                val = [val]
            val = [key + ' ' + v for v in val]
            paramStr += ' ' + ' '.join(val)
        command = 'docker run %s %s %s' % (paramStr, image, cmd)
        self.execCommand(command, verbose)

    def execCommand(self, command, verbose=False):
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.client.WarningPolicy())
        client.connect(self.getIp(), username='root')
        if verbose:
            print(command)
        stdin, stdout, stderr = client.exec_command(command)
        for i in stdout:
            if verbose:
                print(i.strip('\n'))
        client.close()

