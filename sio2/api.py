import requests
import json


class Api:
    def __init__(self, address='http://sio2.staszic.waw.pl'):
        self.address = address

    """ returns a dict with two keys:
            'len': number of tasks in the queue
            'time': sum of tasks' time limits, in seconds
    """
    def get_queue_info(self):
        response = requests.get(self.address+'/workers/queue.json')
        if response.status_code != 200:
            raise Exception('%d %s' % (response.status_code, response.reason))
        return json.loads(response.text)
