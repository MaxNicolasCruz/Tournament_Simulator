import random
from core.knockout_Tournament import KnockoutTournament

class Tournament_manager():
    """
    Manages the creation, searching, deletion, and management of teams,
    as well as the initiation of the tournament
    """
    def __init__(self, teams):
        """
        Initializes the Tournament_manager with an empty list of teams
        """
        self.teams = teams

    
    def get_initial_teams(self):
        """
        Return a copy of the teams list to avoid modifying the original.

        Returns:
        list: A copy of the list of Team objects.
        """
        return self.teams[:]
    
    def start_tournament(self, teams):
        self.teams = teams
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
        tournament = KnockoutTournament(self.teams)
        
        return tournament


    def advance_round(self, tournament):
        """Advances the round and awards the trophy if needed."""
        matches = tournament.simulate_round(self.teams)
        winners = []
        # Flatten the list of winners before processing

        for teams in matches:
            winner, loser = teams
            winners.append(winner)
            self.update_team_stats(winner, loser)
            
        if len(winners) == 1:
            self.award_trophy(winners[0])

        self.teams = winners
        return winners


    def update_team_stats(self, winner, loser):
        """
        Update the media ratings of the winner and loser.

        Parameters:
        winner (Team): The team that won the match.
        loser (Team): The team that lost the match.
        """
        # Update media ratings
        winner.update_media(0.7)
        loser.update_media(0.5)
        
    
    def award_trophy(self, winner):
        """
        Update the cup count of the final winning team.

        Parameters:
        winner (Team): The final winning team.
        """
        winner.cup += 1