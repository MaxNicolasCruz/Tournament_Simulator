from tournament_manager import Tournament_manager

def main():
    manager = Tournament_manager()
    
    while True:
        res = input('''
1_Create Team
2_Show Teams
3_Show Single Team
4_Delete Team
5_Generate Tournament
6_Exit
\n
''')
        if res == '1':
            name = input('Give the name for new team: ')
            media = input('Give the media for new team: ')
            manager.create_team(name, media)
        elif res == '2':
            manager.show_teams()
        elif res == '3':
            name = input('Give the name of the team for info: ')
            print(manager.search_team(name))
        elif res == '4':
            name = input('Give the name of the team for delete: ')
            print(manager.delete_team(name))
        elif res == '5':
            manager.start_tournament()
        elif res == '6':
            print('Exiting the game.')
            break
        else:
            print('Choose a valid option.')

if __name__ == '__main__':
    main()
