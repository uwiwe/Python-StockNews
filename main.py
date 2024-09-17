import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv('config.env')
STOCK = "NVDA"
COMPANY_NAME = "Nvidia"
api_key_1 = os.getenv('API_KEY_1')  # Alpha Vantage
api_key_2 = os.getenv('API_KEY_2')  # News Api
my_email = os.getenv('MY_EMAIL')
my_password = os.getenv('MY_PASSWORD')


def price_fluctuation(new_price, old_price):
    percentage_fluctuation = ((new_price - old_price) / old_price) * 100
    return percentage_fluctuation


alphavantage_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey=api_key_1'
alphavantage_r = requests.get(alphavantage_url)
alphavantage_data = alphavantage_r.json()["Time Series (Daily)"]
alphavantage_data_list = [value for (key, value) in alphavantage_data.items()]
yesterday_data = alphavantage_data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

day_before_yesterday_data = alphavantage_data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

newsapi_url = f'https://newsapi.org/v2/everything?qInTitle={COMPANY_NAME}&apiKey=api_key_2'
newsapi_r = requests.get(newsapi_url)
newsapi_articles = newsapi_r.json()["articles"]

three_articles = newsapi_articles[:3]
formatted_articles = [
    f"{article['title']}" for article in three_articles]

price_change = price_fluctuation(yesterday_closing_price, day_before_yesterday_closing_price)
if abs(price_change) > 1:
    email_content = f"""
        {COMPANY_NAME}: STOCK {day_before_yesterday_closing_price} -> {yesterday_closing_price}: {round(price_change, 2)}%
        News:
        {formatted_articles[0]}.
        {formatted_articles[1]}.
        {formatted_articles[2]}.
        """

    msg = MIMEText(email_content, 'plain', 'utf-8')
    msg['Subject'] = 'Stock News!'
    msg['From'] = my_email
    msg['To'] = my_email

    print(email_content)
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=msg.as_string())
