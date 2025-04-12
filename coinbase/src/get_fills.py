from coinbase.rest import RESTClient
from json import dumps
import json

client = RESTClient()

# Create a variable to hold the year
year = 2024

print(f"Get transactinons for year {year}")

# Get fills
fills = client.get_fills(
    start_sequence_timestamp=f"{year}-01-01T00:00:00Z",
    end_sequence_timestamp=f"{year}-12-31T23:59:59Z",
)

order_dict = dumps(fills.to_dict(), indent=2)

output_filename = f"files/fills_{year}.json"

with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(fills.to_dict(), f, ensure_ascii=False, indent=4)

print(f"Fills for {year} saved to {output_filename}")
