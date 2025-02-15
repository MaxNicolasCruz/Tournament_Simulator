from .match import Match

class KnockoutTournament():
    def __init__(self, teams):
        """
        Initialize the Tournament with a list of teams

        Parameters:
        teams (list): A list of Team objects participating in the tournament
        """
        self.teams = teams
        self.match = Match()

    def simulate_round(self, tournament):
        """Simulate matches and return winners"""
        
        winners = []
        for i in range(0, len(tournament), 2):
            team1, team2 = tournament[i], tournament[i + 1]
            winners.append(self.match.play(team1, team2))
        
        return winners
