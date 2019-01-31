#emailMsg.py
#12-19-16
#function to send emails, retun 0 = email sent, 1 = fault
"""Send emails, requires the following
    (recAddr, message)
"""
import smtplib

def sendEmail(recAddr, message):
    """Sends an email using gmail (recAddr, message)
    """
    sendAddr = 'enterEmaiAddress@gmail.com'
    emSecret = 'passWordInPlainText'
    gmailPort = 587
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', gmailPort)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(sendAddr, emSecret)
        smtpObj.sendmail(sendAddr, recAddr, message)
        smtpObj.quit()
    except:
        return 1
    return 0

###The following comments are to show you how to add email functionality to the lotto script
###at the start of lotto.py add in the path to the email.py or copy/paste the code into lotto.py
##
##sys.path.append('/home/pi/Python/lib')
##import emailMsg #contains email function
##
###set up the email message as a string with email addresses and subject
##recAddr = ['xxxxxx@hotmail.com', 'xxxxx@comcast.net']
##outMsg = 'To: ' + str(recAddr)
##outMsg += '\nSubject: Lotto Results\r\n\n '
##
################
##REST OF lotto.py script
################
##
###send email using my gmail
##print ('sending ', yesterdayDate, 'results')
##if (emailMsg.sendEmail(recAddr, outMsg)):
##    logging.error('Failed to send email')
##    sys.exit() 
