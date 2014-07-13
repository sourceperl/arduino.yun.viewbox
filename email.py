import imaplib
import json
import paho.mqtt.publish as publish

# Retrieve unseen mail number from IMAP server.

# cat /etc/crontabs/root 
#   format [min] [hour] [day of month] [month] [day of week] [program to be run]
#   */5 * * * * /usr/bin/python /root/bin/email.py

M = imaplib.IMAP4_SSL("imap.free.fr", 993)
M.login(<username>, <password>)
M.select()
(retcode, messages) = M.search(None, "(UNSEEN)")
if retcode == "OK":
  msg = {}
  msg['value'] = len(messages[0].split())
  msg['update'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
  publish.single("pub/mail/loic.celine/unread", json.dumps(msg),
                 hostname="192.168.1.60")
M.close()
