import requests

class NHLAPIWrapper:
    def __init__(self, base_url='https://api-web.nhle.com/', stats_url='https://api.nhle.com/stats/rest'):
        self.base_url = base_url
        self.stats_url = stats_url

    # Add your API methods here