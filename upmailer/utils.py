import re
import email
import base64
import imaplib
import smtplib
import constants as c

from slugify import slugify
from settings import settings as s
from settings import settings as sss


def get_smtp_connection():
    smtp_connection = smtplib.SMTP('%s:%s' % (s.SMTP_HOST, s.SMTP_PORT))
    try:
        smtp_connection.ehlo()
        smtp_connection.starttls()
        smtp_connection.login(sss.PROXY_EMAIL, sss.PROXY_EMAIL_PASSWORD)
        return smtp_connection
    except Exception, e:
        print "Cant authenticate on the SMTP server. Check your settings please."
        exit()


def get_imap_connection():
    conn = imaplib.IMAP4_SSL(s.IMAP_HOST)
    try:
        conn.login(s.PROXY_EMAIL, s.PROXY_EMAIL_PASSWORD)
        return conn
    except Exception, e:
        print "Cant authenticate on the IMAP server. Check your settings please."
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

        if s.LANCEMONITOR_EMAIL in message['from']:
            message_list.append(message)

    return message_list


def extract_metadata(message):
    raw_message = message.as_string()
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

    if s.NEEDED_WORKLOAD and c.WORKLOAD_TAG in job_metadata:
        if c.WORKLOAD[s.NEEDED_WORKLOAD] != job_metadata[c.WORKLOAD_TAG]:
            return False

    if s.NEEDED_BUDGET and c.BUDGET_TAG in job_metadata:
        if s.BUDGET_TAG > job_metadata[c.BUDGET_TAG]:
            return False

    if s.NEEDED_DURATION:  # TODO
        pass

    if s.NEEDED_JOB_TYPE:
        if c.JOB_TYPE[s.NEEDED_JOB_TYPE] != job_metadata[c.JOB_TYPE_TAG]:
            return False

    if s.NEEDED_JOB_POSTED_MIN:
        if s.NEEDED_JOB_POSTED_MIN > client_metadata[c.JOBS_POSTED_TAG]:
            return False

    if s.NEEDED_HIRES_MIN and s.NEEDED_HIRES_MIN > client_metadata[c.PAST_HIRES_TAG]:
        print 5
        return False

    if s.NEEDED_HIRE_RATIO:
        hire_ratio = (client_metadata[c.PAST_HIRES_TAG] / client_metadata[c.JOBS_POSTED_TAG]) * 100
        if s.NEEDED_HIRE_RATIO > hire_ratio:
            return False

    if s.NEEDED_RATING_MIN and s.NEEDED_RATING_MIN > client_metadata[c.RATING_TAG]:
        return False

    if s.NEEDED_REVIEWS_MIN and s.NEEDED_REVIEWS_MIN > client_metadata[c.REVIEWS_COUNT_TAG]:
        return False

    return True


def filter_messages(messages):
    needed_messages = list()

    for message in messages:
        if is_job_acceptable(message):
            needed_messages.append(message)

    return needed_messages


def prepare_message(message):
    email_from = s.PROXY_EMAIL
    email_to = s.DESTINATION_EMAIL
    extracted_text = message.as_string().split('A new job post has matched your criterias:')[1].split('------------------------------')[0]

    result_message = "\r\n".join([
        "From: %s" % email_from,
        "To: %s" % email_to,
        "Subject: New Job",
        "",
        "%s" % extracted_text
        ])

    return result_message


def send_email(smtp_connection, message):
    prepared_message = prepare_message(message)
    email_from = s.PROXY_EMAIL
    email_to = s.DESTINATION_EMAIL

    smtp_connection.sendmail(email_from, [email_to], prepared_message)