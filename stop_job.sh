echo "kill"
ps -ef|grep job.py|grep -v grep|cut -c 9-15
echo "---------------------------------"
ps -ef|grep job.py|grep -v grep|cut -c 9-15|xargs kill -9
ps -ef|grep 'job.py'
