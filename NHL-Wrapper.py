import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


class NHLAPIWrapper:
    def __init__(self, base_url='https://api-web.nhle.com/', stats_url='https://api.nhle.com/stats/rest'):
        self.base_url = base_url
        self.stats_url = stats_url

    def allskaterstats(self):

        stats = []

        for i in range(8):
            start = i*100
            url = self.stats_url + f"/en/skater/summary?limit=100&start={start}&sort=points&cayenneExp=seasonId=20232024"
            # Make a GET request
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                stats += data['data']
            else:
                # Print an error message if the request was not successful
                return [response.status_code, response.text]

        player_dict = {int(player['playerId']): player for player in stats}

        return player_dict

    def skaterbio(self, playerid):
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

    def skatersummary(self, playerid):
        url = self.base_url + f"v1/player/{playerid}/landing"

        response = requests.get(url)

        data = response.json()

        curr_season_stats = data['seasonTotals'][-1]

        keys_to_remove = ['gameTypeId', 'leagueAbbrev',
                          'teamName', 'sequence']

        for key in keys_to_remove:
            if key in curr_season_stats:
                curr_season_stats.pop(key)

        return curr_season_stats

    def faceoffs(self):

        stats = []

        for i in range(8):
            start = i * 100
            url = self.stats_url + f"/en/skater/faceoffpercentages?limit=100&start={start}&sort=totalFaceoffs&cayenneExp=seasonId=20232024"
            # Make a GET request
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                stats += data['data']
            else:
                # Print an error message if the request was not successful
                return [response.status_code, response.text]

        player_dict = {int(player['playerId']): player for player in stats}

        return player_dict

obj = NHLAPIWrapper()

info = obj.skatersummary(8476468)
base_stats = obj.allskaterstats()
faceoff_stats = obj.faceoffs()
#
print(json.dumps(info, indent=4))
print(json.dumps(base_stats[8476468], indent=4))
print(json.dumps(faceoff_stats[8476468], indent=4))

keys_set1 = set(info.keys())
keys_set2 = set(base_stats[8476468].keys())
keys_set3 = set(faceoff_stats[8476468].keys())

# Check for intersection (common keys) between sets
common_keys = keys_set1.intersection(keys_set2, keys_set3)

if common_keys:
    print("Duplicate keys found:")
    print(common_keys)
else:
    print("No duplicate keys found.")