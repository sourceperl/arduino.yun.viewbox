# IMAP library
import imaplib

# Retrieve unseen mail number from IMAP server.
# Format a string to display the number on I2C LCD screen.

# cat /etc/crontabs/root 
#   format [min] [hour] [day of month] [month] [day of week] [program to be run]
#   */5 * * * * /usr/bin/python /root/bin/email.py

# Access to YUN datastore lib (bridge interface ARM <->ATmega)
import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient

value = bridgeclient()

M = imaplib.IMAP4_SSL('imap.free.fr', 993)
M.login(<username>, <password>)
M.select()
(retcode, messages) = M.search(None, '(UNSEEN)')
if retcode == 'OK':
  nb_mail = len(messages[0].split())
  line3 = "%7d %s" % (nb_mail, 'e-mails' if (nb_mail > 1) else 'e-mail')
  value.put("line_3", line3.ljust(20))
M.close()
