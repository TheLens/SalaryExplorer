import ConfigParser
import sys
import csv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append('../classes')
import classes


config_location = "/home/abe/lens/salary_explorer/app.cfg"

Base = declarative_base()


def getFromFile(field):
    config = ConfigParser.RawConfigParser()
    config.read(config_location)
    return config.get('Section1', field)


databasepassword = getFromFile('databasepassword')
server = getFromFile('server')
database = getFromFile('database')


Base = declarative_base()
# an Engine, which the Session will use for connection
engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)
# create a configured "Session" class
Session = sessionmaker(bind=engine)
# create a Session
session = Session()


def add(datatype,name):
	indb = session.query(datatype).filter(datatype.name==name).count()
	if indb==0:
		new = datatype(name)
		session.add(new)
		session.commit()


#This needs to be refactored
def get(datatype,name):
	return session.query(datatype).filter(datatype.name==name).first().id


def process(datatype,name):
	add(datatype, name)
	return get(datatype, name)


def process(datatype,name):
	add(datatype, name)
	return get(datatype, name)


def addPerson(person):
	indb = session.query(classes.Person).filter(classes.Person.first==person.first)\
		.filter(classes.Person.last==person.last)\
		.filter(classes.Person.middle==person.middle)\
		.filter(classes.Person.annualsalary==person.annualsalary)\
		.filter(classes.Person.sourceid==person.sourceid)\
		.filter(classes.Person.jobid==person.jobid)\
		.filter(classes.Person.agencyid==person.agencyid)\
		.filter(classes.Person.departmentid==person.departmentid)\
		.filter(classes.Person.classificationid==person.classificationid)\
		.filter(classes.Person.employmentcategoryid==person.employmentcategoryid)\
		.filter(classes.Person.pctfulltime==person.pctfulltime).count()
	if indb==0:
		session.add(person)
		session.commit()


def getFirstLastMiddle(name):
	print name
	first = name.split(",")[1]
	lastname = name.split(",")[0]
	if len(first.split(" "))==2:
		firstname = first.split(" ")[0]
		middlename = first.split(" ")[1]
	else:
		firstname = first
		middlename = ""
	return [firstname, middlename,lastname]


with open('../data/11-7-2014.csv', 'rU') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	next(csvreader)
	for row in csvreader:
		print row
		source = "State Civil Service"
		vals = ([t.strip() for t in row])
		totals =  ([t.strip() for t in row if len(t.strip())>0])[0:9]
		agency, dept, parish, ein,	name, employmentClassificationType, hours, title, annualrateofpay = totals
		names = getFirstLastMiddle(name)
		person = classes.Person(names[0], names[2])
		person.middle = names[1]
		person.sourceid = process(classes.Source, source)
		person.parishid = process(classes.Parish, parish)
		person.agencyid = process(classes.Agency, agency)
		person.hours = process(classes.EmploymentCategory, hours)
		person.classificationid = process(classes.Classification, employmentClassificationType) #FT, PT, WAE?
		person.employmentcategoryid = process(classes.EmploymentCategory, employmentClassificationType) #civil service?
		person.jobid = process(classes.Job, title)
		person.departmentid = process(classes.Department, dept)
		person.annualsalary = float(annualrateofpay.replace("$", "").replace(",", ""))

		if hours == "Full-Time":
			addPerson(person)