import re
import json
import sys
import requests
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

def get_urls_to_index() -> list[str]:
    """
    Retrieve a list of URLs that need to be indexed from the sitemap.

    Returns:
        list[str]: A list of URLs to be indexed.
    """
    PATTERN = r"<loc>(.*?)</loc>"
    urls = []
    try:
        with open("./gh-out/sitemap.xml", "r", encoding="utf-8") as f:
            while (line := f.readline()):
                match = re.search(PATTERN, line)
                if match:
                    urls.append(match.group(1))
    except FileNotFoundError:
        print("WARNING: Sitemap file not found at ./gh-out/sitemap.xml")
    except Exception as e:
        print(f"WARNING: Error reading sitemap: {str(e)}")
    return urls

def get_indexnow_key() -> str:
    """
    Retrieve the IndexNow key from a local file.

    Returns:
        str: The IndexNow key.
    """
    try:
        with open("./secrets/indexnowkey33fe8f8f945.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("WARNING: IndexNow key file not found at ./secrets/indexnowkey33fe8f8f945.txt")
        return ""
    except Exception as e:
        print(f"WARNING: Error reading IndexNow key: {str(e)}")
        return ""

def submit_to_google_indexing(urls: list[str], auth_http) -> None:
    """
    Submit URLs to Google Indexing API in batches.
    
    Args:
        urls: List of URLs to submit
        auth_http: Authorized HTTP client
    """
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    
    print(f"Submitting {len(urls)} URLs to Google Indexing API...")
    
    for i, url in enumerate(urls, 1):
        content = {
            "url": url,
            "type": "URL_UPDATED"
        }
        
        try:
            response, body = auth_http.request(
                ENDPOINT,
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps(content)
            )
            
            if response.status == 200:
                print(f"  [{i}/{len(urls)}] ✓ {url}")
            else:
                print(f"  [{i}/{len(urls)}] WARNING: Failed - Status: {response.status}")
                print(f"      Response: {body.decode('utf-8')}")
        except Exception as e:
            print(f"  [{i}/{len(urls)}] WARNING: {url} - {str(e)}")

def submit_to_indexnow(urls: list[str], api_key: str) -> None:
    """
    Submit URLs to IndexNow API.
    
    Args:
        urls: List of URLs to submit
        api_key: IndexNow API key
    """
    INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
    
    print(f"\nSubmitting {len(urls)} URLs to IndexNow...")
    
    # IndexNow allows batch submission
    payload = {
        "host": "hku.jacobshing.com",
        "key": api_key,
        "keyLocation": f"https://hku.jacobshing.com/indexnowkey33fe8f8f945.txt",
        "urlList": urls
    }
    
    try:
        response = requests.post(
            INDEXNOW_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
        if response.status_code == 200:
            print(f"  ✓ Successfully submitted all URLs")
        elif response.status_code == 202:
            print(f"  ✓ URLs accepted for indexing")
        else:
            print(f"  WARNING: Failed with status {response.status_code}")
            print(f"      Response: {response.text}")
    except Exception as e:
        print(f"  WARNING: {str(e)}")

def main():
    try:
        urls = get_urls_to_index()
        
        if not urls:
            print("WARNING: No URLs found to index.")
            print("\nIndexing requests completed!")
            return 0
        
        print(f"Found {len(urls)} URLs to index.\n")

        # Google Indexing API setup
        SCOPES = ["https://www.googleapis.com/auth/indexing"]
        GOOGLE_API_KEY_FILE = "./secrets/google_indexing_api_key.json"
        
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                GOOGLE_API_KEY_FILE, scopes=SCOPES
            )
            auth_http = credentials.authorize(httplib2.Http())
            submit_to_google_indexing(urls, auth_http)
        except FileNotFoundError:
            print(f"WARNING: Google API key file not found at {GOOGLE_API_KEY_FILE}")
        except Exception as e:
            print(f"WARNING: Google Indexing API error: {str(e)}")
        
        # IndexNow API submission
        try:
            api_key = get_indexnow_key()
            if api_key:
                submit_to_indexnow(urls, api_key)
            else:
                print("\nWARNING: Skipping IndexNow submission due to missing API key")
        except Exception as e:
            print(f"WARNING: IndexNow API error: {str(e)}")
        
        print("\nIndexing requests completed!")
        return 0
    except Exception as e:
        print(f"WARNING: Unexpected error in main: {str(e)}")
        return 0

if __name__ == "__main__":
    sys.exit(main())
    