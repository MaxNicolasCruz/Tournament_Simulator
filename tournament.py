import random
class Tournament:
    def __init__(self, teams):
        """
        Initialize the Tournament with a list of teams

        Parameters:
        teams (list): A list of Team objects participating in the tournament
        """
        self.teams = teams

    def show_matches(self, teams):
        """
        Return the list of teams participating in the matches

        Parameters:
        teams (list): A list of Team objects

        Returns:
        list: The same list of Team objects passed as input
        """
        data = []
        for team in teams:
            data.append(team)
        return data
    def game(self):
        """
        Simulate the matches by shuffling and returning the list of teams

        Returns:
        list: A shuffled list of Team objects representing the matches
        """
        #Store the teams in a variable for avoid change in the original list
        teams = self.teams[:]
        #Show them
        
        teams = self.show_matches(teams)
        
        return teams
    
    def advance(self, tournament):
        """
        Simulate the advancement of teams through the tournament rounds

        Parameters:
        tournament (list): A list of Team objects representing the current round

        Returns:
        list: A list of Team objects representing the winners of the round
        """
        winners = []
        
        # Iterate over pairs of teams in the tournament list
        for i in range(0, len(tournament), 2):
            team1, team2 = tournament[i], tournament[i + 1]
            # Use the 'play' method to simulate the winner of the match
            winners.append(self.play(team1, team2))
            
        # If there's only one winner left, update their cup count
        if len(winners) == 1:
            team = self.teams[self.teams.index(winners[0])]
            team.cup += 1
        return winners
    
    def play(self, team1, team2):
        """
        Simulate a match between two teams and determine the winner

        Parameters:
        team1 (Team): The first team
        team2 (Team): The second team

        Returns:
        Team: The winning team based on their media ratings
        """
        # Select the winner based on media ratings
        winner = random.choices([team1, team2], weights=[team1.media, team2.media], k=1)[0]

        # Find the correct instance of the winning team in self.teams
        team = self.teams[self.teams.index(winner)]
        
        # Increment the media of the winner and loser, then return the winner
        team.media += 0.7
        loser = team1 if winner == team2 else team2
        loser.media += 0.5
        
        return winner
