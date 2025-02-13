import random as ran
import Spaces as spaces

class player:
    position:int = 0
    money:int = 0
    properties:list
    
    def roll(self):
        ## handle jail

        roll = ran.randint(2,12)
        for i in range(roll):
            self.position = (self.position + 1) % 40
            if self.position == 0: self.money += 200
            ## move peice, wait time
        


_player:player = player()
run:bool = True
while run:
    _input:str = input("END: ")
    if _input.upper() == "END": run = False
    else:
        _player.roll()
        print("position: " + str(_player.position))
        print("money: " + str(_player.money))

