import random

class Match():
    def __init__(self):
        pass
    
    
    def play(self, team1, team2):
        """
        Simulate a match between two teams.

        Parameters:
        team1 (Team): The first team.
        team2 (Team): The second team.

        Returns:
        Team: The winning team.
        """
        winner = self.determine_winner(team1, team2)
        loser = team1 if winner == team2 else team2
        
        return winner, loser

    
    def determine_winner(self, team1, team2):
        """
        Determine the winner between two teams based on their media ratings.

        Parameters:
        team1 (Team): The first team.
        team2 (Team): The second team.

        Returns:
        Team: The winning team.
        """
        return random.choices([team1, team2], weights=[team1.media, team2.media], k=1)[0]
