# PiereLucas 05.06.2025

import requests
import json

class Scraper():

    def scrapeJobsFromJoboerse(self, url) -> list | None:
        """
        Fetches job offers from the given API URL with custom headers and cookies,
        then saves the 'stellenangebote' to a text file.
        The filename includes the current date and key parameters from the URL.
        """

        try:
            # Make the GET request to the API with specified headers and cookies
            response = requests.get(url, headers=config.headers, cookies=config.cookies)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Parse the JSON response
            data = response.json()

            # Extract "stellenangebote"
            job_offers = data.get("stellenangebote", [])

            return job_offers

        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None
        except json.JSONDecodeError:
            print("Error: Could not decode JSON response. Please check the API response format.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def scrapeDetailePageFromJoebboerse(self, url: str):
        return
