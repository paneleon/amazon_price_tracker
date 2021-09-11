import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os

PRODUCT_URL = "https://www.amazon.ca/Instant-Pot-Ultra-Electric-Stainless/dp/B06Y1MP2PY/ref=sr_1_5?crid=2MY7OZALJN5P1&dchild=1&keywords=instant+pot&qid=1626667042&sprefix=insta%2Caps%2C207&sr=8-5"
BUY_PRICE = 100
FROM_EMAIL = os.environ['SENDER-EMAIL']
FROM_EMAIL_PASSWORD = os.environ['EMAIL-PASSWORD']
TO_EMAIL = os.environ['RECEIVER-EMAIL']

# request header is needed to receive an actual website HTML
header = {
    "accept-language": "en-US",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
# makes a request to the webpage and retrieving its content
response = requests.get(PRODUCT_URL, headers=header)
product_website = response.text

# uses retrieved website and lxml parser to create a BeautifulSoup object
soup = BeautifulSoup(product_website, "lxml")
print(soup.prettify())

# gets the product price
price = soup.select("#priceblock_ourprice")[0].getText()

# gets the numeric value of price for further comparison
price_float = float(price.split("$")[1])
print(price_float)

# gets the product price
product_title_tag = soup.select("#productTitle")[0].getText()
# (The title was weirdly formatted with a lot of new lines in it)
product_title_list = product_title_tag.split("\n")
product_title = ""
for title in product_title_list:
    if len(title) > 1:
        product_title = title
print(product_title)

# if price is less than initial, then sends an email notification
if price_float < BUY_PRICE:
    # creates new connection
    with smtplib.SMTP("smtp.gmail.com", port=587) as new_connection:
        # puts the connection in Transport Layer Security mode for encryption
        new_connection.starttls()
        # logins on an SMTP server
        new_connection.login(user=FROM_EMAIL, password=FROM_EMAIL_PASSWORD)
        # sends an email with a subject line
        new_connection.sendmail(from_addr=FROM_EMAIL,
                                to_addrs=TO_EMAIL,
                                msg=f"Subject: Low Price Alert! \n\n{product_title} is now ${price_float} \nLink: {PRODUCT_URL}")