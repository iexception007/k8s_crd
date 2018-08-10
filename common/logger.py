#!/usr/bin/python

import logging
import os
import os.path
import time


logger = logging.getLogger()
logger.setLevel(logging.INFO)


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

#rq       = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
#log_path = os.path.dirname(os.getcwd()) + '/logs/'
rq       = time.strftime('%Y%m%d', time.localtime(time.time()))
log_path = os.getcwd() + '/logs/'
log_name = log_path + rq + '.log'
logfile  = log_name
fh = logging.FileHandler(logfile, mode='a')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)



def test():
    logger.debug('this is a logger debug message')
    logger.info('this is a logger info message')
    logger.warning('this is a logger warning message')
    logger.error('this is a logger error message')
    logger.critical('this is a logger critical message')



if __name__ == "__main__":
    test()