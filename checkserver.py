#!/usr/local/bin/env python

import socket
import sys, os
import threading, Queue
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime

#SEND MAIL

mail_user = "user@gmail.com"
mail_pwd = "password"

def Mail(to, subject, text):
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(mail_user, mail_pwd)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mail_user
    msg['To'] = to
    msg.attach(MIMEText(text, 'plain'))
    mailServer.sendmail(mail_user, to, msg.as_string())
    mailServer.close()

# SCANNER QUEUE BASED VERSION

MAX_THREADS = 50

class Scanner(threading.Thread):
    def __init__(self, inq, outq):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        # queues for (host, port)
        self.inq = inq
        self.outq = outq
    def run(self):
        while 1:
            host, port = self.inq.get()
            sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # connect to the given host:port
                sd.connect((host, port))
            except socket.error:
                # set the CLOSED flag
                self.outq.put((host, port, 'CLOSED'))
            else:
                self.outq.put((host, port, 'OPEN'))
                sd.close()
		
# MAIN

def CheckServer(host, start, stop, nthreads=MAX_THREADS):
    f = open ('./log.txt', 'a')
    toscan = Queue.Queue()
    scanned = Queue.Queue()
    scanners = [Scanner(toscan, scanned) for i in range(nthreads)]
    for scanner in scanners:
        scanner.start()
    hostports = [(host, port) for port in xrange(start, stop+1)]
    for hostport in hostports:
        toscan.put(hostport)
    results = {}
    for host, port in hostports:
        while (host, port) not in results:
            nhost, nport, nstatus = scanned.get()
            results[(nhost, nport)] = nstatus
        status = results[(host, port)]
        if status == 'CLOSED':
            message = str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") + ' SERVER %s:%d %s \n' % (host, port, status))
            f.write(message)
            Mail("admin@servera.ru", "Server is unavailable", message)
    f. close()

if __name__ == '__main__':
     CheckServer('87.87.87.1', 3000, 3100)
     CheckServer('92.92.92.2',5000,5000)
