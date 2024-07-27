import nextcord 
from dateutil.parser import parse


class Match:
    def __init__(self, match) -> None:
        """
        Initialise un objet Match avec les informations fournies.

        :param match: Les informations du match.
        :type match: dict
        """
        self.title: str = match['name']
        self.id: int = match['id']
        self.date = parse(match['original_scheduled_at'])
        if len(match['opponents']) == 2:
            self.opponents: list = [match['opponents'][0]['opponent']['name'], match['opponents'][1]['opponent']['name']]
            self.short_title: str = f"{match['opponents'][0]['opponent']['acronym']} vs {match['opponents'][1]['opponent']['acronym']}"
        else:
            self.opponents: list = ["TBD", "TBD"]
            self.short_title: str = f"To be determined (or data not available)"
        self.league: str = match['league']['name']
        self.series: str = match['serie']['full_name']
        self.status: str = "open"
        try:
            self.stream: str = match['streams_list'][0]['raw_url']
        except IndexError:
            self.stream: str = "https://www.twitch.tv/valorant_fr"
        self.color: int = 0x00ff00
        self.slugs: list = [match['opponents'][0]['opponent']['slug'], match['opponents'][1]['opponent']['slug']]
    
    def __repr__(self) -> str:
        """
        Retourne une représentation sous forme de chaîne de caractères de l'objet Match.

        :return: La représentation de l'objet Match.
        :rtype: str
        """
        return f"{self.title} - {self.date} - {self.opponents[0]} vs {self.opponents[1]} - {self.league} \n"
    
    def __str__(self) -> str:
        """
        Retourne une représentation sous forme de chaîne de caractères de l'objet Match.

        :return: La représentation de l'objet Match.
        :rtype: str
        """
        return str(self.to_dict())
    
    def to_dict(self) -> dict:
        """
        Convertit l'objet Match en un dictionnaire.

        :return: Une représentation sous forme de dictionnaire de l'objet Match.
        :rtype: dict
        """
        return {
            "title": self.title,
            "id": self.id,
            "date": self.date.isoformat(),
            "opponents": self.opponents,
            "slugs": self.slugs,
            "league": self.league,
            "series": self.series,
            "status": self.status,
            "stream": self.stream,
        }
    