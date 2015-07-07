# checkserver (freebsd)
Script checking server. Scan port range on server . If the server port is closed, write a message in log.txt and send e-mail for admin.

Script star checkserver.sh:
python /home/kuvy/data/checkserver.py

Example of adding in cron.
I added task to local cron for run every 30 minutes:
> crontab -e
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
*/30    *       *       *       *       /home/kuvy/data/checkserver.sh
