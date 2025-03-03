#
# University of Sussex - Software Engineering Coursework
#
# Callum Hemsley - Backend Development
# Carys Flack - Frontend Development
# Conor Lagden - Testing and Documentation
# Henry Davies - Frontend Development
# Louis Henry - Testing and Risk Analysis
# James Bardell - 
#


#importing necessary libraries to use UI (PyQt5)

import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QMainWindow, QWidget)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer as qtm

#Importing other libraries to use throughout the program

import PlayerScript as plyr
import Spaces as spce
import OppKnock
import PotLuck

#Importing other libraries to use throughout the program

import random as ran
import sys
import time

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Declaration of variables that require global scope (e.g. variables that may need to be used across multiple windows.)

running:bool = False
current_turn:int = 0
selectedPlayerNo = False
noOfPlayers:int = -1
free_parking_pot:int = 0

potluck_cards:list
opp_knock_cards:list

previous_roll:int = 0
previous_roll_was_double:bool = False
double_count:int = 0

players:list[plyr.player] = []
spaces:list[spce.space] = []
main_window:qtw.QMainWindow

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#declaration of functions that require global scope (may be used across multiple windows)

def get_image_path(name:str, folder:str) -> str:
    ## name is the name of the image itself INCLUDING the .png or .jpg at the end
    ## folder is the name of the folder the image is in, like PItems or Potluck
    ## so to get an image from PNumberMenu, call "get_image_path("3players.png", "PNumberMenu")"
    ## :D
    full_path:str = "IMG/" + folder + "/" + name
    return full_path

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#main gameplay loop + other

def start(player_count:int) -> None:
    print("START METHOD RUN")
    global players, spaces, current_turn, potluck_cards, opp_knock_cards
    
    current_turn = 0
    
    for i in range(player_count): 
        players.append(plyr.player(i))
        print(i)
    
    spaces = spce.load_spaces() ## load spaces and cards
    opp_knock_cards = OppKnock.cards.copy()
    ran.shuffle(opp_knock_cards)
    potluck_cards = PotLuck.cards.copy()
    ran.shuffle(potluck_cards.append)

    qtm.singleShot(1000, loop) # wait until game loop starts

loop_state:int = 0
prev_loop_state:int = -1
def loop() -> None:
    global loop_state, prev_loop_state, current_turn
    global players, spaces, main_window
    global previous_roll, previous_roll_was_double, double_count
    
    new_state:bool = loop_state != prev_loop_state
    prev_loop_state = loop_state
    current_player = players[current_turn]
    
    if loop_state == 0 and new_state: ## roll dice (state 0)
        if current_player.is_bankrupt: ## skip go
            loop_state = -1
        else:
            print("dice roll started")  
            main_window.promptDiceRoll(current_turn + 1)
            current_player.handling_action = True
    
    if loop_state == 1: ## roll finished - move player (state 1)
        current_player = players[current_turn]
        
        if new_state: ## dice roll just finished 
            allow_move:bool = True
            
            if current_player.in_jail: ## in jail
                escaped = current_player.attempt_jail_leave(previous_roll_was_double)
                if escaped:
                    current_player.in_jail = False
                    current_player.position = 10
                    allow_move = True
                else:
                    loop_state = -1
                    allow_move = False
            
            if previous_roll_was_double and double_count == 1:
                current_player.go_to_jail()
                loop_state = -1
                allow_move = False
                previous_roll_was_double = False
                
            if allow_move: 
                print("dice roll finished - moving player") 
                current_player.move(previous_roll, main_window)
        
        if not current_player.moving: ## finished moving
            print("player finished moving")
            space = spaces[current_player.position]
            player_movement_finished(current_player, space)
            loop_state = 2
    
    if loop_state == 2:
        if not current_player.handling_action:
            if previous_roll_was_double:
                loop_state = 0 ## player reroll
                double_count += 1
                print(double_count)
            else:
                loop_state = -1
                double_count = 0
        
    elif loop_state == -1: ## turn finished
        found_player:bool = False
        while not found_player:
            current_turn = (current_turn + 1) % noOfPlayers
            found_player = not players[current_turn].is_bankrupt 
        loop_state = 0
    
    qtm.singleShot(500, loop)

def player_movement_finished(player:plyr.player, space:spce.space) -> None:
    print("current properties:" + str(player.properties))
    if space.is_property:
        if space.owner:
            player.pay_player(space.owner, space.get_price()) # pay owner if owned
            player.handling_action = False
            
        elif player.money >= space.cost:
            buy_prompt = PropertyWindow(player, space) # open property prompt to buy
            buy_prompt.show()
    
    else: ## is not property
        global free_parking_pot
        match space.action:
            case -1: pass ## no action
            
            case 0: player.pull_card_opp()
            case 1: player.pull_card_pot()
            
            case 2: ## take FP
                player.money += free_parking_pot
                free_parking_pot = 0
            case 3: ## pay 200 fine to FP
                free_parking_pot += player.attempt_pay(200)
            case 4: ## pay 100 fine to FP
                free_parking_pot += player.attempt_pay(100)
            
            case 5:  ## go to jail
                player.go_to_jail()

        player.handling_action = False

def pull_potluck_card(player:plyr.player) -> None:
    global potluck_cards
    picked_card = potluck_cards.pop(0) ## take first card
    potluck_cards.append(picked_card) ## add to the back of the deck
    
    action = picked_card[1]
    operand = picked_card[2]
    
    match action:
        case 0: ## get money
            player.money += operand
        case 1: ## go to location
            player.go_to(operand)
        case 2: ## pay bank
            player.attempt_pay(operand)
        case 3: ## pay free parking
            global free_parking_pot
            free_parking_pot += player.attempt_pay(operand)
        case 4: ## go to jail
            player.go_to_jail()
        case 5: ## all players pay player
            global players
            targets = players.copy()
            targets.remove(player) ## get list of every player but the one receiving the money
            for i in targets:
                player.money += i.attempt_pay(operand) ## loop list - each pay
        case 6:
            player.GOOJ_cards.append(False)
            potluck_cards.remove(len(potluck_cards) - 1) ## remove the card from the deck
        case 7:
            if False: ## pay 10 ## TODO - add pay prompt.
                pull_opp_knock_card(player)
            else:
                player.attempt_pay(operand)

def pull_opp_knock_card(player:plyr.player) -> None:
    global opp_knock_cards
    picked_card = opp_knock_cards.pop(0)
    opp_knock_cards.append(picked_card)
    
    action = picked_card[1]
    operand = picked_card[2]
    
    match action:
        case 0: ## get money
            player.money += operand
        case 1: ## go to location
            player.go_to(operand)
        case 2: ## pay bank
            player.attempt_pay(operand)
        case 3: ## pay free parking
            global free_parking_pot
            free_parking_pot += player.attempt_pay(operand)
        case 4:
            fine:int = 0
            for i in player.properties:
                if i.current_level == 0: pass
                elif i.current_level == 5: fine += [115, 100][operand]
                else: fine += i.current_level * [40, 25][operand]
            player.attempt_pay(fine)
        case 5:
            new_position = player.position - operand
            player.go_to(new_position)
        case 6:
            player.go_to_jail()
        case 7:
            player.GOOJ_cards.append(True)
            opp_knock_cards.remove(len(opp_knock_cards) - 1) ## remove the card from the deck
            
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class MainWindow (qtw.QMainWindow): #Class for the main window of the game.
    
    player_icons:list = []
    
    def __init__(self):
        global main_window
        main_window = self
        
        super().__init__()
        self.setWindowTitle("Property Tycoon") #Title of Window
        self.resize(1920,1080) #Adjusting size of background to fit the 1920x1080 scale
        self.setStyleSheet("background-image: url(" + get_image_path("newbackground.png", "Board") + "); background-repeat: no-repeat; background-position: center;")
        #Background images

        self.closebutton = qtw.QPushButton("", self) #code to set up close button properties
        self.closebutton.setIcon(qtg.QIcon(get_image_path("close-button-png-30225(1).png", "Exit")))
        self.closebutton.setIconSize(qtc.QSize(40, 40)) 
        self.closebutton.setGeometry(1860,10,50,50)
        self.closebutton.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.closebutton.setToolTip("Close Game")
        self.closebutton.clicked.connect(self.closebuttonpressed) #call to function when close button is pressed

        #MoneyBoard
        self.moneyBoard = QLabel(self)
        self.moneyBoard.setPixmap(QPixmap(get_image_path("moneyBoardbackground.png", "MoneyBoard"))) #Money board
        self.moneyBoard.setGeometry(5,5,435,480)
        self.moneyBoard.setScaledContents(True)


        self.moneyContainer = QWidget(self.moneyBoard)
        self.moneyContainer.setGeometry(10,60,445,400)
        self.moneyContainer.setStyleSheet("background: transparent;")
        

        self.moneylayout = QVBoxLayout(self.moneyContainer)
        self.moneylayout.setContentsMargins(0,0,0,0)
        self.moneylayout.setSpacing(1)

        #creates an array of playerMoneydisplays
        playerCountMoney= ["BootM.png", "SmartphoneM.png", "CatM.png", "HatstandM.png", "MoneyP5.png", "MoneyBoard"]

        #Display Player Money on board
        global noOfPlayers
        for i in range(noOfPlayers):
            money_label = QLabel(self.moneyContainer)
            pixmap = QPixmap(get_image_path(playerCountMoney[i], "MoneyBoard"))
            money_label.setPixmap(pixmap)
            money_label.setScaledContents(True)
            money_label.setFixedSize(90,95)
            self.moneylayout.addWidget(money_label)

        
    
        for i in range(noOfPlayers):
            self.create_player_icon("Boot.png")

  
        self.helpbutton = qtw.QPushButton("", self) # code to set up help button properties
        self.helpbutton.setIcon(qtg.QIcon(get_image_path("helpbutton.png", "Help")))
        self.helpbutton.setIconSize(qtc.QSize(60, 60)) 
        self.helpbutton.setGeometry(1805,10,50,50)
        self.helpbutton.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.helpbutton.setToolTip("Help")
        self.helpbutton.clicked.connect(self.helpbuttonpressed) #call to function if help button is pressed
        
        #TEST BUTTON TO IMPLEMENT DICE ROLL

        if False: ## turn this to true to reimplement the button :D
            self.diceRollTest = qtw.QPushButton("", self)
            self.diceRollTest.setIcon(qtg.QIcon(get_image_path("rollbutton.png", "Dice")))
            self.diceRollTest.setIconSize(qtc.QSize(300, 100)) 
            self.diceRollTest.setGeometry(40,10,300,100)
            self.diceRollTest.setStyleSheet("QPushButton { background: transparent; border: none; }")
            self.diceRollTest.setToolTip("roll")
            self.diceRollTest.clicked.connect(self.diceRollPressed)
        
        self.showFullScreen() #display main window

    def create_player_icon(self, image:str):
        new_icon = qtw.QLabel(self)
        new_icon.setPixmap(qtg.QPixmap(get_image_path(image, "PItems")))
        new_icon.setScaledContents(True)
        new_icon.setStyleSheet("background: transparent; border: none; ")
        new_icon.setGeometry(1350,910,120,120)
        self.player_icons.append(new_icon)
    
    def closebuttonpressed(self): #close main window
        running = False
        qtw.QApplication.instance().quit() #closes application

    def helpbuttonpressed(self):
        self.help_window_open = HelpWindow() #opens up the help window
        self.help_window_open.show()
        
    def diceRollPressed(self):
        self.dice_roll_open = diceRoll("Dice Roll")
        self.dice_roll_open.show()
    
    def promptDiceRoll(self, player:int):
        self.dice_roll_open = diceRoll("Player " + str(player) + "'s turn!")
        self.dice_roll_open.show()
  
    def move_player_icon(self, player, position):
        icon = self.player_icons[player]
        icon.setGeometry(position[0] - 50, position[1] - 50, 100, 100)
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	

class HelpWindow (qtw.QMainWindow): 
    
    '''I experienced trouble with this window. Use of a scroll area made the usual CSS stylesheet formatting impossible 
    as a CSS-implemented background image cannot be scrolled in this python library. The background of this window was done using a Pixmap instead
    which, although was more difficult, allowed me to implement dynamic resizing which is important as this window isnt fullscreen,
    therefore subject to users changing the size of the window.''' 
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help Page")
        self.resize(600, 900)
        container = QWidget()
        helplayout = QVBoxLayout(container)
        self.background_label = QLabel()
        self.background_label.setAlignment(Qt.AlignTop) #align label to the top of the window

        self.original_pixmap = QPixmap(get_image_path("HelpPageBackground.png", "Help")) #loading background image as a pixmap


        self.update_pixmap_size()  # Initial scaling
        
        help_close_button = QPushButton("") #code to set up properties of close button for help window
        help_close_button.clicked.connect(self.close)
        help_close_button.setIcon(qtg.QIcon(get_image_path("close-button-png-30225(1).png", "Exit")))
        help_close_button.setStyleSheet("QPushButton { background: transparent; border: none; }")
        help_close_button.setIconSize(qtc.QSize(30, 30))
        help_close_button.setToolTip("Close Window")

    
        helplayout.addWidget(self.background_label) #in this block of code we add our labels/buttons to our QVBoxLayout 
        helplayout.addWidget(help_close_button, alignment=Qt.AlignCenter)

    
        scroll_area = QScrollArea(self) #scroll bar
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)

        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #horizontal scrolling not needed as image is fit to size
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(scroll_area)
        
    def resizeEvent(self, event):
        #this method resizes image dynamically when window is resized by user
        self.update_pixmap_size()
        super().resizeEvent(event)

    def update_pixmap_size(self):
        #This method ensures that the image size always fits the width of the window whilst conforming to the original aspect ratio
        if not self.original_pixmap.isNull():
            window_width = self.width()  
            scaled_pixmap = self.original_pixmap.scaledToWidth(
                window_width, Qt.SmoothTransformation
            )
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setFixedHeight(scaled_pixmap.height())
            
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class StartWindow(qtw.QMainWindow): #code for the start window in which the number of players is decided.
    
    '''
    
    NOTES FOR CONOR:
    
    initial issue with the button layout - the 'setGeometry' function i messed up the entry of the parameters, but it initially went unnocticed
    as the size of each looked the same due to their same sized background image and transparency, but the 5 player button overlapped the 4 player button
    which overlapped the 3 player button etc. so every button you pressed would select the 5 player option. this was later discovered in testing and
    quickly amended
    
    (this is callum now): before, each button would run a seperate method, since each button would need to set the amount of players differently.
    after researching this issue, lambda could be use to pass an argument into a function, meaning all 5 methods can be reduced to a single method
    far more cleanly.
    
    '''
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pick Number of Players")
        self.resize(500, 650)
        self.setStyleSheet("background-image: url('" + get_image_path("startscreen.png", "PNumberMenu") + "'); background-repeat: no-repeat; background-position: center;")

        self.players1 = qtw.QPushButton("", self)
        self.players1.setIcon(qtg.QIcon(get_image_path("1players.png", "PNumberMenu")))
        self.players1.setIconSize(qtc.QSize(300, 200))
        self.players1.setGeometry(100, 150, 300, 90)  
        self.players1.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players1.clicked.connect(lambda: self.load_players(1))

        self.players2 = qtw.QPushButton("", self)
        self.players2.setIcon(qtg.QIcon(get_image_path("2players.png", "PNumberMenu")))
        self.players2.setIconSize(qtc.QSize(300, 200))
        self.players2.setGeometry(100, 240, 300, 90)  
        self.players2.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players2.clicked.connect(lambda: self.load_players(2))

        self.players3 = qtw.QPushButton("", self)
        self.players3.setIcon(qtg.QIcon(get_image_path("3players.png", "PNumberMenu")))
        self.players3.setIconSize(qtc.QSize(300, 200))
        self.players3.setGeometry(100, 330, 300, 90)  
        self.players3.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players3.clicked.connect(lambda: self.load_players(3))

        self.players4 = qtw.QPushButton("", self)
        self.players4.setIcon(qtg.QIcon(get_image_path("4players.png", "PNumberMenu")))
        self.players4.setIconSize(qtc.QSize(300, 200))
        self.players4.setGeometry(100, 420, 300, 90)  
        self.players4.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players4.clicked.connect(lambda: self.load_players(4))

        self.players5 = qtw.QPushButton("", self)
        self.players5.setIcon(qtg.QIcon(get_image_path("5players.png", "PNumberMenu")))
        self.players5.setIconSize(qtc.QSize(300, 200))
        self.players5.setGeometry(100, 510, 300, 90)  
        self.players5.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players5.clicked.connect(lambda: self.load_players(5))

        self.show()  # Show the window

    def load_players(self, count:int):
        global selectedPlayerNo, noOfPlayers
        selectedPlayerNo = True
        noOfPlayers = count
        self.openWindow1 = MainWindow()
        self.close()
        
        start(count)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     
class diceRoll(qtw.QMainWindow):
    
    dice_images:list = []
    result_images:dict = {}
    
    '''
    NOTES FOR CONOR
    
    TEST IDEAS:
    
    - ensure that every possible dice roll corresponds with the number displayed above.
    - ensure that button sizes are acceptable. Backgrounds are transparent, so overlap may occur without notice
    - ensure that every element defined in the CSS is applied to the widgets/buttons etc.
    - ensure that if both dice rolls are the same, button remains activated
    - ensure that if a player rolls a double twice, the method that sends to jail is activated
    - JUST MAKE SURE IT ALL WORKS
    - etc, etc
    
    '''
    
    def __init__(self, title:str):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(617,360)
        self.setStyleSheet("background-image: url('"+ get_image_path("bluebackground.jpg", "Dice") +"'); background-repeat: no-repeat;")
        self.setWindowFlags(qtc.Qt.WindowStaysOnTopHint)
        
        ## load images for dice and totals - saves loading this millions of times over later
        for i in range(1,7):self.dice_images.append(QPixmap(get_image_path("dice-" + str(i) + ".png", "Dice")))
        for i in range(2,13): self.result_images[i] = (QPixmap(get_image_path("Total-" + str(i) + ".png", "Dice")))
        
        self.diceRollButton = QPushButton("", self) #setting up properties of dice roll button 
        self.diceRollButton.setGeometry(158, 200, 300, 200)
        self.diceRollButton.clicked.connect(self.rollAnimation)
        self.diceRollButton.setToolTip("Roll")
        self.diceRollButton.setIcon(qtg.QIcon(get_image_path("rollbutton.png", "Dice")))
        self.diceRollButton.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.diceRollButton.setIconSize(qtc.QSize(300, 200))
        
        #DEFINITIONS OF DICE ICONS
        
        self.dice1 = qtw.QLabel(self)
        self.dice1.setGeometry (180,100,100,100)
        self.dice1.setScaledContents(True)
        self.dice1.setStyleSheet("background: transparent; border: none;")
        
        self.dice2 = qtw.QLabel(self) 
        self.dice2.setGeometry (337,100,100,100)
        self.dice2.setScaledContents(True)
        self.dice2.setStyleSheet("background: transparent; border: none;")
        
        self.announcementLabel = qtw.QLabel(self) #this label will output result of dice roll
        self.announcementLabel.setGeometry(210,30, 200, 50)
        self.announcementLabel.setScaledContents(True)
        self.announcementLabel.setStyleSheet("background: transparent; border: none;")
        
        self.DoubleRollLabel = qtw.QLabel(self) #this label will output result of dice roll
        self.DoubleRollLabel.setGeometry(-15,15, 230, 110)
        self.DoubleRollLabel.setStyleSheet("background: transparent; border: none;")
        self.DoubleRollLabel.setScaledContents(True)
        
        self.goToJailLabel = qtw.QLabel(self) #this label will output result of dice roll
        self.goToJailLabel.setGeometry(350,200, 250, 100)
        self.goToJailLabel.setStyleSheet("background: transparent; border: none;")
        self.goToJailLabel.setScaledContents(True)
        
        global double_count
        self.set_double(double_count)
        
        self.conor = qtw.QLabel(self) #ignore this...
        self.conor.setGeometry(50,0,200,400)
        self.conor.setStyleSheet("background: transparent; border: none;")
        self.conor.setScaledContents(True)
        
        self.noOfRolls = 0
        self.animationCounter = 0
        
        self.show()
    
    def set_double(self, count:int) -> None:
            if count == 0: ## no changes needed
                return
            elif count == 1: ## single double roll
                self.DoubleRollLabel.setStyleSheet("background-image: url('"+ get_image_path("DoubleRoll.png", "Dice") + "'); background-repeat: no-repeat; background-position: center;")
            else: ## second double roll - next go to jail
                self.goToJailLabel.setStyleSheet("background-image: url('"+ get_image_path("JailDoubleRoll.png", "Dice") +"'); background-repeat: no-repeat; background-position: center;")
    
    def rollAnimation(self):
        self.announcementLabel.setPixmap(qtg.QPixmap()) 
        self.DoubleRollLabel.setStyleSheet("background: transparent; border: none;")
        self.goToJailLabel.setStyleSheet("background: transparent; border: none;")
        
        self.diceRollButton.setDisabled(True) #immediately disable button so that it cannot be pressed again whilst the animation is still running.
        if self.animationCounter < 10: #repeat roll 10 times as part of the animation
            randomface1 = ran.randint(0,5)
            self.dice1.setPixmap(self.dice_images[randomface1])

            randomface2 = ran.randint(0,5)
            self.dice2.setPixmap(self.dice_images[randomface2])
            
            self.animationCounter += 1
            qtm.singleShot(150, self.rollAnimation)  #wait 150ms, then reset then go again after incrementing the counter.
        else:
            self.diceRollMethod()
    
    def diceRollMethod(self):
        global previous_roll, previous_roll_was_double, loop_state
        self.animationCounter = 0 #reset the animation counter so that it can run again if a double is rolled.
        self.diceRollButton.setDisabled(True) #disable button
        
        diceRoll1 = ran.randint(1,6) #conor, when testing for double rolls, you can change these values both to the same integer to force a double roll x
        diceRoll2 = ran.randint(1,6)
        total = diceRoll1 + diceRoll2
        previous_roll = total
        
        print("Dice 1: " + str(diceRoll1))
        print("Dice 2: " + str(diceRoll2))
        print("roll: " + str(total))
        
        if diceRoll1 == 4 and diceRoll2 == 3: #ignore this 
            self.conor.setStyleSheet("background-image: url("+ get_image_path("Snapchat-675243558.jpg", "Other") +"); background-repeat: no-repeat; background-position: center;")
            qtm.singleShot(500, self.resetConor)
        
        previous_roll_was_double = diceRoll1 == diceRoll2 ## save double roll

        #CHANGING THE DICE ICONS BASED ON WHICH NUMBERS HAVE BEEN RANDOMLY SELECTED: (but BETTER!)

        self.dice1.setPixmap(self.dice_images[diceRoll1 - 1])
        self.dice2.setPixmap(self.dice_images[diceRoll2 - 1])
        
        #CHANGING THE OUTPUT OF OUR ANNOUNCEMENT LABEL BASED OFF OF WHAT OUR TOTAL IS:
        self.announcementLabel.setPixmap(self.result_images[total])
        qtm.singleShot(1000, self.end_roll)

    def end_roll(self) -> None:
        global loop_state
        self.hide()
        loop_state = 1
             
    def resetConor(self):
        self.conor.setStyleSheet("background: transparent; border: none;")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class PropertyWindow(qtw.QMainWindow):
    player:plyr.player
    space:spce.space
    
    def __init__(self, player:plyr.player, space):
        super().__init__()
        self.player = player
        self.space = space
        
        self.setWindowTitle("Buy Properties?")
        self.resize(926,652)
        self.setStyleSheet("background-image: url('"+ get_image_path("PropertyBackground", "Property_Buy") +"'); background-repeat: repeat;")
        
        self.propertyYes = qtw.QPushButton("",self)
        self.propertyYes.setIcon(qtg.QIcon(get_image_path("Yes.png", "Property_Buy")))
        self.propertyYes.setIconSize(qtc.QSize(180,350)) 
        self.propertyYes.setGeometry(100,150,300,90)
        self.propertyYes.setStyleSheet("QPushButton {background: transparent; border: none;}")
        self.propertyYes.pressed.connect(lambda : self.button_pressed(True))

        self.propertyNo = qtw.QPushButton("",self)
        self.propertyNo.setIcon(qtg.QIcon(get_image_path("No.png", "Property_Buy")))
        self.propertyNo.setIconSize(qtc.QSize(180,350)) 
        self.propertyNo.setGeometry(300,150,700,90)
        self.propertyNo.setStyleSheet("QPushButton {background: transparent; border: none;}")
        self.propertyNo.pressed.connect(lambda : self.button_pressed(False))
        
        self.show()
        
    def button_pressed(self, accept:bool):
        if accept:
            self.player.property_purchase(self.space)
        self.player.handling_action = False
        self.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

app = qtw.QApplication([])
mw = PropertyWindow()
'''CONOR. WHEN TESTING, CHANGE THE VALUE OF 'mw' TO THE NAME OF THE UI CLASS YOU WANT TO TEST. THIS WILL MAKE IT DISPLAY. love you'''

app.exec_()