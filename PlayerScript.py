from __future__ import annotations
import Spaces as space
import random as ran

class player:
    player_num:int = 0
    position:int = 0
    money:int = 0
    properties:list
    
    in_jail:bool = False
    jail_turns:int = 0
    GOOJ_cards:list[bool] ## true is opp, false is pot
    
    def roll(self):
        if self.in_jail:
            if self.attempt_jail_leave():
                self.in_jail = False
                self.position = 20 ## i think this is just visiting??
                ## move peice
                ## wait time
            else:
                return

        roll = ran.randint(2,12)
        for i in range(roll):
            self.position = (self.position + 1) % 40
            if self.position == 0: self.money += 200
            ## move peice
            ## wait time (0.1 sec?)
        
        this_space = space.spaces[self.position]
        match this_space.action:
            case -1: pass ## no action
            case 0: self.pull_card_opp()
            case 1: self.pull_card_pot()
            case 2: pass ## TODO - take parking
            case 3: self.pay_parking(200)
            case 4: self.pay_parking(100)
            case 5: pass ## TODO - go to jail
        
        ## TODO - prompt upgrade selection
                
    def attempt_pay(self, amount:int) -> bool:
        if amount > self.money: 
             ## cannot pay, TODO - add property selling and bankrupcy
            return False
        else:
            self.money -= amount
            return True
    
    def pay_parking(self, amount:int) -> None:
        if not self.attempt_pay(amount) : return
        ## add money to parking variable
    
    def pay_player(self, to:player, amount:int) -> None:
        if not self.attempt_pay(amount) : return
        to.money += amount

    def pull_card_opp(self) -> None: pass
    def pull_card_pot(self) -> None: pass
    
    def go_to_jail(self) -> None:
        self.in_jail = True
        self.jail_turns = 0
        ## move peice to jail
    
    def attempt_jail_leave(self) -> bool:
        return False

_player:player = player()
run:bool = True
while run:
    _input:str = input("END: ")
    if _input.upper() == "END": run = False
    else:
        _player.roll()
        print("position: " + str(_player.position))
        print("money: " + str(_player.money))

