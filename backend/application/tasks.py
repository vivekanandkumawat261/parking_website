from celery import shared_task

# task 1 - Download CSV report for user
# User(client) tiggered async job 

# task 2 - Monthly report send via mail
# scheduled job via crontab

# task 3 - Card generation update send via G-chat webhook 
#  Backend(endpoint) triggered async job 

