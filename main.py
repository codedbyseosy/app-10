
import requests # get the webpage's html source code
import selectorlib # retrieve particular information from that html source code
 
URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
 
 
def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source
 
 
def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"] # this ** where we return a dict. The dict will return a key called 'tours
                                                # the value of the key 'tours' is '#displaytimer' which is the id of the header tag we want to extract
    return value
 
 
def send_email():
    print('Email was sent')
 
 
def store(extracted):
    with open("data.txt", 'a') as file:  # 'a' for append
        file.write(extracted + "\n")
 
 
def read():
    with open("data.txt", 'r') as file:
        return file.read()  # Call the read() method to get the content of the file
 
 
if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read()
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email()