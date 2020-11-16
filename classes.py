#Б02-010 Артаева Рожков Садыков

class Platform():
    def __init__(self):
        self.x0 = 400
        self.y0 = 570
        self.width = 60
        self.height = 15
        rectangle(screen, (0,0,0), self.x0-self.width/2, self.y0-self.height/2, self.width, self.height,)
        self.lives = 3
        
    def move_right(self, event):
        if event.keysym == 'Right' and self.x0 <= 695:
            self.x0 += 25
            canvas.move(self.id, 25, 0)
            canvas.move(self.id_body, 25, 0)

    def move_left(self, event):
        if event.keysym == 'Left' and self.x0 >= 5:
            self.x0 -= 25
            canvas.move(self.id, -25, 0)
            canvas.move(self.id_body, -25, 0)
            
class Balls():
    def __init__(self):
        pass
        
class Targets():
    def __init__(self):
        pass
        
class Bonuses():
    def __init__(self):
        pass
            
