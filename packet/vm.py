import logging
import paramiko
import time


class Vm:
    paramTmpl = {'facility': 'ams1', 'plan': 'baremetal_0', 'operating_system': 'ubuntu_18_04', 'spot_instance': True, 'spot_price_max': 0.07}

    api      = None
    id       = None
    status   = None
    ip       = None
    username = None
    log      = None

    def __init__(self, api=None):
        self.api = api
        self.username = 'root'

    def load(self, id):
        self.id = id
        self.refreshStatus()

    def create(self, project, param, wait=True):
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
        if self.ip is not None:
            return self.ip

        for i in self.status['ip_addresses']:
            if i['address_family'] == 4 and i['public']:
                self.ip = i['address']
                return self.ip

    def installDocker(self):
        self.execCommand('export DEBIAN_FRONTEND=noninteractive && apt update && apt upgrade -y && apt install -y docker.io')

    def runDockerContainer(self, image, paramStr='', cmd='', substitute={}):
        substitute['IP'] = self.ip
        for k, v in substitute.items():
            paramStr = paramStr.replace('{%s}' % k, v)
        command = 'docker run %s %s %s' % (paramStr, image, cmd)
        self.execCommand(command)

    def execCommand(self, command):
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        logging.getLogger('paramiko').setLevel(logging.WARNING)
        client.connect(self.ip, username=self.username)
        logging.info(command + '\n')

        stdin, stdout, stderr = client.exec_command(command)
        for i in stdout:
            logging.info(i.strip('\n'))
        client.close()

