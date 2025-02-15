import tkinter as tk

class TeamForms:
    def __init__(self, parent, bg, team_manager, list_rank, clear_frame):
        self.parent = parent
        self.bg = bg
        self.team_manager = team_manager
        self.list_rank = list_rank
        self.clear_frame = clear_frame
        self.draw_frame_form = None
    
    
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

    def form_add_team(self):
        """
        Displays a form to add a new team, with fields for team name and media
        """
        self.frame_for_from(200, 10)
        self.parent.label(self.draw_frame_form, "Enter team name:", 0, 0, 5, 5)
        name = self.entry(self.draw_frame_form, width=20, row=1, column=0, padx=5, pady=5)
        
        self.parent.label(self.draw_frame_form, text="Enter team media:",row=0, column=1, padx=5, pady=5)
        media = self.entry(self.draw_frame_form, width=20, row=1, column=1, padx=5, pady=5)
        
        # Button to submit the form
        btn = tk.Button(self.draw_frame_form, text='Create', bg='gray', font=('Arial', 8),width=10, command=lambda: self.on_create(name, media))
        btn.grid(row=2, column=0, columnspan=2, pady=2)


    def form_search_team(self):
        """
        Displays a form to search for a team by name

        A text entry field is provided for the user to input the team name, and a search button
        that triggers the search and displays the result
        """
        self.frame_for_from(270, 10)
        self.parent.label(self.draw_frame_form, "Enter team name:", 0, 0, 5, 5)
        name = self.entry(self.draw_frame_form, width=20, row=1, column=0, padx=5, pady=5)
        
        # Button to trigger the search
        btn = tk.Button(self.draw_frame_form, text='Search', bg='gray', font=('Arial', 8),width=10, command=lambda: self.show_team_found(name.get()))
        btn.grid(row=2, column=0, columnspan=2, pady=2)

    
    def on_create(self, name, media):
        """
        Handles the creation of a new team by interacting with the tournament manager
        If successful, the form is cleared and the team list is displayed
        
        Args:
            name (tk.Entry): Entry widget containing the team's name
            media (tk.Entry): Entry widget containing the team's media
        """
        result = self.team_manager.create_team(name.get(), media.get())
        if result == True :
            self.clear_frame(self.draw_frame_form)
            self.list_rank()
        else:
            self.parent.label(self.draw_frame_form, text=result['message'],row=3, column=0, columnspan=2, fg='red')

    
    def show_team_found(self, name):
        """
        Searches for a team by name and displays the result.

        Args:
            name (str): The name of the team to search for.

        If the team is found, it displays the team information and provides an option to delete the team.
        """
        found = self.team_manager.search_team(name)
        self.frame_for_from(270, 10)
        
        if isinstance(found, str):
            # Display the result or error message
            self.parent.label(self.draw_frame_form, found, 0, 0, 5, 5, fontsize=13)
        else:
            # Display team information
            self.parent.label(self.draw_frame_form, str(found), 0, 0, 5, 5, fontsize=13)
            # Button to delete the team
            delete_button = tk.Button(
                self.draw_frame_form,
                text='Delete',
                bg='gray',
                font=('Arial', 8),
                width=10,
                command=lambda: [
                    self.team_manager.delete_team(name),
                    self.list_rank(),
                    self.clear_frame(self.draw_frame_form)
                ]
            )
            delete_button.grid(row=2, column=0, columnspan=2, pady=2)



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




    def show_error_message(self, message):
        rect_id, text_id = self.parent.create_cell(0, 0, 350, 70, message)
        self.bg.move(rect_id, 45, 500)
        self.bg.move(text_id, 45, 500)
        self.parent.after(5000, lambda: (self.bg.delete(rect_id), self.bg.delete(text_id)))

