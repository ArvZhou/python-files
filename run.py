import logging
import os
from utils import get_json
from sync import SyncSchema

project_info = get_json(f'{os.path.dirname(__file__)}/_data/project_info.json')

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
print('Log saved in: ' + os.path.dirname(os.path.abspath(__file__)) + '/sync.log')
logging.basicConfig(filename=f'{os.path.dirname(os.path.abspath(__file__))}/sync.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

SyncSchema(project_info={
    'share': project_info['SHARE_PROJECT'],
    'target': project_info['TARGET_PROJECT']
}).start_sync()

