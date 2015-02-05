import sys
import pprint
import json
import time 
import ConfigParser
from sqlalchemy import Column, Integer, String, Float, ForeignKey, distinct
from flask import Flask
from flask import render_template
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import request
from flask.ext.cache import Cache
from sqlalchemy.sql import func
sys.path.append('classes')
from classes import Person, Department, Agency, Job
import locale
locale.setlocale( locale.LC_ALL, '')


app = Flask(__name__)

config_location = "/apps/salaryexplorer/app.cfg"

Base = declarative_base()

def getFromFile(field):
    config = ConfigParser.RawConfigParser()
    config.read(config_location)
    return config.get('Section1', field)

databasepassword = getFromFile('databasepassword')
server = getFromFile('server')
database = getFromFile('database')

cache = Cache(app,config={'CACHE_TYPE': 'simple'})

engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)

PAGE_SIZE = 25

class Row():
    id = Column(Integer, primary_key=True)
    first = ""
    last = ""
    title = ""
    agency = ""
    department = ""
    annualsalary = 0

    def __init__(self, first, last, annualsalary, title=None, agency=None, department=None):
        self.first = first
        self.last = last
        self.annualsalary = annualsalary
        self.title = title
        self.agency = agency
        self.department = department


@cache.memoize(timeout=900)
def get_average(agency):
    engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    avg = session.query(func.avg(Person.annualsalary).label('average')).\
        filter(Agency.name == agency).first()[0]
    return locale.currency(int(avg), grouping=True ).replace(".00", "")


#width_bucket says how many would be in a histogram w/ equal sized buckets
@cache.memoize(timeout=900)
def get_buckets(min, max, agency, nbuckets):
    engine = create_engine('postgresql://abe:' + databasepassword + '@' + server + ':5432/' + database)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
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
def get_max(a):
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
def get_min(a):
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

@cache.memoize(timeout=900)
def query(q):
    return q.all()


@cache.memoize(timeout=900)
def count(q):
    return q.count()


@app.route('/')
def search():
    return render_template('intro_child.html', title="Search government salaries", url="salaries")


#search/?q=Attorney+General
@app.route('/agency/<string:a>', methods=['POST', 'GET'])
def agency(a):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    q = session.query(Person.first, Person.last, Agency.name).\
            filter(Person.agencyid == Agency.id).filter(Agency.name == a)
    workercount = count(q)

    q = session.query(Person.first, Person.last, Person.annualsalary).\
            filter(Person.jobid == Job.id).filter(Person.agencyid == Agency.id).filter(Agency.name == a).order_by(Person.annualsalary.desc()).limit(10)
    highestpaid = q.all()
    print highestpaid
    highest = []
    for h in highestpaid:
        highest.append(Row(h[0], h[1], locale.currency(int(h[2]), grouping=True ).replace(".00", "")))
    highestpaid = highest
    print highestpaid
    minsal = get_min(a)
    maxsal = get_max(a)
    bucks = get_buckets(minsal, maxsal, a, 10)
    avg = get_average(a)
    histogramlabels = []
    for t in bucks:
        histogramlabels.append("$" + str(int(t[0])) + "-" + "$" + str(int(t[1])))
    histogramcounts = [b[2] for b in bucks]
    session.close()
    return render_template('agency.html', name=a, histogramcounts=histogramcounts, average=avg, histogramlabels=histogramlabels, highestpaid=highestpaid, totalworkers=workercount, title="Search government salaries", url="salaries")


def parse(q):
    output = {}
    parts = q.split("&")
    print parts
    name = [p.replace("name=","") for p in parts if "name=" in p]
    if len(name)==1:
        name=name.pop()
    department = [p.replace("department=","") for p in parts if "department=" in p]
    if len(department)==1:
        if not str(department[0])=="undefined" and not str(department[0]) == "Department":
            department=department.pop()
        else:
            department = []
    title = [p.replace("title=","") for p in parts if "title=" in p]
    page = [p.replace("page=","") for p in parts if "page=" in p]
    agency = [p.replace("agency=","") for p in parts if "agency=" in p]
    if len(agency)==1:
        if not str(agency[0])=="undefined" and not str(agency[0]) == "Agency":
            agency = agency.pop()
        else:
            agency = []
    if len(title)==1:
        if not str(title[0])=="undefined" and not str(title[0]) == "Title":
            title = title.pop()
        else:
            title = []
    if len(page)==1:
        if not str(page[0])=="undefined" and not str(page[0]) == "Page":
            page = page.pop()
        else:
            page = 1
    else:
        page = 1 #default vaule
    q = [p.replace("q=","") for p in parts if "q=" in p]
    if len(q)==1:
        q = q.pop()
    output['base'] = q
    output['department'] = department
    output['title'] = title
    output['agency'] = agency
    output['page'] = page
    print "parse"
    print output
    return output


def build(query_terms):
    print query_terms
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    q = session.query(Person.first, Person.last, Person.annualsalary, Job.name, Agency.name, Department.name) 
    if len(query_terms['base'])>0:
        q = session.query(Person.first, Person.last, Person.annualsalary, Job.name, Agency.name, Department.name).\
            filter(Person.first.ilike('%' + query_terms['base'] + '%') | Person.last.ilike('%' + query_terms['base'] + '%'))
        print "adding base"
    if len(query_terms['department'])>0:
        q = q.filter(Department.name==query_terms['department'])
        print "adding department"
    if len(query_terms['title'])>0:
        q = q.filter(Job.name==query_terms['title'])
        print "adding title"
    if len(query_terms['agency'])>0:
        q = q.filter(Agency.name==query_terms['agency'])
        print "adding agency"
    q = q.filter(Person.jobid == Job.id).filter(Person.agencyid == Agency.id).filter(Person.departmentid == Department.id) 
    print "built {}".format(q)
    return q


def get_agencies(query_terms):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    if len(query_terms['base'])>0:
        q = session.query(Person.first, Person.last, Person.annualsalary, Job.name, Agency.name, Department.name).\
            filter(Person.first.ilike('%' + query_terms['base'] + '%') | Person.last.ilike('%' + query_terms['base'] + '%'))
    else: #handles blank queries from the UI
        q = session.query(Person.first, Person.last, Person.annualsalary, Job.name, Agency.name, Department.name)
    if len(query_terms['department'])>0:
        q = q.filter(Department.name==query_terms['department'])
    if len(query_terms['title'])>0:
        q = q.filter(Job.name==query_terms['title'])
    if len(query_terms['agency'])>0:
        q = q.filter(Agency.name==query_terms['agency'])
    q = q.filter(Person.jobid == Job.id).filter(Person.agencyid == Agency.id).filter(Person.departmentid == Department.id) 
    results = [i[4] for i in q.all()]
    results = list(set(results))
    results.sort()
    return results


def get_departments(query_terms):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    if len(query_terms['base'])>0:
        q = session.query(Person.first, Person.last, Person.annualsalary, Job.name, Agency.name, Department.name).\
            filter(Person.first.ilike('%' + query_terms['base'] + '%') | Person.last.ilike('%' + query_terms['base'] + '%'))
    else:  #handles blank queries from the UI
        q = session.query(Person.first, Person.last, Person.annualsalary, Job.name, Agency.name, Department.name)
    if len(query_terms['department'])>0:
        q = q.filter(Department.name==query_terms['department'])
    if len(query_terms['title'])>0:
        q = q.filter(Job.name==query_terms['title'])
    if len(query_terms['agency'])>0:
        q = q.filter(Agency.name==query_terms['agency'])
    q = q.filter(Person.jobid == Job.id).filter(Person.agencyid == Agency.id).filter(Person.departmentid == Department.id) 
    results = [i[5] for i in q.all()]
    results = list(set(results))
    results.sort()
    return results

#search/?q=Attorney+General
@app.route('/search/<path:q>', methods=['POST'])
def results(q):
    query_terms = parse(q)
    q = build(query_terms)
    results_total = q.count()
    q = q.limit(PAGE_SIZE)
    if (int(query_terms['page']) > 1):
        q= q.offset(int(query_terms['page']) * PAGE_SIZE)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    results = query(q)
    print results
    session.close()
    rows = []
    for r in results:
        rows.append(Row(r[0], r[1], locale.currency(int(r[2]), grouping=True ).replace(".00", ""), r[3], r[4], r[5]))
    jobs = list(set([r[3] for r in results]))
    jobs.insert(0,"Title")
    agencies = get_agencies(query_terms)
    agencies.insert(0,"Agency")
    departments = get_departments(query_terms)
    departments.insert(0, "Department")
    return render_template('results.html', results=rows, jobs=jobs, agencies=agencies, departments=departments, page_length=PAGE_SIZE, results_total=results_total)


@app.route('/search/<path:q>', methods=['GET'])
def results_from_URL(q):
    query_terms = parse(q)
    q = build(query_terms)
    results_total = q.count()
    q = q.limit(PAGE_SIZE)
    if (int(query_terms['page']) > 1):
        q= q.offset(int(query_terms['page']) * PAGE_SIZE)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    print "query terms"
    print q
    results = query(q)
    print results
    session.close()
    rows = []
    for r in results:
        rows.append(Row(r[0], r[1], locale.currency(int(r[2]), grouping=True ).replace(".00", ""), r[3], r[4], r[5]))
    jobs = list(set([r[3] for r in results]))
    jobs.insert(0,"Title")
    agencies = get_agencies(query_terms)
    agencies.insert(0,"Agency")
    departments = get_departments(query_terms)
    departments.insert(0, "Department")
    html = render_template('results.html', results=rows, jobs=jobs, agencies=agencies, departments=departments, page_length=PAGE_SIZE, results_total=results_total)
    return render_template('intro_child.html', title="Search government salaries", url="salaries", contents=html)

if __name__ == '__main__':
    app.run(debug=True)