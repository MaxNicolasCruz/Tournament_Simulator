import tkinter as tk
from core.tournament_manager import Tournament_manager
from core.team_manager import Team_manager
from core.knockout_Tournament import KnockoutTournament
from ui.background_effect import BackgroundEffect
from ui.menu import Menu
from ui.team_forms import TeamForms
from ui.team_list import TeamList

class App_view(tk.Tk):
    """
    Main application window for the Tournament Simulator
    Handles the UI elements and interactions for managing the tournament
    """
    def __init__(self):
        """Initialize the application window, background effect, and the slide menu"""
        super().__init__()
        self.team_data = []
        self.tournament_manager = Tournament_manager(self.team_data)
        self.team_manager = Team_manager(self.team_data)
        self.tournament = None
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface components."""
        self.config_window()
        self.bg_effect = BackgroundEffect(self)
        self.bg_effect.start_effect(15)
        self.bg = self.bg_effect.bg
        self.team_list = TeamList(self, self.bg, self.team_manager)
        self.team_forms = TeamForms(self, self.bg, self.team_manager, self.team_list.list_rank, self.clear_frame)
        self.menu = Menu(self, self.bg, self.team_forms.form_add_team, self.team_list.list_rank, self.team_forms.form_search_team, self.tournament_ui, self.load_game, self.quit)
        self.menu.slide_menu()
        
    def config_window(self):
        '''Configures the main window's title, size, and background color'''
        self.title('Tournament Simulator')
        self.geometry('1000x650+200+5')
        self.maxsize(1000,650)
        self.configure(background="black")

    def clear_frame(self, frame):
        """
        Clears all widgets from the specified frame
        
        Args:
            frame (tk.Frame): The frame to clear
        """
        for widget in frame.winfo_children():
            widget.destroy()


    def label(self, frame, text, row, column, padx=0, pady=0, columnspan =1, fg='white', bg='black', fontsize=9):
        """
        Creates a label and places it within a grid in the given frame
        
        Args:
            frame (tk.Frame): The frame to place the label in
            text (str): The text to display in the label
            row (int): The row in the grid where the label should appear
            column (int): The column in the grid where the label should appear
            padx (int, optional): Horizontal padding around the label. Default is 0
            pady (int, optional): Vertical padding around the label. Default is 0
            columnspan (int, optional): Number of columns the label should span. Default is 1
            fg (str, optional): Text color. Default is 'white'
            bg (str, optional): Background color. Default is 'black'
            fontsize (int, optional): Font size. Default is 9
        
        Returns:
            tk.Label: The created label
        """
        label = tk.Label(frame, text=text, fg=fg, bg=bg, font=('Arial', fontsize))
        label.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan)
        return label


    def clear_bg(self):

        """
        Clears all widgets from the background canvas except the canvas itself.
        """
        # Clear all widgets from the main window except the canvas
        for child in self.winfo_children():
            if not isinstance(child, tk.Canvas):
                child.destroy()
        # Clear all widgets from the background canvas
        for child in self.bg.winfo_children():
            child.destroy()

    def initialize_tournament(self):
        """
        Initialize the tournament if it is not already initialized.

        Returns:
            bool: True if the tournament was initialized successfully, False otherwise.
        """
        # Check if team_data is empty or tournament is not initialized
        if len(self.team_data) < 1 or not isinstance(self.tournament, KnockoutTournament):
            
            self.tournament = self.tournament_manager.start_tournament(self.team_data)

            # Check if start_tournament returned an error message
            if isinstance(self.tournament, str):
                self.team_forms.show_error_message(self.tournament)
                return False
            else:
                self.clear_bg()

        return True



    def configure_round_settings(self):
        """
        Configure the settings for the current round.

        Returns:
            tuple: Settings for the current round, including dimensions, margins, spacing, and colors.
        """
        rect_width = 110
        rect_height = 45
        margin_x, margin_y, spacing = 0, 0, 85
        fill, outline = '#25adc8', '#606061'
        
        round_names = {32: 'Round of 32', 16: 'Round of 16', 8: 'Quarterfinal', 4: 'Semifinal', 2: 'Final'}
        current_round = round_names.get(len(self.tournament_manager.get_initial_teams()))
        
        if current_round == 'Round of 32':
            margin_x += 10
            margin_y += 5
        elif current_round == 'Round of 16':
            margin_x += 130
            margin_y += 60
            spacing += 80
            fill = '#219cb5'
        elif current_round == 'Quarterfinal':
            margin_x += 245
            margin_y += 135
            spacing += 255
            fill = '#1b7f93'
        elif current_round == 'Semifinal':
            margin_x += 340
            margin_y += 235
            spacing += 255
            fill = '#156170'
        elif current_round == 'Final':
            margin_x += 450
            margin_y += 350
            spacing += 285
            fill = '#0e434e'
        
        return rect_width, rect_height, margin_x, margin_y, spacing, fill, outline, current_round


    def show_round(self, rect_width, rect_height, current_round):
        """
        Display the current round on the UI.

        Args:
            rect_width (int): Width of the rectangle.
            rect_height (int): Height of the rectangle.
            current_round (str): Name of the current round.

        Returns:
            bool: True if a champion is found, False otherwise.
        """
        round_rect_id, round_text_id = self.create_cell(0, 0, rect_width + 45, rect_height + 25, current_round)
        self.bg.move(round_rect_id, 430, 50)
        self.bg.move(round_text_id, 430, 50)
        # If only one team remains, display the champion
        if len(self.tournament_manager.get_initial_teams()) == 1:
            self.bg.itemconfig(round_text_id, text=f'Champions: {self.tournament_manager.get_initial_teams()[0].name}', fill='black')
            self.bg.itemconfig(round_rect_id, fill='#7f8c8d')
            self.tournament = None
            return True # Indicate that a champion has been found
        return False


    def create_team_cells(self, teams_left, teams_right, rect_width, rect_height, fill, outline, margin_x, margin_y, spacing):
        """
        Create and position the team cells on the UI.

        Args:
            teams_left (list): List of teams on the left side.
            teams_right (list): List of teams on the right side.
            rect_width (int): Width of the rectangle.
            rect_height (int): Height of the rectangle.
            fill (str): Fill color of the rectangle.
            outline (str): Outline color of the rectangle.
            margin_x (int): X margin for positioning.
            margin_y (int): Y margin for positioning.
            spacing (int): Spacing between cells.
        """
        for i in range(0, len(teams_left) - 1, 2):
            text = f'{teams_left[i].name} \n     vs    \n {teams_left[i + 1].name}'
            rect_id, text_id = self.create_cell(0, 0, rect_width, rect_height, text, fill, outline)
            self.bg.move(rect_id, margin_x, margin_y + (i // 2) * spacing)
            self.bg.move(text_id, margin_x, margin_y + (i // 2) * spacing)
        
        for i in range(0, len(teams_right) - 1, 2):
            text = f'{teams_right[i].name} \n     vs     \n {teams_right[i + 1].name}'
            rect_id, text_id = self.create_cell(0, 0, rect_width, rect_height, text, fill, outline)
            self.bg.move(rect_id, 890 - margin_x, margin_y + (i // 2) * spacing)
            self.bg.move(text_id, 890 - margin_x, margin_y + (i // 2) * spacing)


    def show_simulation_button(self):
        """Show the simulation button on the UI."""
        btn_tournament = self.menu.buttons(500, 600, 'Simulate', lambda: self.simulate())
        if len(self.team_data) == 1:
            btn_tournament.config(text='To Menu', command=lambda: self.return_to_menu())


    def tournament_ui(self):
        """
        Initiates or continues the tournament and displays the tournament bracket.
        """
        if not self.initialize_tournament():
            return
        rect_width, rect_height, margin_x, margin_y, spacing, fill, outline, current_round = self.configure_round_settings()
        if self.show_round(rect_width, rect_height, current_round):
            # If there is a champion, change the button to return to the menu
            self.menu.buttons(500, 600, 'To Menu', lambda: self.menu.return_to_menu())
            return
        # If it is the final, display the teams in the center position
        if len(self.tournament_manager.get_initial_teams()) == 2:
            text = f'{self.tournament_manager.get_initial_teams()[0].name} \n     vs    \n {self.tournament_manager.get_initial_teams()[1].name}'
            rect_id, text_id = self.create_cell(0, 0, rect_width + 20, rect_height + 20, text, fill, outline)
            self.bg.move(rect_id, margin_x, margin_y)
            self.bg.move(text_id, margin_x, margin_y)
        
        self.show_simulation_button()
        self.create_team_cells(
            self.tournament_manager.get_initial_teams()[:len(self.tournament_manager.get_initial_teams())//2],
            self.tournament_manager.get_initial_teams()[len(self.tournament_manager.get_initial_teams())//2:],
            rect_width, rect_height, fill, outline, margin_x, margin_y, spacing
        )



    def create_cell(self, x1, y1, x2, y2, text, fill="#303030", outline='white', text_color='white'):
        """
        Creates a rectangular cell on the canvas with centered text

        Args:
            x1, y1 (int): Top-left corner coordinates
            x2, y2 (int): Width and height of the rectangle
            text (str): Text to display inside the rectangle
            fill (str): Fill color of the rectangle
            outline (str): Outline color of the rectangle
            text_color (str): Color of the text

        Returns:
            tuple: IDs of the created rectangle and text
        """
        # Create a rectangle
        rect_id = self.bg.create_rectangle(x1, y1, x1 + x2, y1 + y2, fill=fill, outline=outline, width=2)
        
        # Calculate the center of the rectangle
        cx = x1 + x2 / 2
        cy = y1 + y2 / 2
        
        # Create the text at the center of the rectangle
        text_id = self.bg.create_text(cx, cy, text=text, fill=text_color, font=('arial', 8, 'bold'))
        return rect_id, text_id


    def simulate(self):
        """
        Advances the tournament by simulating the matches and updating the display.
        """
        winners = self.tournament_manager.advance_round(self.tournament)

        self.tournament_ui()



app = App_view()



app.mainloop()