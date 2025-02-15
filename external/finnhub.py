import finnhub
from global.models import HotTopic

finnhub_client = finnhub.Client(api_key="cuo888pr01qokt75ltcgcuo888pr01qokt75ltd0")

print(finnhub_client.ipo_calendar(_from="2024-02-15", to="2025-03-15"))
