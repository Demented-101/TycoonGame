import SpacesDictionary as SpaceDict

class space:
    space_index:int = -1 ## position on the board
    name:str = "ERROR - invalid name"
    action:int = -1 ## -1 is no action, reference player script for all action indexes.
    is_property:bool = False
    position:list[int]

    ## PROPERTY ONLY
    owner = None
    group:int ## -1 is Utility, 0 is Station, the rest is each colour suit
    cost:int = 0 ## cost to buy
    benefit:float = 1 ## benefit used for agent decisions
    current_level:int = 0 ## house count
    house_cost:int ## cost to buy house
    unleveled_rent:int ## used when the owner does not have the full set
    rent:list[int] = [] ## index 0 is full set no houses, index 1 is one house etc, so index 5 is hotel
    house_icon = None

    def __init__(self, space:int) -> None:
        self.space_index = space
        space_temp = SpaceDict.spaces[space]
        self.name = space_temp["name"]
        self.action = space_temp["action"]
        self.position = SpaceDict.space_positions[space]
        
        self.is_property = space_temp["is property"]
        if not self.is_property: return

        self.group = space_temp["prices"][0]
        if self.group == -1 or self.group == 0: return ## is Util (-1) or Station (0)
        if self.group > 0:
            self.house_cost = [0, 50, 50, 100, 100, 150, 150, 200, 200][self.group]
        else:
            self.house_cost = -1
        self.cost = space_temp["prices"][1]
        self.unleveled_rent = space_temp["prices"][2]
        self.rent = space_temp["prices"][3:7]
        self.benefit = space_temp["benefit"]

    def get_price(self, roll:int = 0) -> int:
        amount_in_group:int = 0 ## get amount in same set
        for i in self.owner.properties:
            if i.group == self.group and i != self: amount_in_group += 1

        if self.group == -1:
            return roll * [4, 10][amount_in_group]
        
        if self.group == 0: ## station:
            return [25, 50, 100, 200][amount_in_group]

        if (self.group == 1 or self.group == 8) and amount_in_group == 2: ## full 2 peice set
            return self.rent[self.current_level]

        if amount_in_group == 3:
            return self.rent[self.current_level]

        else:
            return self.unleveled_rent
    
    def upgrade(self) -> None:
        if self.current_level >=5: return
        
        self.current_level += 1
        path = ["house_icon1.png", "house_icon2.png", "house_icon3.png", "house_icon4.png", "Mansion.png"][self.current_level]
        full_path = "IMG/" + "House" + "/" + path
        
    
def load_spaces() -> list[space]:
    spaces:list[space] = []
    for i in range(40): 
        spaces.append(space(i))
    return spaces

