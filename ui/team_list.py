import tkinter as tk

class TeamList:
    def __init__(self, parent, bg, team_manager):
        self.parent = parent
        self.bg = bg
        self.team_manager = team_manager
        self.draw_frame_rank = None
        
    def list_rank(self):
        """
        Displays the list of teams in the tournament.
        If a previous rank list frame exists, it will be destroyed and replaced with a new one
        """
        if self.draw_frame_rank is not None:
            self.draw_frame_rank.destroy()
        
        draw_frame_rank = tk.Frame(self.bg, bg='#1f2222')
        draw_frame_rank.configure(relief='sunken', borderwidth=2)
        self.draw_frame_rank = draw_frame_rank
        
        frame = self.bg.create_window(350, 143, window=self.draw_frame_rank, anchor='s')
        
        teams = self.team_manager.show_teams()
        self.show_teams_list(teams, frame)


    def show_teams_list(self, teams, frame):
        """
        Displays a list of teams in a given frame

        Args:
            teams (list or str): List of team names or an error message
            frame (tk.Frame): The frame where the team list will be displayed

        If the list contains 16 teams or fewer, they will be displayed in a single column
        If there are more than 16 teams, the remaining teams will be displayed in a second column
        """
        if isinstance(teams, list):
            for index, team in enumerate(teams, start=1):
                if index <= 16:
                    # Display teams in the first column
                    self.parent.label(self.draw_frame_rank, text=f"{index}_{team}", row=index, column=0, padx=25, pady=2, bg='#1f2222')
                    # Adjust frame position dynamically
                    self.bg.coords(frame, 350, 235 + index * 19)
                elif index > 16:
                    # Display teams in the second column
                    self.parent.label(self.draw_frame_rank, text=f"{index}_{team}", row=index-16, column=1, padx=25, pady=2, bg='#1f2222')
                    # Adjust frame position dynamically
                    self.bg.coords(frame, 450, 535)
        else:
            # Display error message
            self.parent.label(self.draw_frame_rank, teams, row=0, column=0, padx=5,bg='#1f2222')

