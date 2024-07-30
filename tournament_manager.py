import random
from team import Team
from tournament import Tournament

class Tournament_manager:
    def __init__(self):
        self.teams = []

    def create_team(self, name, media):
        #We validate that the name is valid and available
        if len(name) < 2 or not all(char.isalpha() or char.isspace() for char in name):
            print(f'Sorry, {name} is too short or contains invalid characters. Please select another name.')
            return None
        try:
            media = float(media)
        except ValueError:
            print(f'{media} is not a valid number for media.')
            return None
        for team in self.teams:
            if team.name.lower() == name.lower():
                print(f'The name {name} already exists.')
                return None
        #Create object of class Team and add to list
        new_team = Team(name, media)
        self.teams.append(new_team)
        return new_team

    def search_team(self, name):
        #Traverse the list of teams, searching for that name 
        for team in self.teams:
            if team.name.lower() == name.lower():
                return team
        return 'There is no team with that name.'

    def delete_team(self, name):
        for team in self.teams:
            if team.name.lower() == name.lower():
                #Delete team to found
                self.teams.remove(team)
                return 'team delete'
        return 'There is no team with that name.'

    def show_teams(self):
        if not self.teams:
            print('There are no teams.')
        else:
            #Traverse the list of teams and sort it by their average
            team_order = sorted(self.teams, key=lambda team: team.media, reverse=True)
            for i,team in enumerate(team_order):
                print(f'{i + 1}_{team.name}: {round(team.media, 2)} ')
    def start_tournament(self):
        #Validate that there are enough teams in the list to start the tournament 
        if len(self.teams) not in (4, 8, 16, 32):
            print('You can only create the tournament with 4, 8, or 16 teams.')
            return
        #Reorganize the list random
        random.shuffle(self.teams)
        #Create an object of class Tournament and causes it to start 
        tournament = Tournament(self.teams)
        tournament.game()
