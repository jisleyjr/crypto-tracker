# Coinbase

This application is meant to interact with the Coinbase API, it a built on Python and uses the SDK found here: https://github.com/coinbase/coinbase-advanced-py/

You'll need an API Key and Secret.

Set your API key and secret in your environment (make sure to put these in quotation marks). For example:
```
export COINBASE_API_KEY="organizations/{org_id}/apiKeys/{key_id}"
export COINBASE_API_SECRET="-----BEGIN EC PRIVATE KEY-----\nYOUR PRIVATE KEY\n-----END EC PRIVATE KEY-----\n"
```

Or set in the code:
```
from coinbase.rest import RESTClient

api_key = "organizations/{org_id}/apiKeys/{key_id}"
api_secret = "-----BEGIN EC PRIVATE KEY-----\nYOUR PRIVATE KEY\n-----END EC PRIVATE KEY-----\n"

client = RESTClient(api_key=api_key, api_secret=api_secret)
```