import multiprocessing

# with nginx, gunicorn
workers = multiprocessing.cpu_count()*2 + 1
bind = 'unix:/tmp/jungmin.sock'
wsgi_app = 'nginx_study:create_app()'

# only gunicorn
# bind = '0.0.0.0:5000'
# workers = 2


errorlog = './gunicorn_log/errorlog.txt'
accesslog = './gunicorn_log/accesslog.txt'