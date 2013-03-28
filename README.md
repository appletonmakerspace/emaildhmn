emaildhmn.py
============

A python script to automate the sending of the weekly "This Week..." email 
to the dhmn-discussion mailing list.

This script assumes that you are sending the intended message from a GMAIL account, and you have the proper login credentials for that account.

To be run via cron on Mondays 8:30am central time.

#example
30 8 * * 1 /usr/local/bin/python /home/mike/crons/emaildhmn.py --user USER --pass PASSWORD RECIPIENT

RECIPIENT should be in the format of user@domain.com
