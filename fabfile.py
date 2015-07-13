# -*- coding: utf-8 -*-

'''
Methods for commiting app to Github.
It should never deploy to the server or S3.
That should be left to Travis CI and the server calling git pull.
'''

from fabric.api import local


def repo():
    '''/'''

    local('git add .gitignore')
    local('git add .travis.yml')
    local('git add README.md')
    local('git add fabfile.py')
    local('git add requirements.txt')


def data():
    '''/data/export/'''

    local('git add data/export/data.csv')
    local('git add data/export/highest-paid.csv')

    local('git add data/export/departments.txt')
    local('git add data/export/offices.txt')
    local('git add data/export/positions.txt')


def css():
    '''/statesalaries/static/css'''

    local('git add statesalaries/static/css/state-salaries.css')
    local('git add statesalaries/static/css/lens.css')


def js():
    '''/statesalaries/static/js'''

    local('git add statesalaries/static/js/state-salaries.js')


def templates():
    '''/statesalaries/templates'''

    local('git add index.html')


def scripts():
    '''/scripts'''

    local('git add scripts/check.sh')
    local('git add scripts/clean.py')
    local('git add scripts/export.sh')
    local('git add scripts/import.sh')
    local('git add scripts/main.sh')
    local('git add scripts/prepare_data.py')
    local('git add scripts/process.sh')
    local('git add scripts/util.py')


def addthemall():
    '''Run through entire deployment.'''

    repo()
    data()
    css()
    js()
    scripts()


def push():
    local('git push origin develop')


def pull():
    local('git pull origin develop')
