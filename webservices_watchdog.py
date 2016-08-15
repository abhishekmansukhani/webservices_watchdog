# -*- coding: utf-8 -*-

import time
import uptime
import logging
from urllib.error import URLError
import urllib.request
import subprocess

webservices = {'webservice_name':   
                   {   'address': 'http://localhost:8001/', 
                    'executable': 'C:\\path\\to\\startup_script.vbs'}
              }

check_interval = 600 # seconds, also used at system startup
start_interval =  30 # seconds

logging.basicConfig(filename = 'webservices_watchdog3.log', 
                    format   = '%(asctime)s %(message)s', 
                    datefmt  = '%Y-%m-%d %H:%M:%S', 
                    level    = logging.DEBUG)

def is_available(ws):
    addr = webservices[ws]['address']
    #logging.info('Testing %s', addr)
    try:
        response = urllib.request.urlopen(addr).getcode()
    except URLError:
        #logging.warning('Not reachable at all')
        logging.warning('Cannot reach %s', ws)
        return False
    #logging.info('Got HTTP response code %s', response)
    if response == 200:
        return True
    else:
        return False

def start_process(ws):
    script = webservices[ws]['executable']
    logging.info('Starting %s', script)
    process = subprocess.Popen(script, shell = True)
    logging.info('Now running with PID %d', process.pid)

def check_webservice(ws, i):
    if i > 5:
        logging.warning('Failed to start webservice 5 times without success, skipping for now')
        return False
    if not is_available(ws):
        start_process(ws)
        time.sleep(start_interval)
        return check_webservice(ws, i + 1)
    else:
        return True

if __name__ == '__main__':
    logging.info('-' * 60)
    logging.info('Starting webservice_watchdog.py')

    # w PC start completely before starting webservices
    while uptime.uptime() < check_interval:
        time.sleep(30)

    # main loop
    while True:
        for ws in webservices:
            #logging.info('Webservice %s', ws)
            check_webservice(ws, 0)
        time.sleep(check_interval)

