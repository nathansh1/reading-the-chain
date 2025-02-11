import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

TOKEN_ADDRESS = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
SOL_ADDRESS = "So11111111111111111111111111111111111111112"
url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"

token_response = requests.post(
    url,
    headers={"Content-Type":"application/json"},
    json={
        "jsonrpc":"2.0",
        "id":1,
        "method":"getAsset",
        "params":{"id":TOKEN_ADDRESS}
    }
)

sol_response = requests.post(
    url,
    headers={"Content-Type":"application/json"},
    json={
        "jsonrpc":"2.0",
        "id":1,
        "method":"getAsset",
        "params":{"id":SOL_ADDRESS}
    }
)

token_response = token_response.json()
sol_response = sol_response.json()

with open("token_response.json", "w") as file:
    json.dump(token_response, file, indent=4)

if "error" in token_response:
    print("API Error:", token_response["error"]["message"])
else:
    metadata = token_response.get("result", {}).get("content", {}).get("metadata", {})

    name = metadata.get("name", "N/A")

    # result -> content -> links -> image
    image = token_response.get("result").get("content").get("links").get("image")

    ticker = metadata.get("symbol", "N/A")

    token_info = token_response.get("result", {}).get("token_info", {})

    token_usd_price = token_info.get("price_info", {}).get("price_per_token", "N/A")
    sol_price = sol_response.get("result").get("token_info").get("price_info").get("price_per_token")
    token_sol_price = token_usd_price / sol_price

    total_supply = token_info.get("supply")

    fdv = token_usd_price * total_supply

    print(f"\nToken Name: {name}")
    print(f"Image: {image}")
    print(f"Ticker: {ticker}")
    print(f"Price in SOL: {token_sol_price}")
    print(f"Price in USD: {token_usd_price} ")
    # social links
    print(f"Total Supply: {total_supply}")
    print(f"FDV: {fdv}")