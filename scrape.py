import smtplib
import imaplib
import email
import re
from bs4 import BeautifulSoup
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
        froms = msg.get_all('from', [])
        all_recipients = getaddresses(froms)
        tuple = all_recipients[0]
        incomingAddress = tuple[1]
        #print incomingAddress

        #print "From: " + tuple[1]
        #print "To: " + tuple[0]

        # get body of the message 
        if msg.is_multipart():
            body = []
            for payload in msg.get_payload():
                body.append(payload.get_payload())
            #print 'Body: '+ (body[0])
            text = body[0]
            if (type(text) is list):
                text = text[0].as_string()
                for item in text.split("</td>\r\n"):
                    if "<td>\r\n" in item:
                        print item[item.find("<td>\r\n")+len("</td>\r\n"):]
                        text = item[item.find("<td>\r\n")+len("</td>\r\n"):]
        else:
            text = "No text"
            #print msg.get_payload()

        #print 'Subject %s: %s' % (num, msg['Subject'])
        subject = msg['Subject']
        #print num
        print (subject, incomingAddress, text)
        rtn[num] = (subject, incomingAddress, text)
    return rtn



def findFromPhone(dictionary):
    setList = []
    deleteList = []
    #print dictionary.keys()
    for key in range(1,len(dictionary.keys())+1):
        key = str(key)
        #print key
        #print dictionary[key][0]
        #this is the incomingAddress
        bodyStr = dictionary[key][2]
        #print bodyStr
        bodyWords = bodyStr.split()
        #print bodyWords[0]
        print "From:" + dictionary[key][1]
        if (dictionary[key][1] == '4256475206@mms.att.net'):
            print "this is from kyle"
            if (bodyWords[0] == "Set"):
                print "found a set command"
                setList.append(bodyWords[1])
            elif (bodyWords[0] == "Delete"):
                deleteList.append(bodyWords[1])
    #print setList
    #print deleteList
    return (setList, deleteList)

def deleteFromSetList(setList, deleteList):
    for word in deleteList:
        if word in setList:
            setList.remove(word)


def sendAlertUsingSetList(setlist,dictionary, number):
    for word in setlist:
        for key in range(1,len(dictionary.keys())+1):
            key = str(key)
            #subjectLine = dictionary[key][0]
            bodyStr = dictionary[key][2]
            nameOfSender = dictionary[key][1]
            if word in bodyStr:
                strToSend = "Got "+ word+" from " + nameOfSender
                #print "Should be sending "+strToSend
                text(number, strToSend)
            #elif word in subjectLine:
                #strToSend = "Got "+ word+" from " + nameOfSender
                #text(number, strToSend)
            elif word in nameOfSender:
                strToSend = word+ " sent message"
                text(number, strToSend)


# Need to put texting and emailing in these functions
def text(number, content):
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('hackathonhmc2015@gmail.com','4boizlive')
    content2 = str(content)
    content3 = content2 + ""
    mail.sendmail( 'hackathonhmc2015@gmail.com', '13604211517@tmomail.net', content )
    
    mail.sendmail( 'hackathonhmc2015@gmail.com', number, content3)

    mail.close()


def email2 (outGoingEmail, outGoingPswd, recievingEmail, content):
    content = 'did this make it to ur phone'
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()

    mail.login(outGoingEmail, outGoingPswd)
    mail.sendmail(outGoingEmail, recievingEmail, str(content))

    mail.close()

def main():
    #get info from server 
    server= imaplib.IMAP4_SSL('imap.gmail.com')
    #log in to the email using username and password
    server.login('hackathonhmc2015@gmail.com', '4boizlive')

    code, mailboxen= server.list()

    rv , data = server.select("inbox")

    dictOfMail = process_inbox(server)

    listOfSets = findFromPhone(dictOfMail)

    setList = listOfSets[0]

    deleteList = listOfSets[1]

    sendAlertUsingSetList(setList, dictOfMail, "4256475206@txt.att.net")
    
    deleteFromSetList(setList, deleteList)
    
    print "text"
    server.close()
    server.logout()
if __name__ == "__main__" : main()



