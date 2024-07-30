class Team:
    def __init__(self, name, media):
        self.name = name
        self.media = media
    
    def __str__(self):
        return f'Name: {self.name}, Media: {self.media}'
