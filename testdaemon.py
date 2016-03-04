#!/usr/bin/python

import daemon
import time
import logging

#LOGGING=CRITICAL,ERROR,WARNING,INFO,DEBUG
loggingLevel=logging.ERROR
logFilePath="/tmp/daemon.log"


def do_something():

    while True:
        with open("/tmp/current_time.txt", "w") as f:
            f.write("The time is now " + time.ctime())
        logging.debug ("SLeeping...")
        time.sleep(5)

def run():

    with daemon.DaemonContext():
        do_something()

if __name__ == "__main__":
    logging.debug ("Starting daemon")
    run()

