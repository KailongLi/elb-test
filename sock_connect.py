import sys
import httplib
import time
import logging
import os
import socket

HEAD = {}
BODY = ''
URL = '/'
VERSION_CHECK = False
REQUEST_TIMEOUT = 5

RETRY_TIMES = 10
REQUEST_INTERVAL = 1
RESPONSE_CODE = 200

OUTPUT_INTERVAL = 2


class Log_Recorder(object):
    def __init__(self, host, port):
        self.name = host + ':' + port
        self.file_name = self.name + '.log'
        self.path_file_name = os.path.join(os.path.dirname(__file__),
                                           self.file_name)
        self.format = '%(asctime)s: %(message)s'
        self.level = logging.DEBUG

    def set_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        file_handler = logging.FileHandler(self.path_file_name)
        file_handler.setLevel(self.level)
        formatter = logging.Formatter(self.format)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger


class Http_Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.strict = VERSION_CHECK
        self.req_timeout = REQUEST_TIMEOUT
        self.url = URL
        self.header = HEAD
        self.body = BODY
        self.success_times = 0
        self.fail_times = 0
        self.fail_response = []
        return

    def http_connect(self, reconnect_times, logger):
        self.connection = httplib.HTTPConnection(self.host, self.port,
                                                 self.strict, self.req_timeout)
        logger.info("Connect Setted: connect time - %s" % reconnect_times)
        return

    def http_get(self):
        self.connection.request(method='GET', url=self.url, body=self.body,
                                headers=self.header)
        self.response = self.connection.getresponse()
        self.status = self.response.status
        self.reason = self.response.reason
        self.response_content = self.response.read()

    def response_check(self, logger, counter):
        if self.status != RESPONSE_CODE:
            logger.error("Connect Failed: status - %s, reason - %s\n"
                         % (self.status, self.reason))
            self.fail_times += 1
        else:
            if (self.success_times % OUTPUT_INTERVAL) == 0:
                logger.info("Connect Report: success - %s, faild - %s, "
                            "connect - %s" %
                            (self.success_times, self.fail_times, counter))
            self.success_times += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERR: parameter %d != 2" % len(sys.argv))
    host = sys.argv[1]
    port = int(sys.argv[2])
    reconnect_times = 0
    conn_inst_list = []
    log_rec = Log_Recorder(host, str(port))
    logger = log_rec.set_logger()
    print "=====START====="
    for i in range(0, RETRY_TIMES):
        try:
            conn_inst = Http_Client(host, port)
            conn_inst_list.append(conn_inst)
            conn_inst_list[i].http_connect(reconnect_times, logger)
            while True:
                conn_inst_list[i].http_get()
                conn_inst_list[i].response_check(logger, i)
                time.sleep(REQUEST_INTERVAL)
        except httplib.BadStatusLine:
            logger.error("Connect Error: Bad Status Line")
            reconnect_times += 1
            continue
        except socket.error as e:
            logger.error("Connect Error: Socket Error - %s" % e)
            reconnect_times += 1
            continue
        except KeyboardInterrupt, e:
            break
    logger.info("\nTerminated\n")
    print("Interrupt Times: %s" % reconnect_times)
    print "=====FINISHED====="


