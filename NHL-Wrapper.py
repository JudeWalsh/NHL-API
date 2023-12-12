import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


class NHLAPIWrapper:
    def __init__(self, base_url='https://api-web.nhle.com/', stats_url='https://api.nhle.com/stats/rest'):
        self.base_url = base_url
        self.stats_url = stats_url

    def GetPlayerStats(self):
        for i in range(8):
            start = i*100
            url = self.stats_url + f"/en/skater/summary?limit=100&start={start}&sort=points&cayenneExp=seasonId=20232024"
            # Make a GET request
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON content of the response
                data = response.json()
                print(json.dumps(data, indent=4))
            else:
                # Print an error message if the request was not successful
                print("Error:", response.status_code, response.text)

    def playerBio(self, playerid):
        url = self.base_url + f"v1/player/{playerid}/landing"

        response = requests.get(url)

        data = response.json()

        final = {}

        final['height'] = data['heightInInches']
        final['weight'] = data['weightInPounds']
        final['position'] = data['position']
        final['shootscatches'] = data['shootsCatches']

        birthdate = data['birthDate']
        date_format = "%Y-%m-%d"

        # Convert the string to a datetime object
        birthdate = datetime.strptime(birthdate, date_format)

        current_datetime = datetime.now()

        difference = relativedelta(current_datetime, birthdate)

        # Extract the number of years from the difference
        age = difference.years

        final['age'] = age

        draft_year = int(data['draftDetails']['year'])

        final['draft year'] = draft_year

        return final

    def playerSummary(self, playerid):
        url = self.base_url + f"v1/player/{playerid}/landing"

        response = requests.get(url)

        data = response.json()

        '''
        games played
        goals
        assists
        points
        plus minus
        pim
        p\GP
        EVG
        EVP
        PPG
        PPP
        SHG
        SHP
        OTG
        GWG
        S
        S%
        TOI/GP
        FOW%
        '''

        curr_season_stats = data['seasonTotals'][-1]

        keys_to_remove = ['gameTypeId', 'leagueAbbrev',
                          'teamName', 'sequence']

        for key in keys_to_remove:
            if key in curr_season_stats:
                curr_season_stats.pop(key)

        return curr_season_stats


obj = NHLAPIWrapper()

info = obj.playerSummary(8476453)

print(json.dumps(info, indent=4))

