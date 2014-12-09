import sys
import pprint
import json
import time 
import ConfigParser
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.sql import func
from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import request
from flask.ext.cache import Cache
sys.path.append('/home/abe-lens-laptop/lens/salaryexplorer/classes')
from classes import Person, Department, Agency, Job

Base = declarative_base()
app = Flask(__name__)

cache = Cache(app,config={'CACHE_TYPE': 'simple'})

config_location = "/home/abe-lens-laptop/lens/salaryexplorer/app.cfg"

def getFromFile(field):
    config = ConfigParser.RawConfigParser()
    config.read(config_location)
    return config.get('Section1', field)

databasepassword = getFromFile('databasepassword')
server = getFromFile('server')
database = getFromFile('database')


#width_bucket says how many would be in a histogram w/ equal sized buckets
@cache.memoize(timeout=900)
def get_average(agency):
    engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    out = session.query(func.avg(Person.annualsalary).label('average')).\
        filter(Agency.name == agency).first()
    print out

a ='CRT-OFF OF TOURISM'
get_average(a)

#width_bucket says how many would be in a histogram w/ equal sized buckets
@cache.memoize(timeout=900)
def get_buckets(min, max, agency, nbuckets):
    engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    n = "select * from people inner join agencies on people.agencyid=agencies.id where name='CRT-OFF OF TOURISM'"
    query = "select width_bucket(annualsalary, " + str(min) + ", " + str(max) + " ," + str(nbuckets) + "), count(*) from people inner join agencies on people.agencyid=agencies.id where name='" + agency + "' group by 1 order by 1;"
    connection = engine.connect()
    result = connection.execute(query)
    bucketsize = (max - min) / 10
    output = []
    n = 1
    bucketmin = min
    out = []
    for row in result:
        bucketmax = bucketmin + bucketsize
        r = [bucketmin, bucketmax, str(row[1])]
        out.append(r)
        bucketmin = bucketmax
    connection.close()
    return out

@cache.memoize(timeout=900)
def get_max(agencyname):
    engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    q = session.query(Person.annualsalary).\
        filter(Person.agencyid == Agency.id).filter(Agency.name == a).\
        filter(Agency.name == a).order_by(Person.annualsalary.desc())
    sal = q.first()[0]
    session.close()
    return sal

@cache.memoize(timeout=900)
def get_min(agencyname):
    engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    q = session.query(Person.annualsalary).\
        filter(Person.agencyid == Agency.id).filter(Agency.name == a).\
        filter(Agency.name == a).order_by(Person.annualsalary)
    sal = q.first()[0]
    session.close()
    return sal



print get_buckets(get_min(a),get_max(a), a, 10)

query("campbell")