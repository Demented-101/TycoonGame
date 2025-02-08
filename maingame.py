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

import random
import sys
import time

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Declaration of variables that require global scope (e.g. variables that may need to be used across multiple windows.)

selectedPlayerNo = False
noOfPlayers = 0

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#declaration of functions that require global scope (may be used across multiple windows)

def get_image_path(name:str) -> str: ## just pass in the name of the image (including the .png or .jpg) and it will give u the path u need <3
    #callum you're the best 
    full_path:str = "IMG/" + name
    return full_path

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class MainWindow (qtw.QMainWindow): #Class for the main window of the game.
    def __init__(self):
        
        super().__init__()
        self.setWindowTitle("Property Tycoon") #Title of Window
        self.resize(1920,1080) #Adjusting size of background to fit the 1920x1080 scale
        self.setStyleSheet("background-image: url(" + get_image_path("newbackground.png") + "); background-repeat: no-repeat; background-position: center;")
        #Background images

        self.closebutton = qtw.QPushButton("", self) #code to set up close button properties
        self.closebutton.setIcon(qtg.QIcon(get_image_path("close-button-png-30225(1).png")))
        self.closebutton.setIconSize(qtc.QSize(40, 40)) 
        self.closebutton.setGeometry(1860,10,50,50)
        self.closebutton.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.closebutton.setToolTip("Close Game")
        self.closebutton.clicked.connect(self.closebuttonpressed) #call to function when close button is pressed
        
        self.bootIcon = qtw.QLabel(self)
        bootpixmap = qtg.QPixmap(get_image_path("Bootresized1.png"))
        self.bootIcon.setPixmap(bootpixmap)
        self.bootIcon.setScaledContents(True)
        self.bootIcon.setGeometry(1400,960,100,100)
        print(get_image_path("Bootresizede1.png"))
  
        self.helpbutton = qtw.QPushButton("", self) # code to set up help button properties
        self.helpbutton.setIcon(qtg.QIcon(get_image_path("helpbutton.png")))
        self.helpbutton.setIconSize(qtc.QSize(60, 60)) 
        self.helpbutton.setGeometry(1805,10,50,50)
        self.helpbutton.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.helpbutton.setToolTip("Help")
        self.helpbutton.clicked.connect(self.helpbuttonpressed) #call to function if help button is pressed
        
        #TEST BUTTON TO IMPLEMENT DICE ROLL

        self.diceRollTest = qtw.QPushButton("", self)
        self.diceRollTest.setIcon(qtg.QIcon(get_image_path("rollbutton.png")))
        self.diceRollTest.setIconSize(qtc.QSize(300, 100)) 
        self.diceRollTest.setGeometry(40,10,300,100)
        self.diceRollTest.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.diceRollTest.setToolTip("roll")
        self.diceRollTest.clicked.connect(self.diceRollPressed)
        
  
  
        self.showFullScreen() #display main window

    def closebuttonpressed(self): #close main window
        self.close()
    
    def helpbuttonpressed(self):
        self.help_window_open = HelpWindow() #opens up the help window
        self.help_window_open.show()
        
    def diceRollPressed(self):
        self.dice_roll_open = diceRoll()
        self.dice_roll_open.show()
  
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

        self.original_pixmap = QPixmap(get_image_path("HelpPageBackground.png")) #loading background image as a pixmap


        self.update_pixmap_size()  # Initial scaling
        
        help_close_button = QPushButton("") #code to set up properties of close button for help window
        help_close_button.clicked.connect(self.close)
        help_close_button.setIcon(qtg.QIcon(get_image_path("close-button-png-30225(1).png")))
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
    
    '''
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pick Number of Players")
        self.resize(500, 650)
        self.setStyleSheet("background-image: url('" + get_image_path("startscreen.png") + "'); background-repeat: no-repeat; background-position: center;")

        self.players1 = qtw.QPushButton("", self)
        self.players1.setIcon(qtg.QIcon(get_image_path("1players.png")))
        self.players1.setIconSize(qtc.QSize(300, 200))
        self.players1.setGeometry(100, 150, 300, 90)  
        self.players1.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players1.clicked.connect(self.player1)

        self.players2 = qtw.QPushButton("", self)
        self.players2.setIcon(qtg.QIcon(get_image_path("2players.png")))
        self.players2.setIconSize(qtc.QSize(300, 200))
        self.players2.setGeometry(100, 240, 300, 90)  
        self.players2.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players2.clicked.connect(self.player2)

        self.players3 = qtw.QPushButton("", self)
        self.players3.setIcon(qtg.QIcon(get_image_path("3players.png")))
        self.players3.setIconSize(qtc.QSize(300, 200))
        self.players3.setGeometry(100, 330, 300, 90)  
        self.players3.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players3.clicked.connect(self.player3)

        self.players4 = qtw.QPushButton("", self)
        self.players4.setIcon(qtg.QIcon(get_image_path("4players.png")))
        self.players4.setIconSize(qtc.QSize(300, 200))
        self.players4.setGeometry(100, 420, 300, 90)  
        self.players4.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players4.clicked.connect(self.player4)

        self.players5 = qtw.QPushButton("", self)
        self.players5.setIcon(qtg.QIcon(get_image_path("5players.png")))
        self.players5.setIconSize(qtc.QSize(300, 200))
        self.players5.setGeometry(100, 510, 300, 90)  
        self.players5.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.players5.clicked.connect(self.player5)

        self.show()  # Show the window
        
    '''CALLUM. HERE LIES THE VARIABLE THAT CONTAINS THE NUMBER OF PLAYERS (noOfPlayers). IT IS GLOBAL, FEEL FREE TO USE THEM IN OTHER CLASSES.'''
    def player1(self):
        selectedPlayerNo = True
        if selectedPlayerNo == True:
            self.openWindow1 = MainWindow()
            self.close()
            noOfPlayers = 1 #HERE!
            print(noOfPlayers) #test

    def player2(self):
        selectedPlayerNo = True
        if selectedPlayerNo == True:
            self.openWindow2 = MainWindow()
            self.close()
            noOfPlayers = 2
            print(noOfPlayers) #test

    def player3(self):
        selectedPlayerNo = True
        if selectedPlayerNo == True:
            self.openWindow3 = MainWindow()
            self.close()
            noOfPlayers = 3
            print(noOfPlayers) #test

    def player4(self):
        selectedPlayerNo = True
        if selectedPlayerNo == True:
            self.openWindow4 = MainWindow()
            self.close()
            noOfPlayers = 4
            print(noOfPlayers) #test

    def player5(self):
        selectedPlayerNo = True
        if selectedPlayerNo == True:
            self.openWindow5 = MainWindow()
            self.close()
            noOfPlayers = 5
            print(noOfPlayers) #test
            


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     
class diceRoll(qtw.QMainWindow):
    
    dice_images:list = []
    result_images:list = []
    
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dice Roll")
        self.resize(617,360)
        self.setStyleSheet("background-image: url('"+ get_image_path("bluebackground.jpg") +"'); background-repeat: no-repeat;")
        
        ## load images for dice and totals - saves loading this millions of times over later
        for i in range(1,7):self.dice_images.append(QPixmap(get_image_path("dice-" + str(i) + ".png")))
        for i in range(2,13): self.result_images.append(QPixmap(get_image_path("Total-" + str(i) + ".png")))
        
        self.diceRollButton = QPushButton("", self) #setting up properties of dice roll button 
        self.diceRollButton.clicked.connect(self.rollAnimation)
        self.diceRollButton.setGeometry(158, 200, 300, 200)
        self.diceRollButton.setToolTip("Roll")
        self.diceRollButton.setIcon(qtg.QIcon(get_image_path("rollbutton.png")))
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
        
        self.conor = qtw.QLabel(self) #ignore this...
        self.conor.setGeometry(50,0,200,400)
        self.conor.setStyleSheet("background: transparent; border: none;")
        self.conor.setScaledContents(True)
        
        self.noOfRolls = 0
        self.animationCounter = 0
        
        
              
        self.show()
        
    def rollAnimation(self): 
        self.announcementLabel.setPixmap(qtg.QPixmap()) 
        self.DoubleRollLabel.setStyleSheet("background: transparent; border: none;")
        self.goToJailLabel.setStyleSheet("background: transparent; border: none;")
        
        self.diceRollButton.setDisabled(True) #immediately disable button so that it cannot be pressed again whilst the animation is still running.
        if self.animationCounter < 10: #repeat roll 10 times as part of the animation
            randomface1 = random.randint(0,5)
            self.dice1.setPixmap(self.dice_images[randomface1])

            randomface2 = random.randint(0,5)
            self.dice2.setPixmap(self.dice_images[randomface2])
            
            self.animationCounter += 1
            qtm.singleShot(150, self.rollAnimation)  #wait 150ms, then reset then go again after incrementing the counter.
        else:
            #once animation completes, roll the actual dice
            self.diceRollMethod()
    
    def diceRollMethod(self):
        
        self.animationCounter = 0 #reset the animation counter so that it can run again if a double is rolled.
        
            
        diceRoll1 = random.randint(1, 6) #conor, when testing for double rolls, you can change these values both to the same integer to force a double roll x
        diceRoll2 = random.randint(1, 6)
        global total
        total = diceRoll1 + diceRoll2
        
        if diceRoll1 == 4 and diceRoll2 == 3: #ignore this 
            self.conor.setStyleSheet("background-image: url("+ get_image_path("Snapchat-675243558.jpg") +"); background-repeat: no-repeat; background-position: center;")
            qtm.singleShot(500, self.resetConor)
        
        if diceRoll1 == diceRoll2: #if a double is rolled....
            self.diceRollButton.setDisabled(False) #restore buttons functionality to allow player to roll again
            self.noOfRolls = self.noOfRolls + 1 #increment roll counter
            if self.noOfRolls >= 2: #if another double is rolled...
                self.goToJailLabel.setStyleSheet("background-image: url('"+ get_image_path("ANOTHER-DOUBLE-GO-TO-JAIL-07-02-2025.png") +"'); background-repeat: no-repeat; background-position: center;")
                self.diceRollButton.setDisabled(True) #user can only press dice roll button once
                qtm.singleShot(2000, self.close) #close after 3s
                #CALUM, SEND TO JAIL FUNCTION HERE!
            else:
                self.DoubleRollLabel.setStyleSheet("background-image: url('"+ get_image_path("DOUBLE-ROLL-ROLL-AGAIN-07-02-2025.png") + "'); background-repeat: no-repeat; background-position: center;")
        else:
            self.diceRollButton.setDisabled(True)
            qtm.singleShot(2000, self.close)
                
            
        #CHANGING THE DICE ICONS BASED ON WHICH NUMBERS HAVE BEEN RANDOMLY SELECTED: (but BETTER!)

        self.dice1.setPixmap(self.dice_images[diceRoll1 - 1])
        self.dice2.setPixmap(self.dice_images[diceRoll2 - 1])
        
        #CHANGING THE OUTPUT OF OUR ANNOUNCEMENT LABEL BASED OFF OF WHAT OUR TOTAL IS:
        
        time.sleep(0.2)
        self.announcementLabel.setPixmap(self.result_images[total - 2])
            
    def resetConor(self):
        self.conor.setStyleSheet("background: transparent; border: none;")
        

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

app = qtw.QApplication([])
mw = StartWindow()
'''CONOR. WHEN TESTING, CHANGE THE VALUE OF 'mw' TO THE NAME OF THE UI CLASS YOU WANT TO TEST. THIS WILL MAKE IT DISPLAY. love you'''


app.exec_()
