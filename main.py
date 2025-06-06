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
