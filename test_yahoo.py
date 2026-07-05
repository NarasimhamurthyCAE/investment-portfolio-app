from api.yahoo_client import YahooClient

client = YahooClient()

price = client.latest_price("INFY.NS")

print(price)