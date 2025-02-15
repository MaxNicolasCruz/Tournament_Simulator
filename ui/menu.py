import tkinter as tk
from tkinter import ttk

class Menu:
    def __init__(self, parent, bg, form_add_team, list_rank, form_search_team, tournament_ui, load_game, quit):
        self.parent = parent
        self.bg = bg
        self.form_add_team = form_add_team
        self.list_rank = list_rank
        self.form_search_team = form_search_team
        self.tournament_ui = tournament_ui
        self.load_game = load_game
        self.quit = quit
    
    def buttons(self, x, y, text, command):  
        """
        Creates a styled button on the canvas at a specified location
        
        Args:
            x (int): The x-coordinate for the button
            y (int): The y-coordinate for the button
            text (str): The label text on the button
            command (function): The function to call when the button is clicked
        
        Returns:
            ttk.Button: The created button
        """
        # Configure the button style    
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TButton', font=('Arial', 12, 'bold'))
        style.map('TButton',background=[('active', '#25adc8'), ('!disabled', '#1ad0f4')],
                            foreground=[('active','#fdfefe'),('!disabled','black')],
                            relief=[('pressed','groove'),('!pressed', 'ridge')]
                            )
        
        # Create and place the button
        btn = ttk.Button(self.parent, text=text, command=command, style='TButton', width=12)
        self.bg.create_window(x, y, window=btn)
        return btn

    

    def slide_menu(self):
        """
        Creates the main menu buttons on the left side of the window
        """
        self.buttons(100,150,'Add Team',self.form_add_team)
        self.buttons(100,200,'Show Teams', self.list_rank)
        self.buttons(100,250,'Search Team', self.form_search_team)
        self.buttons(100,300,'Generate Tournament', self.tournament_ui)
        self.buttons(100,350,'Load Game', self.load_game)
        self.buttons(100,400,'Exit', self.exits)

    
    def return_to_menu(self):
        """
        Clears the canvas and returns to the main menu.
        """
        self.bg.delete("all")
        self.slide_menu()


    def exits(self):
        """
        Exits the application.
        """
        self.quit()