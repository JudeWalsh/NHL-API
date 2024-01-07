import requests
import pandas as pd
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

    def full_report(self):
        player_dict = {}
        summary = self.summaryreport()
        misc = self.miscreport()
        bio = self.bioreport()
        TOI = self.timeonice()
        FO_percent = self.faceoffpercentages()
        FO_wins = self.faceoffwins()

        for key in summary.keys():
            # Combine values under the same key from all dictionaries
            player_dict[key] = {
                **summary.get(key, {}),
                **misc.get(key, {}),
                **bio.get(key, {}),
                **TOI.get(key, {}),
                **FO_percent.get(key, {}),
                **FO_wins.get(key, {})
            }
        return player_dict

    def skater_summary(self, skaterID):
        '''

        Retrieve summary report for a player for each season he played

        :param skaterID: playerID of the player to get reports from
        :return: list of dict where each dict is a season's summary report for the player
        '''

        final = []

        url = self.stats_url + f"/en/skater/summary?sort=seasonId&cayenneExp=playerId={skaterID}"
        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
        else:
            # Print an error message if the request was not successful
            return [response.status_code, response.text]

        column_order = ["teamAbbrevs", "shootsCatches", "positionCode", "gamesPlayed",
                        "goals", "assists", "points", "plusMinus", "penaltyMinutes",
                        "pointsPerGame", "evGoals", "evPoints", "ppGoals", "ppPoints",
                        "shGoals", "shPoints", "otGoals", "gameWinningGoals", "shots",
                        "shootingPct", "timeOnIcePerGame", "faceoffWinPct"]

        for season in stats:
            seasonId = season.pop('seasonId')
            reordered_season = {key: season[key] for key in column_order if key in season}

            temp_dict = {seasonId: reordered_season}
            final.append(temp_dict)

        return final

    def skater_bio(self, skaterID):
        '''

        Retrieve bio report for a player for each season he played

        :param skaterID: playerID of the player to get report from
        :return: dict of the player's bio information
        '''
        final = []

        url = self.stats_url + f"/en/skater/bios?sort=height&cayenneExp=playerId={skaterID}"
        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            stats = data['data'][0]
        else:
            # Print an error message if the request was not successful
            return [response.status_code, response.text]

        stats.pop("currentTeamAbbrev")
        stats.pop("shootsCatches")
        stats.pop("positionCode")
        stats.pop("skaterFullName")
        stats.pop("currentTeamName")
        stats.pop("lastName")

        stats["career games played"] = stats.pop("gamesPlayed")
        stats["career assists"] = stats.pop("assists")
        stats["career points"] = stats.pop("points")
        stats["career goals"] = stats.pop("goals")
        stats["first season"] = stats.pop("firstSeasonForGameType")
        stats["birth country"] = stats.pop("birthCountryCode")
        stats["birth city"] = stats.pop("birthCity")
        stats["birth state/province"] = stats.pop("birthStateProvinceCode")
        stats["nationality"] = stats.pop("nationalityCode")
        stats["Hall of Fame"] = stats.pop("isInHallOfFameYn")

        column_order = ["playerId", "birthDate", "birth country", "birth city", "birth state/province",
                        "nationality", "height", "weight", "draftYear", "draftRound",
                        "draftOverall", "first season", "Hall of Fame", "career games played",
                        "career goals", "career assists", "career points", "otGoals", "gameWinningGoals",
                        "shots", "shootingPct", "timeOnIcePerGame", "faceoffWinPct"]

        reordered_stats = {key: stats[key] for key in column_order if key in stats}

        return reordered_stats

    def skater_FO_percent(self, skaterID):
        '''

        Retrieve Faceoff percent report for a player for each season he played

        :param skaterID: playerID of the player to get reports from
        :return: list of dict where each dict is a season's faceoff percent report for the player
        '''
        final = []

        column_order = ["teamAbbrevs", "shootsCatches", "positionCode", "gamesPlayed",
                        "goals", "assists", "points", "plusMinus", "penaltyMinutes",
                        "pointsPerGame", "evGoals", "evPoints", "ppGoals", "ppPoints",
                        "shGoals", "shPoints", "otGoals", "gameWinningGoals", "shots",
                        "shootingPct", "timeOnIcePerGame", "faceoffWinPct"]

        url = self.stats_url + f"/en/skater/faceoffpercentages?sort=seasonId&cayenneExp=playerId={skaterID}"
        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
        else:
            # Print an error message if the request was not successful
            return [response.status_code, response.text]

        for season in stats:
            seasonId = season.pop('seasonId')
            temp_dict = {seasonId: season}
            final.append(temp_dict)

        return final

    def skater_FO_wins(self, skaterID):
        '''

        Retrieve Faceoff win report for a player for each season he played

        :param skaterID: playerID of the player to get reports from
        :return: list of dict where each dict is a season's faceoff win report for the player
        '''
        final = []

        url = self.stats_url + f"/en/skater/faceoffwins?sort=seasonId&cayenneExp=playerId={skaterID}"
        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
        else:
            # Print an error message if the request was not successful
            return [response.status_code, response.text]

        for season in stats:
            seasonId = season.pop('seasonId')
            temp_dict = {seasonId: season}
            final.append(temp_dict)

        return final

    def skater_misc(self, skaterID):
        '''

        Retrieve miscellaneous percent report for a player for each season he played

        :param skaterID: playerID of the player to get reports from
        :return: list of dict where each dict is a season's miscellaneous report for the player
        '''
        final = []

        url = self.stats_url + f"/en/skater/realtime?sort=seasonId&cayenneExp=playerId={skaterID}"
        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
        else:
            # Print an error message if the request was not successful
            return [response.status_code, response.text]

        for season in stats:
            seasonId = season.pop('seasonId')
            temp_dict = {seasonId: season}
            final.append(temp_dict)

        return final

    def skater_TOI(self, skaterID):
        '''

        Retrieve time on ice percent report for a player for each season he played

        :param skaterID: playerID of the player to get reports from
        :return: list of dict where each dict is a season's time on ice report for the player
        '''
        final = []

        url = self.stats_url + f"/en/skater/timeonice?sort=seasonId&cayenneExp=playerId={skaterID}"
        # Make a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
        else:
            # Print an error message if the request was not successful
            return [response.status_code, response.text]

        for season in stats:
            seasonId = season.pop('seasonId')
            temp_dict = {seasonId: season}
            final.append(temp_dict)

        return final

    def skater_full_report(self, skaterID):
        '''
        performs a full report on the skater from the following NHL.com reports: summary, bio,
        faceoff wins and percentages, miscellaneous and time on ice
        :param skaterID: unique identifier for a specific skater
        :return: full report separated by season in a JSON
        '''

        final = []

        summary = self.skater_summary(skaterID)
        bio = self.skater_bio(skaterID)
        FO_P = self.skater_FO_percent(skaterID)
        FO_W = self.skater_FO_wins(skaterID)
        misc = self.skater_misc(skaterID)
        TOI = self.skater_TOI(skaterID)

        # Combine reports into a list
        reports = [summary, FO_P, FO_W, misc, TOI]

        # Create a dictionary to store merged data based on season
        merged_data_dict = {}

        # Iterate through each report
        for report in reports:
            for season_data in report:
                season_key, season_stats = next(iter(season_data.items()))

                # If the season is already in the merged_data_dict, update it; otherwise, add a new entry
                if season_key in merged_data_dict:
                    merged_data_dict[season_key].update(season_stats)
                else:
                    merged_data_dict[season_key] = season_stats

        # Convert the merged_data_dict into a list of dictionaries
        merged_data = [{"Season": season, **stats} for season, stats in merged_data_dict.items()]

        for season in merged_data:
            season.update(bio)

        return merged_data

    def skater_report_csv(self, skater_report):
        '''
        Takes the report written by self.skater_full_report and writes it to csv

        :param skater_report: report written by skater_full_report
        :return: True if success
        '''

        top_season = skater_report[0]
        name = top_season['skaterFullName']

        df = pd.DataFrame(skater_report)

        # Writing to Excel (xlsx)
        xlsx_file_path = f"{name} full report.xlsx"
        df.to_excel(xlsx_file_path, index=False)
        print(f"Excel file '{xlsx_file_path}' has been created.")



obj = NHLAPIWrapper()

base_stats = obj.skater_misc(8475168)

# obj.skater_report_csv(base_stats)

print(json.dumps(base_stats, indent=4))
