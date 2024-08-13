import random
from team import Team
from tournament import Tournament

class Tournament_manager(Tournament):
    """
    Manages the creation, searching, deletion, and management of teams,
    as well as the initiation of the tournament
    """
    def __init__(self):
        """
        Initializes the Tournament_manager with an empty list of teams
        """
        self.teams = []

    def create_team(self, name, media):
        """
        Creates a new team and adds it to the list of teams if the name is valid and available

        Args:
            name (str): The name of the team
            media (float): The media score of the team

        Returns:
            True if the team is successfully created
            dict: Contains an error message if the team cannot be created
        """
        error = {'message': ''}
        
        #We validate that the name is valid and available
        if len(name) < 2 or not all(char.isalpha() or char.isspace() for char in name):
            error['message'] = f'Sorry, {name} is too short or contains invalid characters.'
            return error
        #Validate media
        try:
            media = float(media)
        except ValueError:
            error['message']=f'{media} is not a valid number for media.'
            return error
        
        # Check for duplicate team name
        if any(team.name.lower() == name.lower() for team in self.teams):
            error['message'] = f'The name {name} already exists.'
            return error
        
        # Check for team limit
        if len(self.teams) == 32:
            error['message'] = f'limit reached'
            return error
        
        #Create object of class Team and add to list
        new_team = Team(name, media)
        self.teams.append(new_team)
        return True

    def search_team(self, name):
        """
        Searches for a team by name in the list of teams

        Args:
            name (str): The name of the team to search for

        Returns:
            Team: The team object if found
            str: A message indicating that the team was not found
        """
        #Traverse the list of teams, searching for that name 
        team = next((team for team in self.teams if team.name.lower() == name.lower()), None)
        return team if team else 'There is no team with that name'

    def delete_team(self, name):
        """
        Deletes a team by name from the list of teams

        Args:
            name (str): The name of the team to delete

        Returns:
            str: A message indicating whether the team was successfully deleted or not found
        """
        team = next((team for team in self.teams if team.name.lower() == name.lower()), None)
        if team:
            self.teams.remove(team)
            return 'Team deleted.'
        return 'There is no team with that name.'

    def show_teams(self):
        """
        Displays the list of teams, sorted by their average score in descending order

        Returns:
            list: A list of strings representing the team names and their averages
            str: A message indicating that there are no teams if the list is empty
        """
        
        if not self.teams:
            return 'There are no teams'
        
        team_order = sorted(self.teams, key=lambda team: team.media, reverse=True)
        return [f'{team.name}: {round(team.media, 2)} ({team.cup})' for team in team_order]

    def start_tournament(self):
        """
        Starts the tournament if the number of teams is valid

        Returns:
            list: A list of games to be played in the tournament
            str: A message indicating that the tournament cannot be started due to an invalid number of teams
        """
        #Validate that there are enough teams in the list to start the tournament 
        if len(self.teams) not in (4, 8, 16, 32):
            return 'You can only create the tournament with 4, 8, 16 or 32 teams.'
        #Reorganize the list random
        random.shuffle(self.teams)
        #Create an object of class Tournament and causes it to start 
        tournament = Tournament(self.teams)
        return tournament.game()

