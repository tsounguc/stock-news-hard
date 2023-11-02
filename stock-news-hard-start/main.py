import html
import os
from datetime import datetime, timedelta
# from twilio.rest import Client

import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
# HINT 2: Work out the value of 5% of yerstday's closing stock price.

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": "0PZIOS2AM0OHJL9R"
}
stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
yesterday_date = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
print(yesterday_date)
two_days_ago_date = (datetime.now() - timedelta(2)).strftime("%Y-%m-%d")
print(two_days_ago_date)
print(stock_data)
stock_time_series = stock_data["Time Series (Daily)"]
yesterday_closing_price = stock_data["Time Series (Daily)"][yesterday_date]["4. close"]
print(yesterday_closing_price)
closing_price_two_day_ago = stock_data["Time Series (Daily)"][yesterday_date]["4. close"]
print(closing_price_two_day_ago)
difference = abs(float(yesterday_closing_price) - float(closing_price_two_day_ago))
increment = float(yesterday_closing_price) * 0.05

if difference >= increment:
    print("Get News")
    print(difference)
    print(increment)



## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
# HINT 1: Think about using the Python Slice Operator

news_parameters = {
    "q": COMPANY_NAME,
    "apikey": "7cbf4c31ecbb4c62b7678f9204f84980"
}

news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
# HINT 1: Consider using a List Comprehension.

# Twilio Example
# account_sid = os.environ["Twilio_account_sid"]

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#                               body='Hi there',
#                               from_='+15017122661',
#                               to='+15558675310'
#                           )
#
# print(message.sid)

first_three_articles = news_data["articles"][:3]
news_list = [f'Headline:{html.unescape(article["title"])} Brief:{html.unescape(article["description"])}' for article in first_three_articles]
print(news_list)

# Send each article as a separate message via Twilio
# client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Send each article as a separate message
# for news in news_list:
#     message = client.message.create(body=news,
#                                     from_="+15017122661",
#                                     to="Your number")

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
