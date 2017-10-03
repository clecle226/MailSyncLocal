# MailSyncLocal
Local Mail Box Synchronizer
# On Ubuntu
```
sudo apt-get update | sudo apt-get upgrade | sudo apt-get install python3
git clone https://github.com/clecle226/MailSyncLocal.git
chmod a+x MailSync.py
nano Config.cfg
```
Write in *Config.cfg* a block for each mailbox (you can write as many as you want)
```INI
[NameLocalSave]
Host=imap.example.com
Port=993 ;Optional
User=test@example.com
Pass=BestPassword ;Optional, ask each use if not indicated
AppendOnly=False ;Optional, default True, add only, it does not delete the messages not in the mailbox
Verify=True ;Optional, default False, check the integrity of all messages
```
And run program
```
python3 ./MailSync.py
```
