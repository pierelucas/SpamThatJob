'''
# External Modules
import json

#Internal Modules
import config
import test
from utils import filehandler
from scraper import scraper
from database import jobData as jd

def buidDetailPageLink(input_json: list) -> list:
    linklist: list = []
    for v in input_json:
        ref_number: str = v["refnr"]
        detailpage: str = config.detailpage_url + ref_number
        linklist.append(detailpage)
    return linklist

def main():

    # Call the function to fetch and save the database
    sc = scraper.Scraper()
    job_offers = sc.scrapeJobsFromJoboerse(config.getFullDynamicUrl())

    # Write Job offers to file
    test.writeJobOffersToFile(job_offers)

    # Get the Ref Links from the Job Offers as new list
    jobDetailURLList = buidDetailPageLink(job_offers)

    # Write Job Detaipage
    test.writeJobDetailpageURLSToFile(jobDetailURLList)

    # Initialize the Datastrcuture
    jobs: jd.Job = jd.Job()



if __name__ == "__main__":
    main()
'''

# Author: PiereLucas

# --- External Imports ---
import json
from sqlalchemy.orm import Session

# --- Internal Imports ---
import config
import test
from utils import filehandler
from scraper import jobboerse
from database import jobData as jd

# --- Database Initialization
jd.create_db_table()

# --- Helper function to get a database session ---
def getDbSession():
    db = jd.SessionLocal
    try:
        yield db
    finally:
        db.close()

# --- Adding Job to the Database ---
# TODO: Build the job object in an other function, fetch the missing job details and give Job Object to the function
def addJobTtoDB(job: dict):
    with next(getDbSession()) as db:
        # Build a Dict from the fetched Job Details
        '''
        newJob = {
            "Name": job.get("beruf"),
            "Description": job.get("titel"),
            "Type": None,
            "Ref": job.get("refnr"),
            "Url": config.detailPageBaseUrl + job.get("refnr"),
            "Contact": {
                'email': None,
                'phone': None,
                'company': job.get("arbeitgeber"),
                'contactPerson': None,
                'adress': {
                    'street': None,
                    'city': job.get("argbeitsort").get("ort"),
                    'state': job.get("argbeitsort").get("region"),
                    'zip': job.get("argbeitsort").get("plz"),
                    'country': job.get("argbeitsort").get("land")
                }
            },
            "Status": {
                'active': True,
                'completed': False,
                'when': None
            }
        }

        jobInstance = jd.Job(**newJob)
        '''

        jobInstance = jd.Job(**job)

        try:
            db.add(jobInstance)
            db.commit()
            db.refresh(jobInstance)
        except Exception as e:
            db.rollback()
            print(f"Error Adding job: {e}")

def findJobByReference(refID: str):
    with next(getDbSession()) as db:
        job = db.query(jd.Job).filter(jd.Job.Ref == refID).first()
        if job:
            # TODO: Do soemthing here
            return
        else:
            # TODO: Do something here too
            return

def main():
    # Call the function to fetch and save the database
    jobs = jobboerse.Scraper.scrape(url=config.getFullDynamicURL())
    for job in jobs:
        addJobTtoDB(job)

if __name__ == "__main__":
    main()