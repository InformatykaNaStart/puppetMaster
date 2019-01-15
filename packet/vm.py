import copy
import logging
import os
import paramiko
import time


class Vm:
    paramTmpl = {'facility': 'ams1', 'plan': 'baremetal_0', 'operating_system': 'ubuntu_18_04', 'spot_instance': True, 'spot_price_max': 0.02}

    api      = None
    id       = None
    status   = None
    ip       = None
    username = None
    log      = None
    maxBid   = 0.02
    bidOver  = 1

    def __init__(self, api=None):
        self.api = api
        self.username = 'root'

    def load(self, id):
        self.id = id
        self.refreshStatus()

    def setBid(self, maxBid, bidOver):
        self.maxBid = maxBid
        self.bidOver = 1 + bidOver if bidOver < 1 else bidOver

    def create(self, project, param, wait=True):
        param = copy.copy(param)

        fullPrice, curPrice = self.api.getPrices(param['facility'], param['plan'])

        if min(curPrice, fullPrice) > self.maxBid:
            raise Exception('prices to high: full %.2f market %.2f' % (fullPrice, curPrice))

        if fullPrice <= curPrice:
            param['spot_instance'] = False
            logging.info('Paying full price %.2f' % fullPrice)
        else:
            param['spot_instance'] = True
            param['spot_price_max'] = min(self.maxBid, curPrice * self.bidOver)
            logging.info('Bidding at %.2f' % param['spot_price_max'])

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
        self.ip = self.getIp()

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
        errors = False
        for i in stderr:
            errors = True
            logging.error(i.strip('\n'))

        client.close()
        return errors

