#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getpass, imaplib, os, re, argparse, sys, configparser, getpass
import urllib.parse
from email.parser import BytesParser, Parser
from email.policy import default

def SyncMailBox(NameMailBoxe,Host,Port,User,Pass,AppendOnly=True,VerifyAllMail=False):
        if Host == None or User == None:
                print("Error Config File:"+NameMailBoxe)
                sys.exit(1)
        if Pass == None:
                Pass = getpass.getpass()
        M = imaplib.IMAP4_SSL(Host,Port)
        M.login(User,Pass)
        typ, listeBox = M.list()
        for Box in listeBox:
                NameBox = re.findall('\"(.*?)\"', Box.decode("utf-8"))[1]
                NameDir = os.path.normpath("./"+NameMailBoxe+"/"+NameBox.replace(".","/")+"/")
                if not os.path.exists(NameDir):
                        os.makedirs(NameDir)
                M.select(NameBox,readonly=True)
                typ, data = M.search(None, 'ALL')
                ListeUIDMailBoxes = []
                for num in data[0].split():
                        NameFileUID = urllib.parse.quote_plus(re.findall('\<(.*?)\>', (((M.fetch(num, '(BODY[HEADER.FIELDS (MESSAGE-ID)])'))[1][0][1]).decode("utf-8"))  )[0])
                        if not AppendOnly:
                                ListeUIDMailBoxes.append(NameFileUID+".eml")
                        NameFile = os.path.normpath(NameDir+"/"+NameFileUID+".eml")
                        if not os.path.exists(NameFile):
                                typ, data = M.fetch(num, '(RFC822)')
                                f = open(NameFile, 'w')
                                msg = BytesParser(policy=default).parsebytes(data[0][1])
                                f.write(str(msg))
                                f.close()
                        elif VerifyAllMail and os.path.exists(NameFile):
                                typ, data = M.fetch(num, '(RFC822)')
                                msg = BytesParser(policy=default).parsebytes(data[0][1])
                                f = open(NameFile, 'r')
                                if f.read() != str(msg):
                                        print("Conflit contenu de :"+NameFileUID)
                                        f = open(NameFile, 'w')
                                        f.write(str(msg))
                                f.close()
                if not AppendOnly:
                        ListeUIDDirectory = os.listdir(NameDir)
                        for item in ListeUIDDirectory:
                                if os.path.isdir(os.path.normpath(NameDir+"/"+item)):
                                      ListeUIDDirectory.remove(item)  
                        for item in ListeUIDMailBoxes:
                                ListeUIDDirectory.remove(item)
                        for item in ListeUIDDirectory:
                                os.remove(os.path.normpath(NameDir+"/"+item))
        M.close()
        M.logout()          

parser = argparse.ArgumentParser(description='Mail synchroniser')
parser.add_argument('--Host', type=str, action="store",
                   help='Host MailBoxes')
parser.add_argument('--Port', type=int, default=993,
                   help='Port(Default 993)')
parser.add_argument('--Name', type=str, default="default",
                   help='Name local directory')
parser.add_argument('--Verify', type=bool, default=False,
                   help='Verify integration of mail')
parser.add_argument('--User', type=str,
                   help='User Mailboxes')
parser.add_argument('--Pass', type=str,
                   help='Pass Mailboxes')
parser.add_argument('--AppendOnly', type=bool, default=True,
                   help='Exactly synchronisation or add new mail')
parser.add_argument('--ConfigFile', type=str, default="Config.cfg",
                   help='Auto-configuration File')

args = parser.parse_args()
if args.Host == None and (args.ConfigFile == 'Config.cfg' and not os.path.exists("Config.cfg")):
        print(parser.parse_args(['-h']))
elif args.Host != None and args.User != None and args.Pass != None:
        SyncMailBox(args.Name,args.Host,args.Port,args.User,args.Pass, args.AppendOnly,args.Verify)
elif os.path.exists(args.ConfigFile):
        settings = configparser.ConfigParser()
        settings.optionxform = str
        settings.read(args.ConfigFile)
        for block in settings.sections():
                print(block)
                SyncMailBox(block,
                        settings.get(block,"Host",fallback=None),
                        settings.get(block,"Port",fallback=993),
                        settings.get(block,"User",fallback=None),
                        settings.get(block,"Pass",fallback=None),
                        settings.get(block,"AppendOnly",fallback=True),
                        settings.get(block,"Verify",fallback=False))
else:
        print("Parsing arguments error")
        print(parser.parse_args(['-h']))
