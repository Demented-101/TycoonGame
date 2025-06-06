import SpacesDictionary as SpaceDict

class space:
    space_index:int = -1 ## position on the board
    name:str = "ERROR - invalid name"
    action:int = -1 ## -1 is no action, reference player script for all action indexes.
    is_property:bool = False

    ## PROPERTY ONLY
    owner = None
    house_cost:int
    group:int
    current_level:int = 0
    cost:int
    unleveled_rent:int
    rent:list[int] = []

    def __init__(self, space:int) -> None:
        self.space_index = space
        space_temp = SpaceDict.spaces[space]
        self.name = space_temp["name"]
        self.action = space_temp["action"]
        
        self.is_property = space_temp["is property"]
        if not self.is_property: return

        self.group = space_temp["prices"][0]
        if self.group == -1 or self.group == 0: return ## is Util (-1) or Station (0)
        self.house_cost = [0, 50, 50, 100, 100, 150, 150, 200, 200]
        self.cost = space_temp["prices"][1]
        self.unleveled_rent = space_temp["prices"][2]
        self.rent = space_temp["prices"][3:7]

    def get_price(self) -> int:
        amount_in_group:int ## get amount in same set
        for i in self.owner.properties:
            if i.group == self.group: amount_in_group += 1

        if self.group == -1:
            return 0 ## TODO
        
        if self.group == 0: ## station:
            return [25, 50, 100, 200][amount_in_group]

        if (self.group == 1 or self.group == 8) and amount_in_group == 2: ## full 2 peice set
            return self.rent[self.current_level]

        if amount_in_group == 3:
            return self.rent[self.current_level]

        else:
            return self.unleveled_rent
    
def load_spaces() -> list[space]:
    for i in range(40): yield space(i)

for i in load_spaces():
    print(i.name)
