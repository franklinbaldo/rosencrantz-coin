import urllib.request
import urllib.parse
import sys
import xml.etree.ElementTree as ET

def search_arxiv(query, max_results=10):
    encoded_query = urllib.parse.quote(query)
    url = f'http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}'
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')

        root = ET.fromstring(data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        print(f"--- Results for '{query}' ---")
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
            published = entry.find('atom:published', ns).text[:10]
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')[:200]
            link = entry.find('atom:id', ns).text

            print(f"Title: {title}")
            print(f"Authors: {', '.join(authors)}")
            print(f"Date: {published}")
            print(f"Link: {link}")
            print(f"Summary: {summary}...")
            print()
    except Exception as e:
        print(f"Error: {e}")

if len(sys.argv) > 1:
    search_arxiv(sys.argv[1], 10)
