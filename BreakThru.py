from tkinter import *
from itertools import chain
from PIL import Image, ImageTk

tileSize = 40
window = Tk()
window.title("BreakThru")
geo = tileSize*14
geo = str(geo) + "x" + str(geo)
window.geometry(geo)
window.configure(background="#000")
#window.iconbitmap("icon.ico")	#	Windows only
window.iconphoto(True, PhotoImage("icon.ico"))

tutorialStr = ["""

Welcome! This is Breakthru. In this game there are two teams: silver and golden. 
The golden team wins once all of the silver pieces are captured. 
The silver team wins once the golden flagship is captured (the middle one). 
You can capture pieces that are 1 tile away from your's and each turn you have 2 moves. 
Silver start. Have fun!

""", "Arial 5 bold"]
# Starting board
rects = [
            ['0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','S','S','S','S','S','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0'],
            ['0','S','0','0','G','G','G','0','0','S','0'],
            ['0','S','0','G','0','0','0','G','0','S','0'],
            ['0','S','0','G','0','F','0','G','0','S','0'],
            ['0','S','0','G','0','0','0','G','0','S','0'],
            ['0','S','0','0','G','G','G','0','0','S','0'],
            ['0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','S','S','S','S','S','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0']
        ]

# Texture/img loader
groupImgs = []

groupDir = [
"blank.png",
"golden.png",
"silver.png",
"flagship.png",
"bricks.png",
"select.png",
"flagship_silver.png"
]

def resImg(path):
    image = Image.open(path)
    resized_image = image.resize((tileSize, tileSize), Image.NEAREST)
    groupImg = ImageTk.PhotoImage(resized_image)
    return groupImg

for i in range(0, len(groupDir)):
    groupImgs.append(resImg(groupDir[i]))

# Rect class
class Rect():
    def __init__(self, group, x, y):
        self.group = group
        self.x = x
        self.y = y

    def drawRect(self, can, size):
        can.create_image(self.x*size, self.y*size, image=groupImgs[self.group], anchor=NW)

# Input class
class Input:
    def __init__(self, eventResult):
        self.eventResult = eventResult
        self.choosen = [None, None]
        self.step = 0
        self.player = [2, 2] # silver - [2, 2], golden = [1, 3]

    def nextStep(self):
        if (self.player == [2, 2]):
            playerStr = "Silver"
            playerClr = "#999"
        else:
            playerStr = "Golden"
            playerClr = "#f90"

        if(self.step < 0):
            window.destroy()

        else:
            if ((self.step == 0) or (self.step == 2)):
                if ((findRectInArray(self.eventResult).group == self.player[0]) or (findRectInArray(self.eventResult).group == self.player[1])):
                    self.choosen[0] = findRectInArray(self.eventResult)
                    self.eventResult = None
                    changeInfo((playerStr +" has selected a piece"), "Arial 17 bold", playerClr)
                    self.step += 1
                else:
                    changeInfo("It's "+ playerStr +"'s turn! Choose a valid "+ playerStr +" piece", "Arial 14 bold", playerClr)

            elif(self.step == 1 or (self.step == 3)):
                if ((findRectInArray(self.eventResult).group != self.player[0]) and (findRectInArray(self.eventResult).group != self.player[1])):
                    dis = distance(self.choosen[0], findRectInArray(self.eventResult))
                    
                    if (dis == [0, 0]):
                        changeInfo(("You can't move your "+ playerStr +" piece to the spot it's alredy on! Choose another spot to move"), "Arial 8 bold", playerClr)

                    elif( (dis[0] <= 1) and (dis[1] <= 1)):
                        self.choosen[1] = findRectInArray(self.eventResult)
                        self.eventResult = None
                        if (self.choosen[1].group == 0):
                            changeInfo((playerStr +" has moved a piece to an empty spot"), "Arial 15 bold", playerClr)
                        else:
                            changeInfo((playerStr +" has captured enemy's piece"), "Arial 17 bold", playerClr)
                            self.choosen[1].group = 0
                        switchPlaces(self.choosen[0], self.choosen[1])
                        self.choosen = [None, None]
                        self.step +=1
                    else:
                        changeInfo(("Choosen pool is too far away! You can capture and move only to adjacent pieces"), "Arial 7 bold", playerClr)
                else:
                    changeInfo("You have already selected a "+ playerStr +" piece! Choose your opponent's piece or an empty space", "Arial 7 bold", playerClr)

            #print(self.step)
            drawAllRects()
            if(self.step>3):
                if(self.player == [2, 2]):
                    self.player = [1, 3]
                    playerStr = "Golden"
                    playerClr = "#f90"
                else:
                    self.player = [2, 2]
                    playerStr = "Silver"
                    playerClr = "#999"
                self.step = 0
                changeInfo(("It's "+playerStr +"'s turn!"), "Arial 17 bold", playerClr)
            if(rectsAmountOf(3) == 0):
                self.step = -1
                win("Silver")
            elif(rectsAmountOf(2) == 0):
                self.step = -1
                win("Golden")
            
    
    def onclick(self, event):
        self.eventResult = event
        self.nextStep()

input = Input(None)

# Setting up background
bg = Canvas(window, width=tileSize*14, height=tileSize*14, bg="#f00", highlightthickness = 0, borderwidth=0)
bg.place(relx=.5, rely=.5,anchor= CENTER)

def drawBg(img):
    bg.delete("all")
    for i in range (14):
        for j in range(14):
            bg.create_image(i*tileSize, j*tileSize, image=groupImgs[img], anchor=NW)

def drawBgFromArray(img1, img2):
    b = 0
    bg.delete("all")
    k="1010101010101001010101010101101010101010100101010101010110101010101010010101010101011010101010101001010101010101101010101010100101010101010110101010101010010101010101011010101010101001010101010101"
    for i in range (14):
        for j in range(14):
            b+=1
            if(k[b-1] == '0'):
                imgKey = img1
            else:
                imgKey = img2
            bg.create_image(i*tileSize, j*tileSize, image=groupImgs[imgKey], anchor=NW)

drawBg(4)



# Filling rects tab with proper objects according to rects 2dArray
for i in range (11):
    for j in range(11):
        if(rects[i][j] == 'G'):
            rects[i][j] = Rect(1, i, j)
        elif(rects[i][j] == 'S'):
            rects[i][j] = Rect(2, i, j)
        elif(rects[i][j] == 'F'):
            rects[i][j] = Rect(3, i, j)
        else:
            rects[i][j] = Rect(0, i, j)

rects = list(chain.from_iterable(rects))

# Creating a game canvas and positioning it
canvas = Canvas(window, height=tileSize*11,width=tileSize*11,bg="#f00", highlightthickness = 0, borderwidth=0)
canvas.place(relx=.5, rely=.5,anchor= CENTER)

# Creating an info text
bg.create_text(tileSize*7,tileSize*0.75,fill="#000",font=tutorialStr[1],text=tutorialStr[0], tag="info")
bg.update()

def changeInfo(str, strFont, color):
    bg.delete("info")
    bg.delete("info_under")
    bg.create_rectangle(tileSize*0.2,tileSize*0,tileSize*13.8,tileSize*1.5,fill="#000", tag="info_under")
    bg.create_text(tileSize*7,tileSize*0.75,fill=color,font=tutorialStr[1],text=tutorialStr[0], tag="info")
    info = bg.find_withtag("info")
    bg.itemconfig(info, text= str)
    bg.itemconfig(info, font=strFont)

def getInfo():
    info = bg.find_withtag("info")
    str = bg.itemcget(info, 'text')
    return str

# Creating a canvas which display highlights

def drawSelected():
    if(input.choosen[0] is not None):
        canvas.create_image(input.choosen[0].x*tileSize, input.choosen[0].y*tileSize, image=groupImgs[5], anchor=NW)

# Drawing all rects from the array
def drawAllRects():
    canvas.delete("all")
    for i in range(len(rects)):
        rect = rects[i]
        rect.drawRect(canvas, tileSize)
    drawSelected()
drawAllRects()

# Binding event listener for clicking on canvas
canvas.bind("<Button-1>", input.onclick)

def rectsAmountOf(groupId):
    amount = 0
    for i in range(len(rects)-1):
        if(rects[i].group == groupId):
            amount += 1
    return amount

def findRectInArray(inputEv):
    x = inputEv.x
    y = inputEv.y
    x = x//tileSize
    y = y//tileSize
    for i in range(len(rects)-1):
        if ((rects[i].x == x) and (rects[i].y == y)):
            return rects[i]

def distance(rect1, rect2):
    xDis = abs(rect1.x - rect2.x)
    yDis = abs(rect1.y - rect2.y)
    return [xDis, yDis]

def switchPlaces(rect1, rect2):
    pos1 = [rect1.x, rect1.y]
    pos2 = [rect2.x, rect2.y]

    rect1.x = pos2[0]
    rect1.y = pos2[1]

    rect2.x = pos1[0]
    rect2.y = pos1[1]

def win(winner):
    if (winner == "Silver"):
        imgs = [2, 6, 7]
        clr = "#999"
    else:
        imgs = [1, 3, 8]
        clr = "#f90"
    drawBgFromArray(imgs[1], imgs[0])
    changeInfo(winner + " has won! Click on the board to quit", "Arial 15 bold", clr)

window.mainloop()
