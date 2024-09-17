import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv('config.env')
STOCK = "GOOG"
COMPANY_NAME = "Google"
api_key_1 = os.getenv('API_KEY_1')  # Alpha Vantage
api_key_2 = os.getenv('API_KEY_2')  # News Api
my_email = os.getenv('MY_EMAIL')
my_password = os.getenv('MY_PASSWORD')


def price_fluctuation(new_price, old_price):
    percentage_fluctuation = ((new_price - old_price) / old_price) * 100
    return percentage_fluctuation


alphavantage_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey=api_key_1'
alphavantage_r = requests.get(alphavantage_url)
alphavantage_data = alphavantage_r.json()
current_date = datetime.now()
new_date = current_date - timedelta(days=1)
old_date = current_date - timedelta(days=2)

formatted_new_date = new_date.strftime("%Y-%m-%d")
formatted_old_date = old_date.strftime("%Y-%m-%d")

new_price = float(alphavantage_data["Time Series (Daily)"][formatted_new_date]["4. close"])
old_price = float(alphavantage_data["Time Series (Daily)"][formatted_old_date]["4. close"])

news_date = current_date - timedelta(days=3)
formatted_news_date = news_date.strftime("%Y-%m-%d")
newsapi_url = f'https://newsapi.org/v2/everything?q={STOCK}&from={formatted_news_date}&apiKey=api_key_2'
newsapi_r = requests.get(newsapi_url)
newsapi_data = newsapi_r.json()

print(newsapi_data)
print(api_key_1, api_key_2)
# news_1 = newsapi_data["articles"][0]["title"]
# news_2 = newsapi_data["articles"][1]["title"]
# news_3 = newsapi_data["articles"][2]["title"]
#
# price_change = price_fluctuation(new_price, old_price)
# if price_change > 1 or price_change < -1:
#     email_content = f"""
#                 {COMPANY_NAME}: STOCK {old_price} -> {new_price}: {round(price_change, 2)}%
#                 News:
#                 {news_1}.
#                 {news_2}.
#                 {news_3}.
#             """
#
#     msg = MIMEText(email_content, 'plain', 'utf-8')
#     msg['Subject'] = 'Stock News!'
#     msg['From'] = my_email
#     msg['To'] = my_email
#
#     with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
#         connection.starttls()
#         connection.login(user=my_email, password=my_password)
#         connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=msg.as_string())
