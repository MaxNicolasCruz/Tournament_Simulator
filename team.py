class Team:
    def __init__(self, name, media):
        """
        Initialize a Team object with a name, media rating, and cup count

        Parameters:
        name (str): The name of the team
        media (float): The media rating of the team, representing its strength
        """
        self.name = name
        self.media = media
        self.cup = 0
    def __str__(self):
        """
        Return a string representation of the Team object

        Returns:
        str: A string describing the team's name and media rating
        """
        return f'Name: {self.name}, Media: {self.media}'
