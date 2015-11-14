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

    rtn = {}
    for num in data[0].split():
      #data is the first email
      #split into list of all the words in that email 
        rv, data= server.fetch(num, '(RFC822)')
        if rv != "OK":
            print "error"
            return
        #print data[0][0][0]
        msg = email.message_from_string(data[0][1])
        # create message object from first email
        tos = msg.get_all('to', [])
        #ccs = msg.get_all('cc', [])
        resent_tos = msg.get_all('resent-to', [])
        #resent_ccs = msg.get_all('resent-cc', [])

        all_recipients = getaddresses(tos + resent_tos)
        tuple = all_recipients[0]
        incomingAddress = tuple[1]

        #print "From: " + tuple[1]
        #print "To: " + tuple[0]

        # get body of the message 
        if msg.is_multipart():
            body = []
            for payload in msg.get_payload():
                body.append(payload.get_payload())
            #print 'Body: '+ (body[0])
            text = body[0]

        else:
            text = "no text"
            #print msg.get_payload()

        #print 'Subject %s: %s' % (num, msg['Subject'])
        subject = msg['Subject']
        #print num
        #print (subject, incomingAddress, text)
        rtn[num] = (subject, incomingAddress, text)
    return rtn



def findFromPhone(dictionary):
    setList = []
    deleteList = []
    print dictionary.keys()
    for key in range(1,len(dictionary.keys())):
        key = str(key)
        #this is the incomingAddress
        print dictionary[key][1]
        bodyStr = dictionary[key][2]
        bodyWords = bodyStr.split()
        print bodyWords[0]
        if (dictionary[key][1] == '4256475206@txt.att.net'):
            if (bodyWords[0] == "Set"):
                setList.append(bodyWords[1])
            elif (bodyWords[0] == "Delete"):
                deleteList.append(bodyWords[1])
    #print setList
    #print deleteList
    return (setList, deleteList)
    




# Need to put texting and emailing in these functions
def text (number, content):
    content = 'did this make it to ur phone'
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('hackathonhmc2015@gmail.com','4boizlive')
    
    mail.sendmail( 'hackathonhmc2015@gmail.com', '13604211517@tmomail.net', content )
    mail.sendmail( 'hackathonhmc2015@gmail.com', number, content )

    mail.close()


def email2 (outGoingEmail, outGoingPswd, recievingEmail, content):
    content = 'did this make it to ur phone'
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()

    mail.login(outGoingEmail, outGoingPswd)
    mail.sendmail(outGoingEmail, recievingEmail, content)

    mail.close()

def main():
    server= imaplib.IMAP4_SSL('imap.gmail.com')

    server.login('hackathonhmc2015@gmail.com', '4boizlive')

    code, mailboxen= server.list()

    rv , data = server.select("inbox")

    dictOfMail = process_inbox(server)

    listOfSets = findFromPhone(dictOfMail)

    setList = listOfSets[0]

    deleteList = listOfSets[1]

    print setList

    print deleteList
    
    text('4256475206@txt.att.net', "We recieved your text.  We set the marker to be")
    print "text"
    server.close()
    server.logout()
if __name__ == "__main__" : main()



