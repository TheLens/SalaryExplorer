
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from first import first
from sqlalchemy import Index
import ConfigParser
import sys

sys.path.append("../")

#config = ConfigParser.RawConfigParser()
config_location = "/apps/salaryexplorer/app.cfg"
#config.read(config_location)

Base = declarative_base()

def getFromFile(field):
    config = ConfigParser.RawConfigParser()
    #print config_location
    config.read(config_location)
    return config.get('Section1', field)

databasepassword = getFromFile('databasepassword')
server = getFromFile('server')
database = getFromFile('database')

def indexDB():
    engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)
    print 'engine'
    tables = Base.metadata.reflect(engine)
    print '1'
    peoplez = [i for i in Base.metadata.sorted_tables if i.name=='people'].pop()
    print '3'
    jobs = [i for i in Base.metadata.sorted_tables if i.name=='jobs'].pop()
    print '4'
    jobsnameindex = Index('jobs_name_index', jobs.c.name)
    for i in Base.metadata.sorted_tables:
        if i.name=="people":
            for t in i.c:
                print t
    #peoplenameindex_first = Index('people_name_index_first', people.c.first)
    #peoplenameindex_last = Index('people_name_index_last', people.c.last)
    #job_name = [i for i in Base.metadata.sorted_tables if i.name=='jobs'].pop()
    #for i in Base.metadata.sorted_tables:
    #    print i.name
    #i = Index('someindex', mytable.c.col5)
    #SQLi.create(engine)
    #Index('idx_col34', Person.)

indexDB()