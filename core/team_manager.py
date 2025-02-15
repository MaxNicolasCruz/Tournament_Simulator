'''Métodos:

create_team(name, media): Crea un nuevo equipo.
search_team(name): Busca un equipo por nombre.
delete_team(name): Elimina un equipo por nombre.
show_teams(): Muestra la lista de equipos ordenados por puntuación media.
generate_teams(): Genera equipos de prueba (podría estar aquí o en un módulo de pruebas).
'''
from .team import Team

class Team_manager():
    def __init__(self, teams):
        self.teams = teams
        # self.generate_test_teams()
    
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

    # Método para crear equipos con una media de 1 a manera de prueba(test)
    def generate_test_teams(self):
        """
        Generates 32 teams with names of national selections and a media score of 1.
        """
        selection_names = [
            "Brazil", "Argentina", "France", "Germany", "Spain", "Italy", 
            "Portugal", "Netherlands", "England", "Belgium", "Croatia", "Uruguay", 
            "Mexico", "USA", "Japan", "South Korea", "Colombia", "Chile", 
            "Sweden", "Denmark", "Switzerland", "Poland", "Senegal", "Morocco", 
            "Nigeria", "Egypt", "Ivory Coast", "Australia", "Peru", "Ghana", 
            "Serbia", "Turkey"
        ]
        
        for name in selection_names:
            self.create_team(name, 1.0)

