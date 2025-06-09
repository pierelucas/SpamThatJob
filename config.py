from datetime import datetime, timezone
from urllib.parse import urlencode

'''
Everything we need for the base scraping
'''
baseHeaders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "correlation-id": "4c368a0d-e2f4-fd0f-af2b-0cdf663810ce",
    "X-API-Key": "jobboerse-jobsuche",
    "Origin": "https://www.arbeitsagentur.de",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=0",
    "TE": "trailers"
}

# Define the cookies to be sent with the request
# Note: requests library handles the 'Cookie' header automatically when 'cookies' parameter is used.
baseCookies = {
    "_pk_id.35.cfae": "8b5daffa6d796864.1748962596.",
    "_pk_ref.35.cfae": "[\"\",\"\",1748962596,\"https://www.google.com/\"]",
    "_pk_ses.35.cfae": "1",
    "cookie_consent": "accepted",
    "marketing_consent": "accepted",
    "personalization_consent": "accepted"
}

# REST Api

def generate_iso_utc_timestamp() -> str:
    """
    Generates the current UTC date and time in ISO 8601 format
    with milliseconds and 'Z' for Zulu time.
    Example: 2025-06-03T14:56:48.826Z
    """
    # Get the current time in UTC
    now_utc = datetime.now(timezone.utc)

    # Format the datetime object to the desired string format
    # %Y-%m-%dT%H:%M:%S handles YYYY-MM-DDTHH:MM:SS
    # %f gives microseconds, we need to slice it to 3 digits for milliseconds
    # and then append 'Z'
    formatted_time = now_utc.strftime('%Y-%m-%dT%H:%M:%S')
    milliseconds = now_utc.strftime('%f')[:3] # Get first 3 digits for milliseconds

    return f"{formatted_time}.{milliseconds}Z"

# Original GET Requests
# "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v5/jobs?angebotsart=1&was=it&wo=minden&umkreis=25&page=2&size=25&aktualisiertVor=2025-06-03T14:56:48.826Z&pav=false&facetten=veroeffentlichtseit,arbeitszeit,arbeitsort"

baseURL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v5/jobs"

params = {
    "angebotsart": "1",
    "was": "it",
    "wo": "minden",
    "umkreis": "25",
    "page": "2",
    "size": "25",
    "aktualisiertVor": generate_iso_utc_timestamp(), # Use the generated timestamp here
    "pav": "false",
    "facetten": "veroeffentlichtseit,arbeitszeit,arbeitsort"
}

def getFullDynamicURL() -> str:
    return f"{baseURL}?{urlencode(params)}"

'''
Everything we need for the Detailpage scraping
'''

# Define your custom headers as a dictionary
detailHeaders = {
    "Host": "www.arbeitsagentur.de",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i"
}

# Define your cookies as a dictionary
detailCookies = {
    "wwwarbeitsagentur": "0227eab218-f9b5-46zmN8_wp4Gf3pQLlQxLhjwchwByMMH8yAjsQMimQa8MTT8sDr7sp2rGI8Ftj_Dh0iJo0",
    "cookie_consent": "accepted",
    "personalization_consent": "accepted",
    "marketing_consent": "accepted",
    "_pk_ref.35.cfae": '["","",1748974995,"https://www.google.com/"]',
    "_pk_id.35.cfae": "8b5daffa6d796864.1748962596.",
    "_pk_ses.35.cfae": "1"
}

detailPageBaseUrl = "https://www.arbeitsagentur.de/jobsuche/jobdetail/"