from decouple import config
from dydx3 import Client
from web3 import Web3
from constants import (
    HOST,
    ETH_ADDR,
    DYDX_API_KEY,
    DYDX_API_PASSPHRASE,
    DYDX_API_SECRET,
    STARK_PRIVATE_KEY,
    HTTP_PROVIDER
)

def connect_dydx():
    client = Client(
        host=HOST,
        api_key_credentials={
            "key": DYDX_API_KEY,
            "secret": DYDX_API_SECRET,
            "passphrase": DYDX_API_PASSPHRASE,
        },
        stark_private_key=STARK_PRIVATE_KEY,
        eth_private_key=config("ETH_PRIVATE_KEY"),
        default_ethereum_address=ETH_ADDR,
        web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER)),
    )
    account = client.private.get_account()
    account_id = account.data["account"]["id"]
    balance = account.data["account"]["quoteBalance"]
    print("Connected")
    print("id:", account_id)
    print("balance:", balance)
    return client