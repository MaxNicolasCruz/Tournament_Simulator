import random
class Tournament:
    def __init__(self, teams):
        self.teams = teams

    def show_matches(self, teams):
        #Create dictionary and to get the number of teams for determine the round
        rounds = {32: 'Round of 32',16: 'Round of 16', 8: 'Quarterfinal', 4: 'Semifinal', 2: 'Final'}
        print(f'{rounds.get(len(teams), "Tournament")} Matches:')
        #Generate matches and show them
        for i in range(0, len(teams), 2)    :
            print(f' {teams[i].name} ({round(teams[i].media, 2)}) vs {teams[i+1].name} ({round(teams[i + 1].media, 2)}) ')
            
    def game(self):
        #Store the teams in a variable for avoid change in the original list
        teams = self.teams[:]
        #Show them
        self.show_matches(teams)
        
        res = input('\033[33m \n Continue? (yes/no): \033[0m')
        
        if res.lower() in ('yes', 'y'):
            #the method advance simulate the round and return the winning teams
            winners = self.advance(teams)
            print(f' \n \033[32mLos ganadores son: {[team.name for team in winners]} y pasan a la siguiente ronda.\033[0m \n ')
            #Create a loop for each round
            while len(winners) > 1:
                self.show_matches(winners)
                res = input('\033[33m \n Continue? (yes/no): \033[0m ')
                
                if res.lower() in ('yes', 'y'):
                    winners = self.advance(winners)
                    
                    print(f'\n \033[32mLos ganadores son: {[team.name for team in winners]} y pasan a la siguiente ronda.\033[0m \n')
                elif res.lower() == 'cancel':
                    return
                else:
                    print('For finish tournament: write "cancel" in the console')
            #Add the letter "C" to the champion's name
            team = self.teams.index(winners[0])
            self.teams[team].name = self.teams[team].name + ' C '
            print(f'The champion is {winners[0].name}')
        else:
            print('Tournament cancelled.')
    
    def advance(self, tournament):
        winners = []
        #Iterate through each round the parameter 'tournament'
        for i in range(0, len(tournament), 2):
            team1 = tournament.pop(0)
            team2 = tournament.pop(0)
            #Use the 'play' method to simulate the winners
            winners.append(self.play(team1, team2))
        return winners

    def play(self, team1, team2):
        #The winner is chosen 
        winner = random.choices([team1, team2], weights=[team1.media, team2.media], k=1)[0]
        team = self.teams.index(winner)
        #Increment the media of the teams and return the winner
        self.teams[team].media += 0.7
        if winner == team1:
            team_loser = self.teams.index(team2)
            self.teams[team_loser].media += 0.5
        else:
            team_loser = self.teams.index(team1)
            self.teams[team_loser].media += 0.5
        print(f"{winner.name} won against {team1.name} vs {team2.name}")
        return winner
