from __future__ import annotations
import Spaces as space
import SpacesDictionary as spceDict
import random as ran
import time
from PyQt5.QtCore import QTimer as qtm

## PROMPTS NEEDED:
    # purchase property
    # leave Jail (50 payment)
    # upgrade property prompt

class player:
    player_num:int = 0
    is_bankrupt:bool = False
    position:int = 0
    money:int = 1500
    properties:list = []
    
    in_jail:bool = False
    jail_turns:int = 0
    GOOJ_cards:list[bool] ## true is opp, false is pot
    
    moving:bool = False
    handling_action:bool = True
    
    main_window = None
    
    def __init__(self, index:int):
        self.player_num = index
    
    def move(self, roll:int, main_window) -> None:
        self.main_window = main_window
        print("move: " + str(roll) + " player index: " + str(self.player_num))
        self.moving = True
        
        if self.in_jail and False: ## TODO - reimplement jail
            if self.attempt_jail_leave():
                self.in_jail = False
                self.position = 10 ## i think this is just visiting??
                ## move peice
                time.sleep(0.1)
            else:
                return ## return so that the rest of the turn is nullified

        self.position = (self.position + 1) % 40
        if self.position == 0: self.money += 200
        main_window.move_player_icon(self.player_num, spceDict.space_positions[self.position])
        
        if roll > 1:
            qtm.singleShot(300, lambda: self.move(roll - 1, main_window))
        else:
            self.moving = False
        ## move peice
    
    def finish_movement(self, space):
        self.handling_action = True
        match space.action:
            case -1: pass ## no action
            case 0: self.pull_card_opp()
            case 1: self.pull_card_pot()
            case 2: pass ## TODO - take parking
            case 3: self.pay_parking(200)
            case 4: self.pay_parking(100)
            case 5: self.go_to_jail()
        self.handling_action = False
        
    def attempt_pay(self, amount:int) -> int:
        if amount > self.money: 
            self.is_bankrupt = True
            prev_money = self.money
            self.money = 0
            return prev_money
        else:
            self.money -= amount
            return amount
    
    def pay_parking(self, amount:int) -> None:
        to_pay_middle = self.attempt_pay(amount) ## TODO - add to free parking total
    
    def pay_player(self, to:player, amount:int) -> None:
        to.money += self.attempt_pay(amount)

    def pull_card_opp(self) -> None: pass
    def pull_card_pot(self) -> None: pass    
    
    def go_to_jail(self) -> None:
        self.in_jail = True
        self.jail_turns = 0
        self.main_window.move_player_icon(self.player_num, spceDict.jail_position)
    
    def attempt_jail_leave(self) -> bool:
        if self.jail_turns == 3:
            return True
        
        if self.attempt_pay(50):
            return True ## TODO - prompt choice for this
        
        if len(self.GOOJ_cards) > 0:
            card = self.GOOJ_cards.pop()
            return True

        self.jail_turns += 1
