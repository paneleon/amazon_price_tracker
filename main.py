import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

PRODUCT_URL = "https://www.amazon.ca/Instant-Pot-Ultra-Electric-Stainless/dp/B06Y1MP2PY/ref=sr_1_5?crid=2MY7OZALJN5P1&dchild=1&keywords=instant+pot&qid=1626667042&sprefix=insta%2Caps%2C207&sr=8-5"
BUY_PRICE = 120
FROM_EMAIL = "elya.studying@gmail.com"
FROM_EMAIL_PASSWORD = "alisa100"
TO_EMAIL = "paneleon06@gmail.com"

header = {
    "accept-language": "en-US",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
response = requests.get(PRODUCT_URL, headers=header)
product_website = response.text

soup = BeautifulSoup(product_website, "lxml")
print(soup.prettify())

price = soup.select("#priceblock_ourprice")[0].getText()

price_float = float(price.split("$")[1])
print(price_float)

product_title_tag = soup.select("#productTitle")[0].getText()
# The title was weirdly formatted with a lot of new lines in it
product_title_list = product_title_tag.split("\n")
product_title = ""
for title in product_title_list:
    if len(title) > 1:
        product_title = title
print(product_title)

if price_float < BUY_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as new_connection:
        new_connection.starttls()
        new_connection.login(user=FROM_EMAIL, password=FROM_EMAIL_PASSWORD)
        new_connection.sendmail(from_addr=FROM_EMAIL,
                                to_addrs=TO_EMAIL,
                                msg=f"Subject: Low Price Alert! \n\n{product_title} is now ${price_float} \nLink: {PRODUCT_URL}")