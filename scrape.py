import smtplib
import imaplib
import email
from email.utils import getaddresses

#move emails to new folder once done
#if cell phone user texts email "set marker ANYTHING" and then program stores ANYTHING
#if email contains "set marker (.?) from phone addresses then make that keyword a maker
#if a new email comes along with that marker, the phone that sent the text gets notified

def process_inbox(server):
    
    """ Accesses a mailbox for an email 
        Scrapes the message senders and body of the messages  
    """
    rv, data = server.search(None, "All")
    # rv tells us if the search was successful
    if rv != "OK":
        print "error"
        return

    
    for num in data[0].split():
      #data is the first email
      #split into list of all the words in that email 
        rv, data= server.fetch(num, '(RFC822)')
        if rv != "OK":
            print "error"
            return


        msg = email.message_from_string(data[0][1])
        # create message object from first email
        tos = msg.get_all('to', [])
        ccs = msg.get_all('cc', [])
        resent_tos = msg.get_all('resent-to', [])
        resent_ccs = msg.get_all('resent-cc', [])

        all_recipients = getaddresses(tos + ccs + resent_tos + resent_ccs)
        tuple = all_recipients[0]
        print "From: " + tuple[1]
        print "To: " + tuple[0]

        # get body of the message 
        if msg.is_multipart():
            body = []
            for payload in msg.get_payload():
                body.append(payload.get_payload())
            print 'Body: '+ (body[0])

        else:
            print msg.get_payload()

        print 'Subject %s: %s' % (num, msg['Subject'])





server= imaplib.IMAP4_SSL('imap.gmail.com')

server.login('hackathonhmc2015@gmail.com', '4boizlive')

code, mailboxen= server.list()

rv , data = server.select("inbox")



process_inbox(server)






server.close()
server.logout()


# Need to put texting and emailing in these functions
#def text (number, carrier, content):
#def email (outGoingEmail, outGoingPswd, recievingEmail, content):

content = 'did this make it to ur phone'
mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.ehlo()
mail.starttls()
mail.login('hackathonhmc2015@gmail.com','4boizlive')
mail.sendmail('kylesuversucks@gmail.com', 'alexmitchell1234@gmail.com', content)
mail.sendmail( 'hackathonhmc2015@gmail.com', '13604211517@tmomail.net', content )
mail.sendmail( 'hackathonhmc2015@gmail.com', '4256475206@mms.txt.net', content )

mail.close()