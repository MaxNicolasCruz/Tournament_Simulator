import tkinter as tk
from tkinter import ttk
import random
from tournament_manager import Tournament_manager

class App_view(tk.Tk):
    """
    Main application window for the Tournament Simulator
    Handles the UI elements and interactions for managing the tournament
    """
    def __init__(self):
        """Initialize the application window, background effect, and the slide menu"""
        super().__init__()
        self.tournament_manager = Tournament_manager()
        self.bg = None
        self.draw_frame_form = None
        self.draw_frame_rank = None
        self.team_data = []
        self.config_window()
        self.bg_efect(15)
        self.slide_menu()
    
    
    def config_window(self):
        '''Configures the main window's title, size, and background color'''
        self.title('Tournament Simulator')
        self.geometry('1000x650+200+5')
        self.maxsize(1000,650)
        self.configure(background="black")


    def create_point(self, x, y, size):
        """
        Creates a point on the canvas and initiates its shrinking process
        
        Args:
            x (int): The x-coordinate for the point
            y (int): The y-coordinate for the point
            size (int): The initial size of the point
        """
        point = self.bg.create_oval(x, y, x + size, y + size,fill='white', outline='white')
        self.shrink_point(point, x, y, size)


    def shrink_point(self, point, x, y, size):
        """
        Recursively shrinks a point on the canvas until it disappears
        
        Args:
            point (int): The canvas object ID of the point
            x (int): The x-coordinate of the point
            y (int): The y-coordinate of the point
            size (int): The current size of the point
        """
        if size > 0:
            size -= 1
            self.bg.coords(point, x, y, x + size, y + size)
            self.after(50,self.shrink_point,point,x,y,size)
        else:
            self.bg.delete(point)        


    def bg_efect(self,count):
        """
        
        Creates a background effect by randomly generating points on the canvas
        
        Args:
            count (int): The number of points to generate
        """

        # Initialize canvas if not already done 
        if self.bg is None:
            bg = tk.Canvas(self, bg='black', width=1000, height=650)
            bg.pack()
            self.bg = bg
            
        # Get window dimensions
        w_width = self.winfo_width()
        w_height = self.winfo_height()
        
        # Generate points if window dimensions are valid
        if w_width > 1 and w_height > 1:
            for i in range(count):
                x = random.randint(0, w_width)
                y = random.randint(0, w_height)
                size = random.randint(4, 9)
                self.create_point(x, y, size)
        
        # Schedule the next effect
        self.after(random.randint(100, 300), self.bg_efect, count)


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
        btn = ttk.Button(self, text=text, command=command, style='TButton', width=12)
        self.bg.create_window(x, y, window=btn)
        return btn

    def slide_menu(self):
        """
        Creates the main menu buttons on the left side of the window
        """
        self.buttons(100,150,'Add Team',self.form_add_team)
        self.buttons(100,200,'Show Teams', self.list_rank)
        self.buttons(100,250,'Search Team', self.form_search_team)
        self.buttons(100,300,'Generate Tournament', self.tournament)
        self.buttons(100,350,'Exit', self.exits)

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


    def entry(self, frame, width, row, column, padx, pady):
        """
        Creates an entry widget and places it within a grid in the given frame
        
        Args:
            frame (tk.Frame): The frame to place the entry in
            width (int): The width of the entry
            row (int): The row in the grid where the entry should appear
            column (int): The column in the grid where the entry should appear
            padx (int): Horizontal padding around the entry
            pady (int): Vertical padding around the entry
        
        Returns:
            tk.Entry: The created entry widget
        """
        entry = tk.Entry(frame, width=width)
        entry.grid(row=row, column=column, padx=padx, pady=pady)
        return entry


    def clear_frame(self, frame):
        """
        Clears all widgets from the specified frame
        
        Args:
            frame (tk.Frame): The frame to clear
        """
        for widget in frame.winfo_children():
            widget.destroy()


    def frame_for_from(self, x, y):
        """
        Creates a new frame at the specified position on the canvas
        If a previous frame exists, it will be destroyed
        
        Args:
            x (int): The x-coordinate for the frame
            y (int): The y-coordinate for the frame
        """
        if self.draw_frame_form is not None:
            self.draw_frame_form.destroy()

        frame = tk.Frame(self.bg, bg='black')
        self.draw_frame_form = frame
        self.bg.create_window(x, y, window=self.draw_frame_form, anchor='nw')


    def on_create(self, name, media):
        """
        Handles the creation of a new team by interacting with the tournament manager
        If successful, the form is cleared and the team list is displayed
        
        Args:
            name (tk.Entry): Entry widget containing the team's name
            media (tk.Entry): Entry widget containing the team's media
        """
        result = self.tournament_manager.create_team(name.get(), media.get())
        if result == True :
            self.clear_frame(self.draw_frame_form)
            self.list_rank()
        else:
            self.label(self.draw_frame_form, text=result['message'],row=3, column=0, columnspan=2, fg='red')


    def form_add_team(self):
        """
        Displays a form to add a new team, with fields for team name and media
        """
        self.frame_for_from(200, 10)
        self.label(self.draw_frame_form, "Enter team name:", 0, 0, 5, 5)
        name = self.entry(self.draw_frame_form, width=20, row=1, column=0, padx=5, pady=5)
        
        self.label(self.draw_frame_form, text="Enter team media:",row=0, column=1, padx=5, pady=5)
        media = self.entry(self.draw_frame_form, width=20, row=1, column=1, padx=5, pady=5)
        
        # Button to submit the form
        btn = tk.Button(self.draw_frame_form, text='Create', bg='gray', font=('Arial', 8),width=10, command=lambda: self.on_create(name, media))
        btn.grid(row=2, column=0, columnspan=2, pady=2)


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
        
        teams = self.tournament_manager.show_teams()
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
                    self.label(self.draw_frame_rank, text=f"{index}_{team}", row=index, column=0, padx=25, pady=2, bg='#1f2222')
                    # Adjust frame position dynamically
                    self.bg.coords(frame, 350, 235 + index * 19)
                elif index > 16:
                    # Display teams in the second column
                    self.label(self.draw_frame_rank, text=f"{index}_{team}", row=index-16, column=1, padx=25, pady=2, bg='#1f2222')
                    # Adjust frame position dynamically
                    self.bg.coords(frame, 450, 535)
        else:
            # Display error message
            self.label(self.draw_frame_rank, teams, row=0, column=0, padx=5,bg='#1f2222')


    def form_search_team(self):
        """
        Displays a form to search for a team by name

        A text entry field is provided for the user to input the team name, and a search button
        that triggers the search and displays the result
        """
        self.frame_for_from(270, 10)
        self.label(self.draw_frame_form, "Enter team name:", 0, 0, 5, 5)
        name = self.entry(self.draw_frame_form, width=20, row=1, column=0, padx=5, pady=5)
        
        # Button to trigger the search
        btn = tk.Button(self.draw_frame_form, text='Search', bg='gray', font=('Arial', 8),width=10, command=lambda: self.show_team_found(name.get()))
        btn.grid(row=2, column=0, columnspan=2, pady=2)


    def show_team_found(self, name):
        """
        Searches for a team by name and displays the result.

        Args:
            name (str): The name of the team to search for.

        If the team is found, it displays the team information and provides an option to delete the team.
        """
        found = self.tournament_manager.search_team(name)
        self.frame_for_from(270, 10)
        
        if isinstance(found, str):
            # Display the result or error message
            self.label(self.draw_frame_form, found, 0, 0, 5, 5, fontsize=13)
        else:
            # Display team information
            self.label(self.draw_frame_form, str(found), 0, 0, 5, 5, fontsize=13)
            # Button to delete the team
            delete_button = tk.Button(
                self.draw_frame_form,
                text='Delete',
                bg='gray',
                font=('Arial', 8),
                width=10,
                command=lambda: [
                    self.tournament_manager.delete_team(name),
                    self.list_rank(),
                    self.clear_frame(self.draw_frame_form)
                ]
            )
            delete_button.grid(row=2, column=0, columnspan=2, pady=2)


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


    def show_error_message(self, message):
        rect_id, text_id = self.create_cell(0, 0, 350, 70, message)
        self.bg.move(rect_id, 45, 500)
        self.bg.move(text_id, 45, 500)
        self.after(5000, lambda: (self.bg.delete(rect_id), self.bg.delete(text_id)))


    def initialize_tournament(self):
        if len(self.team_data) < 1 or isinstance(self.team_data, str):
            self.team_data = self.tournament_manager.start_tournament()
            if isinstance(self.team_data, str):
                self.show_error_message(self.team_data)
                return False
            else:
                self.clear_bg()
        return True


    def configure_round_settings(self):
        rect_width = 110
        rect_height = 45
        margin_x, margin_y, spacing = 0, 0, 85
        fill, outline = '#25adc8', '#606061'
        
        round_names = {32: 'Round of 32', 16: 'Round of 16', 8: 'Quarterfinal', 4: 'Semifinal', 2: 'Final'}
        current_round = round_names.get(len(self.team_data))
        
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
        round_rect_id, round_text_id = self.create_cell(0, 0, rect_width + 45, rect_height + 25, current_round)
        self.bg.move(round_rect_id, 430, 50)
        self.bg.move(round_text_id, 430, 50)
        # If only one team remains, display the champion
        if len(self.team_data) == 1:
            self.bg.itemconfig(round_text_id, text=f'Champions: {self.team_data[0].name}', fill='black')
            self.bg.itemconfig(round_rect_id, fill='#7f8c8d')
            self.team_data = []
            return True # Indicate that a champion has been found
        return False


    def create_team_cells(self, teams_left, teams_right, rect_width, rect_height, fill, outline, margin_x, margin_y, spacing):
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
        btn_tournament = self.buttons(500, 600, 'Simulate', lambda: self.simulate())
        if len(self.team_data) == 1:
            btn_tournament.config(text='To Menu', command=lambda: self.return_to_menu())


    def tournament(self):
        """
        Initiates or continues the tournament and displays the tournament bracket.
        """
        if not self.initialize_tournament():
            return
        
        rect_width, rect_height, margin_x, margin_y, spacing, fill, outline, current_round = self.configure_round_settings()
        if self.show_round(rect_width, rect_height, current_round):
            # If there is a champion, change the button to return to the menu
            self.buttons(500, 600, 'To Menu', lambda: self.return_to_menu())
            return

        # If it is the final, display the teams in the center position
        if len(self.team_data) == 2:
            text = f'{self.team_data[0].name} \n     vs    \n {self.team_data[1].name}'
            rect_id, text_id = self.create_cell(0, 0, rect_width + 20, rect_height + 20, text, fill, outline)
            self.bg.move(rect_id, margin_x, margin_y)
            self.bg.move(text_id, margin_x, margin_y)
        
        self.show_simulation_button()
        self.create_team_cells(
            self.team_data[:len(self.team_data)//2],
            self.team_data[len(self.team_data)//2:],
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
        winners = self.tournament_manager.advance(self.team_data)
        self.team_data = winners
        self.tournament()


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

app = App_view()



app.mainloop()