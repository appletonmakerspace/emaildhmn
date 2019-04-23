import imaplib
import base64
import os
import email


parser = argparse.ArgumentParser(description='Download email attachments')
parser.add_argument('--user', help='Gmail user.')
parser.add_argument('--password', help='Gmail app password.')
parser.add_argument('--folder', help='IMAP folder/label.')
args = parser.parse_args()

mailbox = imaplib.IMAP4_SSL('imap.gmail.com')
mailbox.login(args.user, args.password)
mailbox.select(args.folder)

type, data = mailbox.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()

for num in data[0].split():
    typ, data = mailbox.fetch(num, '(RFC822)' )
    raw_email = data[0][1]
    # converts byte literal to string removing b''
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    # downloading attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            #FIXME this just drops the attachment in the same dir as this python script
            filePath = os.path.join(os.getcwd(), fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject, uid=num.decode('utf-8')))
            # move to trash
            mailbox.store(num, '+X-GM-LABELS', '\\Trash')

# empty trash
mailbox.select('[Gmail]/Trash')
mailbox.store("1:*", '+FLAGS', '\\Deleted')
mailbox.expunge()
mailbox.close()
mailbox.logout()
