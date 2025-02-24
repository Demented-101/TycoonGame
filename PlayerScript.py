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
    passed_go:bool = False
    money:int = 1500
    properties:list = []
    
    in_jail:bool = False
    jail_turns:int = 0
    GOOJ_cards:list[bool] = [] ## true is opp, false is pot
    
    moving:bool = False
    handling_action:bool = True
    
    main_window = None
    
    def __init__(self, index:int):
        self.player_num = index
    
    def move(self, roll:int, main_window) -> None:
        self.main_window = main_window
        self.moving = True

        self.position = (self.position + 1) % 40
        main_window.move_player_icon(self.player_num, spceDict.space_positions[self.position])
        if self.position == 0: 
            self.passed_go = True
            self.money += 200
        
        
        if roll > 1:
            qtm.singleShot(300, lambda: self.move(roll - 1, main_window))
        else:
            self.moving = False
        ## move peice
       
    def go_to(self, position:int) -> None:
        old_position = self.position
        self.position = position
        self.main_window.move_player_icon(self.player_num, spceDict.space_positions[self.position])
        
        if old_position > self.position: ## has passed go
            self.money += 200
     
    def attempt_pay(self, amount:int) -> int:
        if amount > self.money: 
            self.is_bankrupt = True
            prev_money = self.money
            self.money = 0
            return prev_money
        else:
            self.money -= amount
            return amount
    
    def pay_player(self, to:player, amount:int) -> None:
        to.money += self.attempt_pay(amount)

    def property_purchase(self, space:space.space) -> None:
        print("property purchased")
        self.money -= space.cost
        space.owner = self
        self.properties.append(space)

    def pull_card_opp(self) -> None: pass
    def pull_card_pot(self) -> None: pass    
    
    def go_to_jail(self) -> None:
        self.in_jail = True
        self.jail_turns = 0
        self.position = 10
        self.main_window.move_player_icon(self.player_num, spceDict.jail_position)
    
    def attempt_jail_leave(self, rolled_double:bool) -> bool:
        if self.jail_turns == 3 or rolled_double:
            return True
        
        if False:#disabled until prompt is ready
            return True ## TODO - prompt choice for this
        
        if len(self.GOOJ_cards) > 0:
            card = self.GOOJ_cards.pop()
            ## TODO - add back to respective pack
            return True

        self.jail_turns += 1
        return False
