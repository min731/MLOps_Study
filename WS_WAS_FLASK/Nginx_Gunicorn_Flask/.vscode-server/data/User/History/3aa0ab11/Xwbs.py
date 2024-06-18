import multiprocessing

workers = multiprocessing.cpu_count()*2 + 1

bind = '0.0.0.0:5000'
# workers = 2
errorlog = './gunicorn_log/errorlog.txt'
accesslog = './gunicorn_log/accesslog.txt'