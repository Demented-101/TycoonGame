spaces = [
    {"name": "Go",                      "action": -1,   "is property": False},
    {"name": "The Old Creek",           "action": -1,   "is property": True, "prices": [1, 60, 2, 10, 30, 90, 160, 250], "benefit": 0.5},
    {"name": "Pot Luck",                "action": 1,    "is property": False},
    {"name": "Gangsters Paradise",      "action": -1,   "is property": True, "prices": [1, 60, 4, 20, 60, 180, 320, 450], "benefit": 0.5},
    {"name": "Income Tax",              "action": 3,    "is property": False},
    {"name": "Brighton Station",        "action": -1,   "is property": True, "prices": [0, 200], "benefit": 0.9},
    {"name": "The Angels Delight",      "action": -1,   "is property": True, "prices": [2, 100, 6, 30, 90, 270, 400, 550], "benefit": 0.7},
    {"name": "Opportunity Knocks",      "action": 0,    "is property": False},
    {"name": "Potter Avenue",           "action": -1,   "is property": True, "prices": [2, 100, 6, 30, 90, 270, 400, 550], "benefit": 0.7},
    {"name": "Granger Drive",           "action": -1,   "is property": True, "prices": [2, 120, 8, 40, 100, 300, 450, 600], "benefit": 0.7},
    {"name": "Jail - Just Visiting",    "action": -1,   "is property": False},
    {"name": "Skywalker Drive",         "action": -1,   "is property": True, "prices": [3, 140, 10, 50, 150, 450, 625, 750], "benefit": 0.9},
    {"name": "Tesla Power Co",          "action": -1,   "is property": True, "prices": [-1, 150], "benefit": 0.9},
    {"name": "Wookie Hole",             "action": -1,   "is property": True, "prices": [3, 140, 10, 50, 150, 450, 625, 750], "benefit": 0.9},
    {"name": "Rey Lane",                "action": -1,   "is property": True, "prices": [3, 160, 12, 60, 180, 500, 700, 900], "benefit": 0.9},
    {"name": "Hove Station",            "action": -1,   "is property": True, "prices": [0, 200], "benefit": 0.9},
    {"name": "Bishop Drive",            "action": -1,   "is property": True, "prices": [4, 180, 14, 70, 200, 550, 750, 950], "benefit": 0.9},
    {"name": "Pot Luck",                "action": 1,    "is property": False},
    {"name": "Durham Street",           "action": -1,   "is property": True, "prices": [4, 180, 14, 70, 200, 550, 750, 950], "benefit": 0.9},
    {"name": "Broyles Lane",            "action": -1,   "is property": True, "prices": [4, 200, 16, 80, 220, 600, 800, 1000], "benefit": 0.9},
    {"name": "Free Parking",            "action": 2,    "is property": False},
    {"name": "Yue Fei Square",          "action": -1,   "is property": True, "prices": [5, 220, 18, 90, 250, 700, 875, 1050], "benefit": 0.9},
    {"name": "Opportunity Knocks",      "action": 0,    "is property": False},
    {"name": "Mulan Rouge",             "action": -1,   "is property": True, "prices": [5, 220, 18, 90, 250, 700, 875, 1050], "benefit": 0.9},
    {"name": "Han Xin Gardens",         "action": -1,   "is property": True, "prices": [5, 240, 20, 100, 300, 750, 925, 1100], "benefit": 0.9},
    {"name": "Falmer Station",          "action": -1,   "is property": True, "prices": [0, 200], "benefit": 0.9},
    {"name": "Shatner Close",           "action": -1,   "is property": True, "prices": [6, 260, 22, 110, 330, 800, 975, 1150], "benefit": 0.9},
    {"name": "Picard Avenue",           "action": -1,   "is property": True, "prices": [6, 260, 22, 110, 330, 800, 975, 1150], "benefit": 0.9},
    {"name": "Edison Water",            "action": -1,   "is property": True, "prices": [-1, 150], "benefit": 0.9},
    {"name": "Crusher Creek",           "action": -1,   "is property": True, "prices": [6, 280, 22, 120, 360, 850, 1025, 1200], "benefit": 0.9},
    {"name": "Go To Jail",              "action": 5,    "is property": False},
    {"name": "Sirat Mews",              "action": -1,   "is property": True, "prices": [7, 300, 26, 130, 390, 900, 1100, 1275], "benefit": 1},
    {"name": "Ghengis Crescent",        "action": -1,   "is property": True, "prices": [7, 300, 26, 130, 390, 900, 1100, 1275], "benefit": 1},
    {"name": "Pot Luck",                "action": 1,    "is property": False},
    {"name": "Iblis Close",             "action": -1,   "is property": True, "prices": [7, 320, 28, 150, 450, 1000, 1200, 1400], "benefit": 1},
    {"name": "Portslade Station",       "action": -1,   "is property": True, "prices": [0, 200], "benefit": 0.9},
    {"name": "Opportunity Knocks",      "action": 0,    "is property": False},
    {"name": "James Webb Way",          "action": -1,   "is property": True, "prices": [8, 350, 35, 175, 500, 1100, 1300, 1500], "benefit": 1.4},
    {"name": "Super Tax",               "action": 4,    "is property": False},
    {"name": "Turing Heights",          "action": -1,   "is property": True, "prices": [8, 400, 50, 200, 600, 1400, 1700, 2000], "benefit": 1.5},
]
## Name, Action, Is Property, [Group, Cost, rent....], benefit

jail_position:list[int] = [535,940] ## the position "in jail"
space_positions:list[list[int]] = [ ## each position on the board in order
    [1400,960],
    [1290,960],
    [1210,960],
    [1125,960],
    [1040,960],
    [960,960],
    [880,960],
    [795,960],
    [715,960],
    [635,960],
    [480,1000],
    [510,850],
    [510,770],
    [510,690],
    [510,610],
    [510,530],
    [510,450],
    [510,360],
    [510,280],
    [510,200],
    [525,85],
    [635,85],
    [710,85],
    [790,85],
    [880,85],
    [960,85],
    [1040,85],
    [1120,85],
    [1200,85],
    [1285,85],
    [1400,85],
    [1410,200],
    [1410,280],
    [1410,360],
    [1410,450],
    [1410,530],
    [1410,610],
    [1410,690],
    [1410,770],
    [1410,850],
]
space_card_paths:list[str] = [
    "N/a",
    "The Old creek.png", 
    "N/a",
    "Gangsters Paradise.png",
    "N/a",
    "Brighton Station.png",
    "The Angels Delight.png",
    "N/a",
    "Potter Avenue.png",
    "Granger Drive.png",
    "N/a",
    "Skywalker Drive.png",
    "Tesla Power Co",
    "Wookie Hole.png",
    "Rey Lane.png",
    "Hove Station.png",
    "Bishop Drive.png",
    "N/a",
    "Dunham Street.png",
    "Broyles Lane.png",
    "N/a",
    "Yue Fei Square.png",
    "N/a",
    "Mulan Rouge.png",
    "Han Xin Gardens.png",
    "Falmer Station.png",
    "Shatner Close.png",
    "Picard Avenue.png",
    "Edison Water.png",
    "Crusher Creek.png",
    "N/a",
    "Sirat Mews.png",
    "Ghengis Crescent.png",
    "N/a",
    "Ibis Close",
    "Portslade Station.png",
    "N/a",
    "James Webb Way.png",
    "N/a",
    "Turing Heights.png",
    "TOO FAR IN LIST.FUCK YOU" ## used to catch if your trying to load the wrong image
]
