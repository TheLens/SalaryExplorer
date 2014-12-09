from fabric.api import run
from fabric.api import env
from fabric.context_managers import settings

env.hosts = ['localhost']

def restart_app():
    with settings(warn_only=True):
        run('fuser -k 5000/tcp')
    run('python /home/abe-lens-laptop/lens/salaryexplorer/app.py')

def compile_coffee():
    run('coffee --compile --output /home/abe-lens-laptop/lens/salaryexplorer/static/js/ /home/abe-lens-laptop/lens/salaryexplorer/static/coffee/')

def compile_less():
    run('lessc /home/abe-lens-laptop/lens/salaryexplorer/static/less/explorer.less > /home/abe-lens-laptop/lens/salaryexplorer/static/css/explorer.css')

def compile():
	compile_less()
	compile_coffee()