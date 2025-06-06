from datetime import datetime, timezone
from urllib.parse import urlencode

 # Define the headers to be sent with the request
headers = {
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
cookies = {
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

base_url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v5/jobs"

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

def get_full_dynamic_url() -> str:
    return f"{base_url}?{urlencode(params)}"

# Job Detail Page

detailpage_url = "https://www.arbeitsagentur.de/jobsuche/jobdetail/"