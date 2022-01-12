import pandas as pd
from pathlib import Path
from solana.rpc.api import Client

crypto_folder = Path('C:/Users/andre/Desktop/crypto')
crypto_transactions = crypto_folder / 'my_transactions.pkl'

# all_addresses = [
#     '2AQdpHJ2JpcEgPiATUXjQxA8QmafFegfQwSLWSprPicm',
#     'Vote111111111111111111111111111111111111111',
#     'fake address',
# ]

all_addresses = [
    'CHEaPfCeuyoPRc7n9NJx4vB3uHSrBKRyU6wcgbAKTmG3',
    'fake address',
]

# endpoint = 'https://api.devnet.solana.com'    # probably for `developing`
# endpoint = 'https://api.testnet.solana.com'   # probably for `testing`
endpoint = 'https://api.mainnet-beta.solana.com'
# endpoint = 'https://solana-api.projectserum.com'

solana_client = Client(endpoint)

for address in all_addresses:
    print('address:', address)

    # result = solana_client.get_confirmed_signature_for_address2(address, limit=1)
    result = solana_client.get_signatures_for_address(
        address)  # , before='89Tv9s2uMGaoxB8ZF1LV9nGa72GQ9RbkeyCDvfPviWesZ6ajZBFeHsTPfgwjGEnH7mpZa7jQBXAqjAfMrPirHt2')



    df = pd.DataFrame(result)
    df.to_pickle(crypto_transactions, protocol=4)

    if 'result' in result:
        print('len:', len(result['result']))

        # I use `[:5]` to display only first 5 values
        for number, item in enumerate(result['result'][:5], 1):
            print(number, 'signature:', item['signature'])

        # check if there is `4SNQ4h1vL9GkmSnojQsf8SZyFvQsaq62RCgops2UXFYag1Jc4MoWrjTg2ELwMqM1tQbn9qUcNc4tqX19EGHBqC5u`
        for number, item in enumerate(result['result'], 1):
            if item['signature'].startswith('4SN'):
                print('found at', number, '>>>', item['signature'])

    else:
        # error message
        print(result)

    print('---')

    # solana_client.get_account_info(address)