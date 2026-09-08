import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import re
import json
import sys
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import requests
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

def get_urls_to_index(sitemap: Path) -> list[str]:
    tree = ET.parse(sitemap)
    return [element.text for element in tree.findall('.//{*}loc')
            if element.text and not element.text.endswith('.xml')]


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

def submit_to_indexnow(urls: list[str], api_key: str, site_url: str) -> None:
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
        "host": urlparse(site_url).netloc,
        "key": api_key,
        "keyLocation": f"{site_url.rstrip('/')}/{api_key}.txt",
        "urlList": urls
    }
    
    try:
        response = requests.post(
            INDEXNOW_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=30
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
    parser = argparse.ArgumentParser(description='Explicit post-deployment indexing notifications; never part of make site')
    parser.add_argument('--sitemap', type=Path, default=Path('dist/site/sitemap.xml'))
    parser.add_argument('--google-key', type=Path)
    parser.add_argument('--indexnow-key', type=Path)
    parser.add_argument('--site-url', default='https://hku.jacobshing.com/')
    args = parser.parse_args()
    if not args.google_key and not args.indexnow_key:
        parser.error('Supply --google-key and/or --indexnow-key to send notifications')
    try:
        urls = get_urls_to_index(args.sitemap)
        
        if not urls:
            print("WARNING: No URLs found to index.")
            print("\nIndexing requests completed!")
            return 0
        
        print(f"Found {len(urls)} URLs to index.\n")
        print("URLs to be indexed:\n\n" + "\n".join(urls))

        # Google Indexing API setup
        SCOPES = ["https://www.googleapis.com/auth/indexing"]
        GOOGLE_API_KEY_FILE = args.google_key
        
        try:
            if GOOGLE_API_KEY_FILE:
                credentials = ServiceAccountCredentials.from_json_keyfile_name(str(GOOGLE_API_KEY_FILE), scopes=SCOPES)
                auth_http = credentials.authorize(httplib2.Http(timeout=30))
                submit_to_google_indexing(urls, auth_http)
        except FileNotFoundError:
            print(f"WARNING: Google API key file not found at {GOOGLE_API_KEY_FILE}")
        except Exception as e:
            print(f"WARNING: Google Indexing API error: {str(e)}")
        
        # IndexNow API submission
        try:
            api_key = args.indexnow_key.read_text().strip() if args.indexnow_key else ""
            if api_key:
                submit_to_indexnow(urls, api_key, args.site_url)
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
    