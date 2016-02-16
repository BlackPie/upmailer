import utils


imap_connection = utils.get_imap_connection()
smtp_connection = utils.get_smtp_connection()
messages = utils.fetch_new_emails(imap_connection)

if messages:
    needed_messages = utils.filter_messages(messages)

    print needed_messages

    for message in needed_messages:
        utils.send_email(smtp_connection, message)
