# # jobs/services/jsearch.py
# import os
# import requests

# def fetch_jobs(query, location, radius="", num_pages=1):
#     """
#     Fetch jobs from JSearch API
    
#     Args:
#         query: Job keywords (e.g., "Software Engineer")
#         location: City, State or Zip Code (e.g., "Austin, TX" or "78701")
#         radius: Search radius in miles (e.g., "10", "25") - optional
#         num_pages: Number of pages to fetch (each page has ~10 jobs)
    
#     Returns:
#         List of job dictionaries
#     """
#     all_jobs = []
    
#     # Get API key from environment
#     api_key = os.environ.get("JSEARCH_API_KEY")
    
#     # Debug: Check if API key exists
#     if not api_key:
#         print("ERROR - JSEARCH_API_KEY environment variable not set!")
#         return []
    
#     for page in range(1, num_pages + 1):
#         try:
#             url = "https://api.openwebninja.com/jsearch/search"
            
#             headers = {
#                 "X-RapidAPI-Key": api_key,
#                 "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
#             }
            
#             params = {
#                 "query": f"{query} in {location}",
#                 "page": str(page),
#                 "num_pages": "1"
#             }
            
#             # Add radius if specified
#             if radius:
#                 params["radius"] = radius
            
#             print(f"DEBUG - Fetching: '{query} in {location}' (radius: {radius or 'none'}, page {page})")
            
#             response = requests.get(url, headers=headers, params=params, timeout=10)
            
#             # Debug: Show response status
#             print(f"DEBUG - Response status: {response.status_code}")
            
#             response.raise_for_status()
            
#             data = response.json()
#             jobs = data.get("data", [])
            
#             print(f"DEBUG - Received {len(jobs)} jobs on page {page}")
            
#             if not jobs:
#                 break
            
#             all_jobs.extend(jobs)
            
#         except requests.exceptions.HTTPError as e:
#             print(f"ERROR - HTTP Error on page {page}: {e}")
#             if 'response' in locals():
#                 print(f"ERROR - Response text: {response.text[:500]}")
#             break
#         except Exception as e:
#             print(f"ERROR - Error fetching page {page}: {e}")
#             break
    
#     print(f"DEBUG - Total jobs fetched: {len(all_jobs)}")
#     return all_jobs

# jobs/services/jsearch.py
import os
import requests

def fetch_jobs(query, location, radius="", num_pages=1):
    """
    Fetch jobs from OpenWebNinja JSearch API
    """
    all_jobs = []

    # Get API key from environment
    api_key = os.environ.get("JSEARCH_API_KEY")

    if not api_key:
        print("ERROR - OPENWEBNINJA_API_KEY environment variable not set!")
        return []

    base_url = "https://api.openwebninja.com/jsearch/search"

    headers = {
    "X-API-Key": api_key,
    "Accept": "application/json"
    }


    for page in range(1, num_pages + 1):
        try:
            params = {
                "query": f"{query} in {location}",
                "page": page,
                "num_pages": 1
            }

            if radius:
                params["radius"] = radius

            print(
                f"DEBUG - Fetching: '{query} in {location}' "
                f"(radius: {radius or 'none'}, page {page})"
            )

            response = requests.get(
                base_url,
                headers=headers,
                params=params,
                timeout=10
            )

            print(f"DEBUG - Response status: {response.status_code}")

            response.raise_for_status()

            data = response.json()
            jobs = data.get("data", [])

            print(f"DEBUG - Received {len(jobs)} jobs on page {page}")

            if not jobs:
                break

            all_jobs.extend(jobs)

        except requests.exceptions.HTTPError as e:
            print(f"ERROR - HTTP Error on page {page}: {e}")
            print(response.text[:500])
            break
        except Exception as e:
            print(f"ERROR - Error fetching page {page}: {e}")
            break

    print(f"DEBUG - Total jobs fetched: {len(all_jobs)}")
    return all_jobs
