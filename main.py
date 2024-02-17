
import requests # get the webpage's html source code
import selectorlib # retrieve particular information from that html source code
import smtplib, ssl
import time
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
 
# Establsih a connection and a cursor
connection = sqlite3.connect("data.db")
 
# Function to obtain url and return the webpage's source code for the events
def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source
 
# Function to extract the events on the webpage
def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"] # this ** where we return a dict. The dict will return a key called 'tours
                                                # the value of the key 'tours' is '#displaytimer' which is the id of the header tag we want to extract
    return value
 

# Function to send an email to the user if a new event is found
def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "odioneseose@gmail.com"
    password = "dnywnzwqhpxzjerz"

    receiver = "odioneseose@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)
    print("Email was sent!")


# Function to write the events from the webpage into a .txt fil
def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row] # remove the spaces from each item in the list
    cursor = connection.cursor() # 'cursor' serves as an object that can execute sql queries
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row) # row is a list of three items, where each item will replace one '?' each and be added to the db
    connection.commit() # always commit when writing changes to the database

# Function to return the contents of the data.txt file
def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row] # remove the spaces from each item in the list
    band, city, date = row
    cursor = connection.cursor() # 'cursor' serves as an object that can execute sql queries
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date)) # we repeat the 'execute' method in the functions anytime they're needed
    rows = cursor.fetchall() # fetchall() returns a list of strings when used with 'execute()' and returns a list of tuples when used with 'executemany()'
    print(rows)
    return rows
   
 
 
if __name__ == "__main__":
    while True: # to execute everything in this loop every two seconds
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row: # this basically means if 'row' which is a list is not empty, non-empty list is True and and empty list is False
                store(extracted)
                send_email(message="Hey, new event was found!")
        time.sleep(2) # sets time delay for two seconds
                     # always checks for new events/tours every two seconds