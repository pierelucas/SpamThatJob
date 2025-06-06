# PiereLucas 05.06.2025

import json
from utils import filehandler
import config

def writeJobOffersToFile(jobOffers: list | None):
    fileContent = json.dumps(jobOffers, indent=2, ensure_ascii=False)
    if jobOffers is not None:
        print("Job offers found")
        filename = filehandler.write_str_to_file(fileContent, f"jobOffers{config.generateIsoUTCTimestamp()}.txt", "")
        if filename is not None:
            print(f"Successfully saved Job Offers to: {filename}")
        else:
            print("Failed to save Job Offers")

def writeJobDetailpageURLSToFile(jobDetailpageURLS: list | None):
    fileContent = json.dumps(jobDetailpageURLS, indent=2, ensure_ascii=False)
    if jobDetailpageURLS is not None:
        print("Got Job Detailpage URLS!")
        filename = filehandler.write_str_to_file(fileContent, f"jobDetailpageURLS{config.generateIsoUTCTimestamp()}.txt", "")
        if filename is not None:
            print(f"Succesfully saved Job Detailpage URLS to {filename}")
        else:
            print("Failed to save Detail Page URLS")
