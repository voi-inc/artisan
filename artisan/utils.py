# stdlib
import os
import re
import time
import signal


def each_subdir(parent_dir):
    """
    Helper method for looping through subdirectories
    """
    for name in os.listdir(parent_dir):
        path = os.path.join(parent_dir, name)
        if os.path.isdir(path):
            yield (name, path)

def each_tmpl(parent_dir):
    """
    Helper method for looping through template files
    """
    for name in os.listdir(parent_dir):
        path = os.path.join(parent_dir, name)
        if re.search('\.(?:txt|html)', path, re.I) and not os.stat(path).st_size == 0:
            yield (name, path)

def keep_daemon_running(on_interrupt):
    """
    Keep active daemons running until keyboard interrupt
    """
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt or signal.SIGINT:
        on_interrupt()