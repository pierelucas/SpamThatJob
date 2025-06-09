# PiereLucas 05.06.2025

# --- External Imports ---
import requests
import json

from camoufox.sync_api import Camoufox

# --- Interal Imports ---
import config

# --- Scraper Class ---
class Scraper():

    @staticmethod
    def scrape(url) -> list | None:
        """
        Fetches job offers from the given API URL with custom headers and cookies,
        then saves the 'stellenangebote' to a text file.
        The filename includes the current date and key parameters from the URL.
        """

        jobs = []

        try:
            # Make the GET request to the API with specified headers and cookies
            response = requests.get(url, headers=config.baseHeaders, cookies=config.baseCookies)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Parse the JSON response
            data = response.json()

            # Extract "stellenangebote"
            jobJSONList = data.get("stellenangebote", [])

            for job in jobJSONList:
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

                # TODO: Camoufox/Playwright logic to get the missing details

                jobs.append(newJob)

            return jobs

        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None
        except json.JSONDecodeError:
            print("Error: Could not decode JSON response. Please check the API response format.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    @staticmethod
    def testCamoufox():
        with Camoufox(headless=False, humanize=True) as browser:
            page = browser.new_page()
            page.goto("https://www.arbeitsagentur.de/jobsuche/jobdetail/10001-1000735585-S")
            page.get_by_role("button", name="Auswahl bestätigen").click() # Accept Cookies
            page.get_by_role("button", name="Anmelden").click()
            browser.close()



# --- Testing the Scraper Module ---
if __name__ == "__main__":

    '''
    jobs = Scraper.scrape(config.getFullDynamicURL())
    for job in jobs:
        print(f"Job: {job}\n\n")
        jobDetailPageURL = config.detailPageBaseUrl + job.get("refnr")
        print(f"JobDetailPageURL: {jobDetailPageURL}\n\n")
    '''
    Scraper.testCamoufox()