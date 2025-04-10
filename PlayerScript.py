from __future__ import annotations
import Spaces as space
import SpacesDictionary as spceDict
import random as ran
import time
from PyQt5.QtCore import QTimer as qtm

class player:
    player_num:int = 0
    is_agent:bool = False
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
    
    def __init__(self, index:int, mainwindow):
        self.player_num = index
        self.main_window = mainwindow
    
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
            self.main_window.add_text_log("PLAYER " + str(self.player_num + 1) + " IS BANKRUPT!")
            return prev_money
        else:
            self.money -= amount
            return amount
    
    def pay_player(self, to:player, amount:int) -> None:
        to.money += self.attempt_pay(amount)
        self.main_window.add_text_log("player " + str(self.player_num + 1) + " payed player " + str(to.player_num + 1) + " £" + str(amount))

    def property_purchase(self, space:space.space) -> None:
        self.main_window.add_text_log("player " + str(self.player_num + 1) + " purchased property " + space.name)
        self.money -= space.cost
        space.owner = self
        self.properties.append(space)
    
    def go_to_jail(self) -> None:
        self.in_jail = True
        self.jail_turns = 0
        self.position = 10
        self.main_window.move_player_icon(self.player_num, spceDict.jail_position)
        self.main_window.add_text_log("player " + str(self.player_num + 1) + " went to jail")
    
    def get_full_sets(self, colour_only:bool = True) -> list[int]:
        checked_sets:list[int] = []
        found_sets:list[int] = []
        
        if colour_only: checked_sets = [0, -1] ## remove stations and utils from search
        
        for prop in self.properties:
            if prop.group in self.properties: continue ## skip checked sets
            
            checked_sets.append(prop.group)
            found_in_set:int = 0
            
            for other in self.properties:
                if other.group == prop.group: found_in_set += 1 ## find others in set
            
            if (prop.group == 1 or prop.group == 8 or prop.group == -1) and found_in_set == 2:
                found_sets.append(prop.group)
            elif prop.group == 0 and found_in_set == 4:
                found_sets.append(prop.group)
            elif found_in_set == 3:
                found_sets.append(prop.group)
        
        return found_sets
        
    
    ## AGENTS -----------------------------------------------------------------------
    
    decision_chance:int = -1 ## chance that they will take a monetary decision
    poor_decision_chance:int = -1 ## chance they will take a monetaty decision while under the "poor threshold"
    poor_threshold:float = 0.5 ## when under this threshold percentage wise compared to the cost of the purchase
    absolute_no_dist:int = 10 ## how far the price must be from the amount of money the player has to always say no
    group_preference:float = 1.2 ## how much the benefit is multiplied per existing property in the same group
    jail_benefit:float = 1 ## benefit used when deciding to pay to leave jail.
    house_chance:float = 0.1 ## chance to buy a house
    is_henry:bool = False ## will always go all in
    
    def setup_agent(self) -> None:
        self.is_agent = True
        self.decision_chance = ran.randint(45, 85)
        self.poor_decision_chance = self.decision_chance - ran.randint(10, 40)
        self.poor_threshold = ran.random() + 1.5
        if self.poor_threshold > 2.3:
            self.absolute_no_dist = ran.randint(30, 100)
        else:
            self.absolute_no_dist = ran.randint(0, 30)
        self.group_preference = 1.2 + (ran.random() * 0.5)
        self.jail_benefit = ran.random() + 0.5
        self.house_chance = 0.05 + (ran.random() / 5)
        self.is_henry = ran.randint(0, 99) == 50
        
    def decide_property_benefit(self, space:space.space) -> float:
        benefit:float = space.benefit
        for i in self.properties:
            if i.group == space.group:
                benefit *= self.group_preference
            else:
                benefit -= ran.random() * 0.05
        
        print("agent " + str(self.player_num) + " decided proptery benefit - " + str(benefit))
        return benefit
    
    def agent_decision(self, benefit:float, cost:int) -> bool:
        if cost >= self.money - self.absolute_no_dist:
            print("agent " + str(self.player_num) + " decided flat out no")
            return False
        
        if self.is_henry:
            self.main_window.add_text_log("ALL IN!!")
            return True
        
        true_decision_chance = self.decision_chance
        if cost * self.poor_threshold > self.money:
            true_decision_chance = self.poor_decision_chance
            print("agent decision chance reduced - poor decision chance used")
        
        true_decision_chance *= benefit
        random_num = ran.randint(0,100)
        print("agent " + str(self.player_num) + " decided " + str(true_decision_chance > random_num) + ". chance - " + str(true_decision_chance))
        return true_decision_chance > random_num
        
    def agent_house_decision(self, available_sets:list[int]) -> None:
        chosen_set = ran.choice()
        
        example_property:space.space = None
        while example_property == None:
            pick = ran.choose(self.properties)
            if pick.group == chosen_set: example_property = pick
        
        if self.agent_decision(example_property.benefit, example_property.house_cost):
            money -= example_property.house_cost
            example_property.current_level += 1
        
            if ran.random() < self.house_chance: ## buy another
                self.agent_house_decision(available_sets)
        
        
