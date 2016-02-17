#!/usr/bin/env python

import sys
import time
import utils

from daemon.base import Daemon


# it makes debugging simple
def daemon_function():
    imap_connection = utils.get_imap_connection()
    smtp_connection = utils.get_smtp_connection()
    messages, id_list = utils.fetch_new_emails(imap_connection)

    if messages:

        needed_messages = utils.filter_messages(messages)

        for message in needed_messages:
            utils.send_email(smtp_connection, message)

    utils.mark_messages_as_seen(imap_connection, id_list)

    imap_connection.close()
    imap_connection.logout()
    smtp_connection.quit()


def cycle_test():
    i = 0
    while True:
        time.sleep(10)
        print i
        i += 1
        daemon_function()


class MyDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(60)
            daemon_function()


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/upmailer.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'test' == sys.argv[1]:
            daemon_function()
        elif 'cycle_test' == sys.argv[1]:
            cycle_test()
        # elif 'restart' == sys.argv[1]:
        #     daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
