#!/usr/bin/env python

import sys
import time
import utils

from daemon.base import Daemon


# it makes debugging simple
def daemon_function(imap_connection, smtp_connection):
    messages, id_list = utils.fetch_new_emails(imap_connection)

    if messages:

        needed_messages = utils.filter_messages(messages)

        for message in needed_messages:
            utils.send_email(smtp_connection, message)

        utils.mark_messages_as_seen(imap_connection, id_list)


class MyDaemon(Daemon):
    def __init__(self, pidfile, imap_connection, smtp_connection):
        super(MyDaemon, self).__init__(pidfile)
        self.imap_connection = imap_connection
        self.smtp_connection = smtp_connection

    def run(self):
        while True:
            time.sleep(60)
            daemon_function(self.imap_connection, self.smtp_connection)


if __name__ == "__main__":
    imap_connection = utils.get_imap_connection()
    smtp_connection = utils.get_smtp_connection()
    daemon = MyDaemon('/tmp/upmailer.pid', imap_connection, smtp_connection)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.imap_connection.quit()
            daemon.smtp_connection.quit()
            daemon.stop()
        elif 'test' == sys.argv[1]:
            daemon_function(imap_connection, smtp_connection)
        # elif 'restart' == sys.argv[1]:
        #     daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
