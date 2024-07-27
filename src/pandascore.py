import requests
import json
from dateutil.parser import parse
from datetime import datetime
from src.matches import Match


config = json.load(open('config.json', 'r'))

class PandaScore:
    def __init__(self, token: str):
        """
        Initialize the PandaScore class.

        Args:
            token (str): The API token for authentication.
        """
        self.token = token

    def get_upcomming_matches(self, number_of_matches=5) -> list:
        """
        Get a list of upcoming matches.

        Args:
            number_of_matches (int): The number of matches to retrieve. Default is 5.

        Returns:
            list: A list of upcoming matches.
        """
        url = "https://api.pandascore.co/valorant/matches/upcoming"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            matches = response.json()
            if matches :
                matches = matches[:number_of_matches]
                print("PandaScore API : Upcoming matches retrieved successfully")
            return matches
        else:
            print(f"{response.status_code} | Unable to retrieve upcoming matches")
            return None
        
    def get_matches_for_today(self) -> list:
        """
        Get a list of matches scheduled for today.

        Returns:
            list: A list of matches scheduled for today.
        """
        url = "https://api.pandascore.co/valorant/matches/upcoming"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)
        output = []

        if response.status_code == 200:
            matches = response.json()
            today_matches = [match for match in matches if parse(match['original_scheduled_at']).date() == datetime.now().date()]
            for match in today_matches:
                    output.append(Match(match))
            print("PandaScore API : Today's matches retrieved successfully")
            return output
        else:
            print(f"{response.status_code} | Unable to retrieve today's matches")
            return None
    
    def get_match_by_id(self, match_id: int) -> dict:
        """
        Get a match by its ID.

        Args:
            match_id (int): The ID of the match.

        Returns:
            dict: The match details.
        """
        url = f"https://api.pandascore.co/matches/{match_id}"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            match = response.json()
            print(f"Match '{match_id}' retrieved successfully")
            return match
        else:
            print(f"Unable to read match '{match_id}' | Error : {response.status_code}")
            return None
        
    def get_ongoing_matches(self) -> list:
        """
        Get a list of ongoing matches.

        Returns:
            list: A list of ongoing matches.
        """
        url = "https://api.pandascore.co/valorant/matches/running"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            matches = response.json()
            print("PandaScore API : Ongoing matches retrieved successfully")
            return matches
        else:
            print(f"{response.status_code} | Unable to retrieve ongoing matches")
            return None
    
    def get_past_matches(self, number_of_matches=5) -> list:
        """
        Get a list of past matches.

        Args:
            number_of_matches (int): The number of matches to retrieve. Default is 5.

        Returns:
            list: A list of past matches.
        """
        url = "https://api.pandascore.co/valorant/matches/past"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            matches = response.json()
            if matches:
                matches = matches[:number_of_matches]
                print("PandaScore API : Past matches retrieved successfully")
                return matches
            else:
                print(f"{response.status_code} No past matches found")
                return None
    
    def get_teams(self) -> list:
        """
        Get a list of teams.

        Returns:
            list: A list of teams.
        """
        url = "https://api.pandascore.co/valorant/teams"
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            teams = response.json()
            return teams
        else:
            return None
