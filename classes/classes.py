from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import ConfigParser
import sys

sys.path.append("../")

#config = ConfigParser.RawConfigParser()
config_location = "/home/abe/lens/salary_explorer/app.cfg"
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

#CREATE UNIQUE INDEX uniquename ON basics (first, last);

#Data from the city is quite messy so we are 
#just going to use first, last, title, department, annual salary


class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class Parish(Base):
    __tablename__ = 'parishes'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class Agency(Base):
    __tablename__ = 'agencies'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class EmploymentCategory(Base):
    __tablename__ = 'employmentcategories'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class Classification(Base):
    __tablename__ = 'classifications'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    first = Column(String)
    middle = Column(String)
    last = Column(String)
    annualsalary = Column(Float)
    sourceid = Column(Integer, ForeignKey("sources.id"), nullable=False)
    parishid = Column(Integer, ForeignKey("parishes.id"), nullable=False)
    jobid = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    agencyid = Column(Integer, ForeignKey("agencies.id"), nullable=False)
    departmentid = Column(Integer, ForeignKey("departments.id"), nullable=False)
    classificationid = Column(Integer, ForeignKey("classifications.id"), nullable=False)
    employmentcategoryid = Column(Integer, ForeignKey("employmentcategories.id"), nullable=False)
    pctfulltime = Column(Float)

    def __init__(self, first, last, middle = None,annualsalary = None\
            ,source = None, parish = None, job = None, \
            agency = None, department = None, \
            classification = None, employmentcategory = None, pctfulltime = None):
        self.first = first
        self.middle = middle
        self.last = last
        self.annualsalary = annualsalary
        self.sourceid = source
        self.parishid = parish
        self.jobid = job
        self.agencyid = agency
        self.departmentid = department
        self.classificationid = classification #civil service or no?
        self.employmentcategoryid = employmentcategory #FT, PT, WAE
        self.pctfulltime = pctfulltime

def remakeDB():
    engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)
    Base.metadata.create_all(engine)

remakeDB()