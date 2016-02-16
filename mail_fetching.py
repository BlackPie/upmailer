import utils


imap_connection = utils.get_imap_connection()
smtp_connection = utils.get_smtp_connection()
messages = utils.fetch_new_emails(imap_connection)

if messages:
    needed_messages = utils.filter_messages(messages)

    for message in needed_messages:
        utils.send_email(smtp_connection, message)

imap_connection.close()
smtp_connection.close()
