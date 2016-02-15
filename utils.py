import email
import imaplib
import settings.settings as settings

from slugify import slugify


def get_smtp_connection():
    pass


def get_imap_connection():
    conn = imaplib.IMAP4_SSL(settings.IMAP_HOST)

    try:
        conn.login(settings.EMAIL, settings.PASSWORD)
        return conn
    except Exception, e:
        print "Cant authenticate on the server. Check your settings please."
        exit()


def fetch_new_emails(imap_connection):
    imap_connection.select("inbox")
    result, data = imap_connection.search(None, "ALL")  # TODO make it smart
    id_list = data[0].split()#[:settings.MAX_NUMBER_OLD_MESSAGES]
    message_list = list()

    for message_id in id_list:
        result, data = imap_connection.fetch(message_id, "(RFC822)")
        raw_email = data[0][1]
        message = email.message_from_string(raw_email)

        if settings.LANCEMONITOR_EMAIL in message['from']:
            message_list.append(message)

    return message_list


def extract_metadata(message):
    raw_message = message.get_payload()[0].get_payload()
    text1 = raw_message.split('Job metadata')
    text2 = text1[1].split('Client metadata')
    raw_job_metadata = text2[0]
    raw_client_metadata = text2[1].split('--------------')[0]
    job_metadata = dict()
    client_metadata = dict()
    job_variables = raw_job_metadata.split('\r\n')[:-1]
    client_variables = raw_client_metadata.split('\r\n')[:-2]

    for var in job_variables:
        key, value = var.split(': ')
        job_metadata.update({slugify(key).replace('-', '_'): value})

    for var in client_variables:
        key, value = var.split(': ')
        client_metadata.update({slugify(key).replace('-', '_'): value})

    return job_metadata, client_metadata


def is_job_acceptable(message):
    job_metadata, client_metadata = extract_metadata(message)


def filter_messages(messages):
    needed_messages = list()

    for message in messages:
        if is_job_acceptable(message):
            needed_messages.append(message)

    return needed_messages


def send_email(smtp_connection, message):
    pass
