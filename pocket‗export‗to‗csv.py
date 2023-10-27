import argparse
import csv
from bs4 import BeautifulSoup
import requests

def get_title_from_url(url):
    """
    Given a URL, fetch the web page and parse it to retrieve the title.
    
    Args:
    url (str): The URL of the web page to fetch.
    
    Returns:
    str: The title of the web page, or the URL itself if the title couldn't be retrieved.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else url
    return title.strip()

def convert_html_to_csv(input_html, output_csv):
    """
    Convert a list of links in an HTML file to a CSV file.
    
    The function reads an HTML file, finds all the anchor tags, extracts the text and the href attribute, 
    and writes them to a CSV file. If the text and the href are the same, it fetches the web page and uses its title as the text.
    
    Args:
    input_html (str): Path to the input HTML file.
    output_csv (str): Path to the output CSV file.
    """
    with open(input_html, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    links = soup.find_all('a')
    link_data = [(link.get_text(strip=True), link.get('href')) for link in links]

    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        csvwriter.writerow(["Title", "URL"])

        for title, url in link_data:
            if title == url:
                title = get_title_from_url(url)
            csvwriter.writerow([title, url])

if __name__ == "__main__":
    """
    Command-line tool for converting a list of links in an HTML file to a CSV file.
    
    The tool takes two arguments:
    - The path to the input HTML file.
    - The path to the output CSV file.
    """
    parser = argparse.ArgumentParser(description='Convert HTML links to CSV format.')
    parser.add_argument('input_html', help='Path to the input HTML file')
    parser.add_argument('output_csv', help='Path to the output CSV file')
    args = parser.parse_args()

    convert_html_to_csv(args.input_html, args.output_csv)
