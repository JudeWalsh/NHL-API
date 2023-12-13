import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


class NHLAPIWrapper:
    def __init__(self, base_url='https://api-web.nhle.com/', stats_url='https://api.nhle.com/stats/rest'):
        self.base_url = base_url
        self.stats_url = stats_url

    def summaryreport(self):
        '''
        Returns dict of every NHL Player's summary report

        PlayerID : {}

        A, EVG, EVP, FOW%, GWG, GP, G, lastname, OTG, PIM, playerID, plusMinus,
        P, P/GP, Pos, PPG, PPP, SeasonID, SHG, SHP, S/C, Shots, full name, team, TOI

        Faceoff winPCT is dropped as it is part of the faceoff report
        '''

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

        player_dict = {}
        for player in stats:
            playerID = int(player.pop('playerId'))
            player.pop('faceoffWinPct')
            player.pop('timeOnIcePerGame')
            player_dict[playerID] = player
        return player_dict

    def bioreport(self):
        '''
        Returns dict of every NHL Player's Bio report

        PlayerID : {}

        Where dict has the following stats:
        A, birth city, birth country, birthdate, birth state/province code,
        current team, draft overall, draft round, draft year, first season, games played,
        G, height, in hall of fame, last name, nationality code, playerid, points

        Following keys are popped as they are duplicated in the summary report:
        Assists, goals, points, games played, lastname, playerid, team, in hall of fame

        '''
        stats = []

        for i in range(8):
            start = i * 100
            url = self.stats_url + f"/en/skater/bios?limit=100&start={start}&sort=points&cayenneExp=seasonId=20232024"
            # Make a GET request
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                stats += data['data']
            else:
                # Print an error message if the request was not successful
                return [response.status_code, response.text]

        # player_dict = {int(player['playerId']): player for player in stats}

        player_dict = {}
        for player in stats:
            playerID = int(player.pop('playerId'))
            player.pop('goals')
            player.pop('assists')
            player.pop('points')
            player.pop('gamesPlayed')
            player.pop('lastName')
            player.pop('currentTeamAbbrev')
            player.pop('isInHallOfFameYn')
            player_dict[playerID] = player
        return player_dict


    def faceoffpercentages(self):
        '''
        Returns dict of every NHL Player's faceoff percentages

        PlayerID : {}

        Where dict has the following stats:
        D Zone FO%, D Zone FO total, evFO%, evFO total, FO%, GP, lastname, N Zone FO%, N Zone total,
        O Zone FO%, O Zone FO Totals, playerID, position, PPFO%, PPFO total, SeasonID, Shoots/catches,
        full name, team name, TOI, FO totals

        Following keys are popped as they are duplicated in the summary report:
        GP, lastname, playerID, position, seasonID, shoots/catches, name, team name, TOI

        '''

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

        player_dict = {}
        for player in stats:
            playerID = int(player.pop('playerId'))
            player.pop('gamesPlayed')
            player.pop('seasonId')
            player.pop('shootsCatches')
            player.pop('lastName')
            player.pop('teamAbbrevs')
            player.pop('timeOnIcePerGame')
            player.pop('positionCode')
            player_dict[playerID] = player
        return player_dict

    def faceoffwins(self):
        '''
        Returns dict of every NHL Player's faceoff totals

        PlayerID : {}

        Where dict has the following stats:
        D zone faceoff losses, D zone faceoff wins, D zone faceoffs, evFaceoffs, evFaceoffs lost, evFaceoffs won,
        faceoff win pct, N zone faceoffs, N zone faceoff wins, N zone faceoff losses, O zone faceoff wins, O zone faceoffs,
        O Zine faceoff losses, ppFaceoffs, ppFaceoffsLost, ppFaceoffs won, shFaceoffs, shfaceoffs lost, shFaceoffs won,
        total faceoffs, total faceoff wins, total faceoff losses

        '''

        stats = []

        for i in range(8):
            start = i * 100
            url = self.stats_url + f"/en/skater/faceoffwins?limit=100&start={start}&sort=totalFaceoffs&cayenneExp=seasonId=20232024"
            # Make a GET request
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                stats += data['data']
            else:
                # Print an error message if the request was not successful
                return [response.status_code, response.text]

        player_dict = {}
        for player in stats:
            playerID = int(player.pop('playerId'))
            player.pop('gamesPlayed')
            player.pop('lastName')
            player.pop('positionCode')
            player.pop('seasonId')
            player.pop('skaterFullName')
            player.pop('teamAbbrevs')
            player_dict[playerID] = player
        return player_dict

    def miscreport(self):
        '''
        Returns dict of every NHL Player's miscellaneous stats

        PlayerID : {}

        Where dict has the following stats:
        blocked shots, blocked shots per 60, empty net assists, empty net goals,
        empty net points, first goals, giveaways, giveaways per 60, hits,
        hits per 60, missed shot crossbar, missed shot goalpost, missed shot over net,
        missed shot wide of not, missed shots, takeaways, takeaways per 60

        '''

        stats = []

        for i in range(8):
            start = i * 100
            url = self.stats_url + f"/en/skater/realtime?limit=100&start={start}&sort=hits&cayenneExp=seasonId=20232024"
            # Make a GET request
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                stats += data['data']
            else:
                # Print an error message if the request was not successful
                return [response.status_code, response.text]

        player_dict = {}
        for player in stats:
            playerID = int(player.pop('playerId'))
            player.pop('gamesPlayed')
            player.pop('lastName')
            player.pop('otGoals')
            player.pop('positionCode')
            player.pop('seasonId')
            player.pop('shootsCatches')
            player.pop('skaterFullName')
            player.pop('teamAbbrevs')
            player.pop('timeOnIcePerGame')
            player_dict[playerID] = player
        return player_dict

    def timeonice(self):
        '''
        Returns dict of every NHL Player's time on ice stats

        PlayerID : {}

        Where dict has the following stats:
        evTOI, evTOI/G, otTOI, otTOI/G, ppTOI, ppTOI/G, shTOI, shTOI/G, shifts, shifts/G,
        TOI, TOI/G, TOI/shift

        '''

        stats = []

        for i in range(8):
            start = i * 100
            url = self.stats_url + f"/en/skater/timeonice?limit=100&start={start}&sort=timeOnIce&cayenneExp=seasonId=20232024"
            # Make a GET request
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                stats += data['data']
            else:
                # Print an error message if the request was not successful
                return [response.status_code, response.text]

        player_dict = {}
        for player in stats:
            playerID = int(player.pop('playerId'))
            player.pop('gamesPlayed')
            player.pop('lastName')
            player.pop('positionCode')
            player.pop('seasonId')
            player.pop('shootsCatches')
            player.pop('skaterFullName')
            player.pop('teamAbbrevs')
            player_dict[playerID] = player
        return player_dict

obj = NHLAPIWrapper()

base_stats = obj.faceoffwins()

print(json.dumps(base_stats[8476468], indent=4))
