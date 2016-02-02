import pygame, sys
import os
from pygame.locals import *

##Window init
pygame.init() 
fpsClock = pygame.time.Clock()

WWIDTH  = 1280
WHEIGHT = 720

##Files
mapDir = "./maps"

#f = open("File.map", "r")

#tile sets
tiles = pygame.image.load("./images/tiles.png")

#saving images
fileSaved = pygame.image.load("./images/saved_on.png")
fileNotSaved = pygame.image.load("./images/saved_off.png")

#scroll arrows
leftScrollArrow = pygame.image.load("./images/scroll_left.png")
rightScrollArrow = pygame.image.load("./images/scroll_right.png")
upScrollArrow = pygame.image.load("./images/scroll_up.png")
downScrollArrow = pygame.image.load("./images/scroll_down.png")
leftScrollArrowClick = pygame.image.load("./images/scroll_left_clicked.png")
rightScrollArrowClick = pygame.image.load("./images/scroll_right_clicked.png")
upScrollArrowClick = pygame.image.load("./images/scroll_up_clicked.png")
downScrollArrowClick = pygame.image.load("./images/scroll_down_clicked.png")

#collision toggle
collisionOn = pygame.image.load("./images/collision_on.png")
collisionOff = pygame.image.load("./images/collision_off.png")

##Init window
window = pygame.display.set_mode((WWIDTH,WHEIGHT))
font = pygame.font.Font('freesansbold.ttf', 20)
pygame.key.set_repeat(750, 1)



##Lists
mapList = []
tempMapList = []

tileTypeOnScreen = []
onTile = [0]

tileIdList = []
tileTypeList = []

##Colours
white  =                (255,255,255)
black  =                (  0,  0,  0)
red    =                (255,  0,  0)
green  =                (  0,255,  0)
blue   =                (  0,  0,255)
yellow =                (255,255,  0)
purple =                (255,  0,255)
cyan   =                (  0,255,255)

tilePanel =             ( 69, 69, 69)
collisionTileSelected = (213, 12, 12)
tileSelected =          (147,213, 12)
tileBG =                ( 36, 36, 36)
tileSetDarkDetail =     ( 56, 56, 56)
tileSetLightDetail =    ( 97, 97, 97)
scrollBar =             ( 30, 30, 30)
scrollBarDetail =       ( 49, 49, 49)
mapGrid =               ( 30, 30 ,30)

##Constants
tileWidth = 32
padding = 10

#Tiles that will fit on the screen
screenSizeX = 33
screenSizeY = 22

##Stuff for BG
tilePanelLeft = screenSizeX * tileWidth 
tilePanelRight = WWIDTH - tilePanelLeft
tilePanelBottom = WHEIGHT * 0.75

buttonPanelTop = tilePanelBottom + 15
buttonPanelLeft = tilePanelLeft + 20

scrollBarWidth = 15

##Variables
mouseX = 0
mouseY = 0
mouseMode = 0

mapSizeX = 0
mapSizeY = 0

mapMoveX = 0
mapMoveY = 0
tileMoveY = 0

mapNum = 0

tileX = 0
tileY = 0
tile = 0

tileSetTile = 0
rTileSetTile = 1
tileSetType = 2
rTileSetType = 2

#Toggles
mouseButtonDown = False
gridToggle = False
collisionToggle = True

lCollisionToggle = False
rCollisionToggle = True

#################################################################

def drawBox(x, y, colour, width, lWidth, place):
    
    if (place >= 1000):
        place -= 1000
        pygame.draw.line(window, colour, (x, y + width ), (x + width - 1, y + width), lWidth)#Bottom line
        
    if (place >= 100):
        place -= 100
        pygame.draw.line(window, colour, (x + width, y), (x + width, y + width - 1), lWidth)#Right line

    if (place >= 10):
        place -= 10
        pygame.draw.line(window, colour, (x - 2 , y), (x - 2 , y + width - 1), lWidth) #Left line

    if (place == 1):
        pygame.draw.line(window, colour, (x, y - 2), (x + width - 1, y - 2), lWidth) #Top line

    #draw Nothing

#################################################################

def drawTileSetBg():
    pygame.draw.rect(window, tilePanel, (tilePanelLeft, 0, tilePanelRight, WHEIGHT * 0.75)) 

def drawButtonPanel():
    pygame.draw.rect(window, tilePanel, (tilePanelLeft, tilePanelBottom, tilePanelRight, tilePanelBottom *0.25))
    pygame.draw.line(window, purple, (tilePanelLeft, tilePanelBottom), (WWIDTH, tilePanelBottom),2 )
    pygame.draw.line(window, purple, (tilePanelLeft, tilePanelBottom + tilePanelBottom * .25 - 2), (WWIDTH,tilePanelBottom + tilePanelBottom * .25 - 2),2 )

def drawScrollBars():
    ##Verticle
    pygame.draw.rect(window, scrollBar, (tilePanelLeft, 0, scrollBarWidth, WHEIGHT))

    ##Horizontal
    pygame.draw.rect(window, scrollBar, (0, WHEIGHT - scrollBarWidth - 1, tilePanelLeft, scrollBarWidth + 1))

    pygame.draw.line(window, (scrollBarDetail),(tilePanelLeft,0), (tilePanelLeft, WHEIGHT), 1) #vert scroll panel detail
    pygame.draw.line(window, (tileSetDarkDetail),(0, WHEIGHT - scrollBarWidth - 1), (tilePanelLeft + scrollBarWidth, WHEIGHT - scrollBarWidth - 1), 1) #Horizontal scroll bar detail

    pygame.draw.line(window, (tileSetDarkDetail),(tilePanelLeft + scrollBarWidth,0), (tilePanelLeft + scrollBarWidth, WHEIGHT), 1) #vert scroll panel detail
    pygame.draw.line(window, (scrollBarDetail),(tilePanelLeft + scrollBarWidth + 1,0), (tilePanelLeft + scrollBarWidth + 1, WHEIGHT), 1) #vert scroll panel detail

##################################################################

def getPlace(tileNum):
    place = 0
    
    #check top
    if (tileNum < mapSizeX):
        place += 1
    elif (tileTypeList[tileNum - mapSizeX] == 1):
        place += 1

    #Check left
    if (tileNum % mapSizeX == 0):
        place += 10
    elif (tileTypeList[tileNum - 1] == 1):
        place += 10

    if ((tileNum + 1) % mapSizeX == 0 and tileNum > 0):
        place += 100
    elif (tileTypeList[tileNum + 1] == 1):
        place += 100

    if (tileNum >= mapSizeX * (mapSizeY - 1)):
        place += 1000
    elif (tileTypeList[tileNum + mapSizeX] == 1):
        place += 1000
    
    return place    

#################################################################

def resetGlobals():
    global mapSizeX, mapSizeY, mapMoveX, mapMoveY, tileX, tileY, tile
    global tileIdList, tileTypeList, tileTypeOnSceen
    mapSizeX = mapSizeY = mapMoveX = mapMoveY = tileX = tileY = tile = 0
    tileTypeOnSceen = []
    tileIdList = []
    tileTypeList = []

#################################################################
    
def readMap(mapFile):
    global mapSizeX
    global mapSizeY
    ##Read all lines
    mFile = "./maps/" + str(mapFile)
    
    f = open(mFile, "r")
    line = f.read()

    ##Initialize 2 digit number check
    colon = 0

    ##set to 1 on newline to get mapSizeX
    mapSizeXEnd = 0

    ##Reads the map file

    while (len(line) != 0):


        ##Checks for space or new line
        spaceCheck = line[0]
        if (line[0] == " " or line[0] == "\n"):
            if (line[0] == "\n"):
                mapSizeXEnd = 1
                mapSizeY += 1
            ##Deletes space or newline
            line = line.replace(spaceCheck, '', 1)

        ##check for 2 digit number    
        try:
            colonCheck = line[1]
        except:
            break
        
        if colonCheck != ":":
            colon = 1
        tile = line[0:4 + colon]
        line = line.replace(tile, '', 1)

        ##Gets tileID and tileType
        tileIdList.append(int( tile[0:1 + colon]))
        tileTypeList.append(int( tile[2 + colon:3 + colon]))
        colon = 0

        if (mapSizeXEnd != 1):
            mapSizeX += 1
            
#################################################################
    
def getMaps():
    for i in range(0, len(os.listdir(mapDir))):
        fileName = os.listdir(mapDir)[i]
        ext = fileName[len(fileName) - 4: len(fileName)]
        ##Checks for the .map on any file in the folder
        if ext == ".map":
            mapList.append(fileName)
            tempMapList.append("temp_" + fileName)

#################################################################
            
def drawMap(mapSizeX, mapSizeY):

    global tileTypeOnScreen
    tileTypeOnScreen = []
    #coordinates
    x = 0
    y = 0
    
    image = tiles
    
    tileSizeX = 0
    tileSizeY = 0

    
    countX = (mapMoveX // tileWidth) + ((mapMoveY // tileWidth) * mapSizeX) #gets tile number
    countY = 0 #used to tell the function to stop drawing on the y axis
    for i in range (0, mapSizeX * mapSizeY):
        if (countY == screenSizeY):
            break
        
        tileId = tileIdList[countX]
        #Gets the tile from the tileset
        tileSizeX = (tileWidth * (tileId % 4))
        tileSizeY = (tileWidth * (tileId // 4))

        window.blit(image, (x,y), (tileSizeX, tileSizeY, tileWidth, tileWidth))

        
        #Draws collision boxes
        if (tileTypeList[countX] == 2):
            tileTypeOnScreen.append(countX)
                     
        #Moves to the right one tile
        x += tileWidth

        #When i  equals mapsize move down a tile annd reset x to 0
        if ((i + 1) % screenSizeX == 0 and i > 1):
            countY += 1
            x = 0
            y += tileWidth
            countX += mapSizeX - screenSizeX
            
        countX += 1
        if countX >= (mapSizeX * mapSizeY):
            break
    
    
###################################################################
    
def drawCollisions():
    x = 0
    y = 0
    for i in tileTypeOnScreen:
        tileX = i % mapSizeX
        tileY = i // mapSizeX

        x = tileX * tileWidth - mapMoveX
        y = tileY * tileWidth - mapMoveY
        
        place = getPlace(i)
 
        drawBox(x, y, collisionTileSelected, tileWidth, 2, place)
    drawScrollBars()

###################################################################
    
def drawTileSet():
    origX = tilePanelLeft + ((WWIDTH - tilePanelLeft) / 2) - 2 * tileWidth - padding
    x = origX
    y = tileWidth

    setX = 0
    setY = 0

    for i in range (0, 33):
        tileRect = (setX, setY + tileMoveY, tileWidth, tileWidth)
        window.blit(tiles, (x, y), tileRect)

        x += tileWidth + padding
        setX += tileWidth
        if (i > 0 and i % 4 == 0):
            setX = 0
            setY += tileWidth
            
            x = origX
            y += tileWidth + padding
    

##################################################################

def createTemps():
    for i in mapList:
        resetGlobals()
        readMap(i)
        newFile = open("./maps/temp_" + i, "w")

        for j in range(0, mapSizeX * mapSizeY):
            
            try:
                newFile.write(str(tileIdList[j]) + ":" + str(tileTypeList[j]) + " ")
            except:
                break
            
            if ((j + 1) % mapSizeX == 0):
                newFile.write("\n")
        newFile.close()

##################################################################

def destroyTemps():
    for i in tempMapList:
        try:
            os.remove("./maps/" + i)
        except:
            continue

##################################################################
            
def saveMaps(n):
    newFile = open(mapList[n], "w")

    for i in range (0, mapSizeX * mapSizeY):
        newFile.write(str(tileIdList[i]) + ":" + str(tileTypeList[i]) + " ")
        if ((i + 1) % mapSizeX == 0):
            newFile.write("\n")
        
    newFile.close()

##################################################################

def saveTempMap(n):
    newFile = open("./maps/" + tempMapList[n], "w")

    for i in range (0, mapSizeX * mapSizeY):
        newFile.write(str(tileIdList[i]) + ":" + str(tileTypeList[i]) + " ")
        if ((i + 1) % mapSizeX == 0):
            newFile.write("\n")

    print tempMapList[n] + " File saved"
    newFile.close()

##################################################################
    
def switchMap(n):
    global mapNum
    resetGlobals()
    try:
        if (mapNum < 0):
            mapNum = len(tempMapList) - 1
        readMap(tempMapList[n])
        pygame.display.set_caption(mapList[n])
    except:
        if (mapNum < 0):
            mapNum = len(tempMapList) - 1
        else:
            mapNum = 0
        readMap(tempMapList[mapNum])
        pygame.display.set_caption(mapList[mapNum])
        
    drawMap(mapSizeX, mapSizeY)

#################################################################

def drawMapGrid():
    ##Verticle lines
    for i in range(0, screenSizeX + 1): #33 is the tile width show at one time
        pygame.draw.line(window, (mapGrid),(tileWidth * i , 0), ( tileWidth * i , WHEIGHT - 17), 2)

    #Horizontal lines
    for i in range(0, screenSizeY + 1): #28 is the tile height show at one time
        pygame.draw.line(window, (mapGrid),(0,  tileWidth * i ), (tilePanelLeft - 1, tileWidth * i ), 2) #horz scroll panel detail

#################################################################
        
def getCoords(mouseX, mouseY):
    global tileX, tileY, tile
    tileX = (mouseX + mapMoveX) // 32
    tileY = (mouseY + mapMoveY) // 32
    tile = tileX + (mapSizeY * tileY)

#################################################################

def updateMapGui():
    if (gridToggle == True):
        drawMapGrid()        
    if (collisionToggle == True):
        drawCollisions()

#################################################################
        
def drawTile(tile, mode, tileType, x1, y1):
    
    tileId = tileIdList[tile]

        
    colour = green
    #Gets the tile from the tileset
    tileSizeX = (tileWidth * (tileId % 4))
    tileSizeY = (tileWidth * (tileId // 4))
    
    tileX = tile % mapSizeX
    tileY = tile // mapSizeX

    x = tileX * tileWidth - mapMoveX
    y = tileY * tileWidth - mapMoveY
    if (mode == 0):
        window.blit(tiles, (x,y), (tileSizeX, tileSizeY, tileWidth, tileWidth))

    if (mode == 2):
        if (tileTypeList[tile] == 2):
            colour = collisionTileSelected

        updateMapGui()
        drawBox(x + 2, y + 2, colour, tileWidth - 4, 2, 1111)

    if (mode == 3):
        tileSizeX = (tileWidth * (tileType % 4))
        tileSizeY = (tileWidth * (tileType // 4))
        window.blit(tiles, (x1,y1), (tileSizeX, tileSizeY, tileWidth, tileWidth))
#################################################################

def updateTile():
    getCoords(mouseX, mouseY)
    if tileX < 31:
        drawTile(onTile[0] - 51, 0, 0, 0, 0)
        drawTile(onTile[0] - 50, 0, 0, 0, 0)
        drawTile(onTile[0] - 49, 0, 0, 0, 0)
        drawTile(onTile[0] - 1, 0, 0, 0, 0)
        drawTile(onTile[0], 0, 0, 0, 0)
        drawTile(onTile[0] + 1, 0, 0, 0, 0)
        drawTile(onTile[0] + 51, 0, 0, 0, 0)
        drawTile(onTile[0] + 50, 0, 0, 0, 0)
        drawTile(onTile[0] + 49, 0, 0, 0, 0)
    drawTile(onTile[0], 0, 0, 0, 0)
    onTile.pop()
    drawTile(tile, 2, 0, 0, 0)
    onTile.append(tile)
    

#################################################################

def drawToggleCollisions(mode):
    global lCollisionToggle, rCollisionToggle

    
    #left
    if (mode == 0):
        if (lCollisionToggle == True):
            lCollisionToggle = False
        else:
            lCollisionToggle = True
    #right
    if (mode == 1):
        if (rCollisionToggle == True):
            rCollisionToggle = False
        else:
            rCollisionToggle = True

    if (lCollisionToggle == False):
        lColour = green
    else:
        lColour = red

    if (rCollisionToggle == False):
        rColour = green
    else:
        rColour = red
        
    drawBox(buttonPanelLeft , buttonPanelTop + tileWidth + padding,  lColour,tileWidth, 2, 1111)
    drawBox(buttonPanelLeft + padding + tileWidth, buttonPanelTop + tileWidth + padding,  rColour, tileWidth, 2, 1111)
        
#################################################################

def updateLeft():
    drawMap(mapSizeX, mapSizeY)
    updateMapGui()
    updateTile()

def updateRight():
    drawTileSetBg()
    drawScrollBars()
    drawTileSet()

#################################################################

def onLeftMouseDown(mode):
    #mode == 1: in map
    getCoords(mouseX, mouseY)
    global tileSetTile, tileSetType
    onTileA = 0

    if (lCollisionToggle == False):
        tileSetType = 1
    else:
        tileSetType = 2


    if (mode == 1):
        if (tileSetType == 2):
            if (tile not in tileTypeOnScreen):
                tileTypeOnScreen.append(tile)
        else:
            if (tile in tileTypeOnScreen):
                tileTypeOnScreen.remove(tile)

        tileIdList[tile] = tileSetTile
        tileTypeList[tile] = tileSetType
        
        updateMapGui()
        updateTile()

    elif (mode == 2):
        onTileA = 0
        origX = tilePanelLeft + ((WWIDTH - tilePanelLeft) / 2) - 2 * tileWidth - padding
        for i in range(0, 5):
            if (mouseX >= (origX + (i * padding +  (i * tileWidth)))):
                if (mouseX <= (origX + tileWidth + (i * padding + (i * tileWidth)))):
                    onTileA += i
                    for i in range(0, 9):
                        if (mouseY >= tileWidth + (i * padding + (i * tileWidth))):
                            if (mouseY <= 2 * tileWidth + (i * padding +  (i * tileWidth))):
                                onTileA += i * 4
                                tileSetTile = onTileA + (tileMoveY // tileWidth) * 4
        updateRight()

    elif (mode == 3):
        for i in range (0, 2):
            if (mouseX >= buttonPanelLeft + (i * padding + (i * tileWidth))):
                if (mouseX <= (buttonPanelLeft + tileWidth) + (i * padding + (i * tileWidth))):                    
                    if (mouseY >= buttonPanelTop + tileWidth + padding and mouseY <= buttonPanelTop + padding + (2 * tileWidth)):
                        drawToggleCollisions(i)


##################################################################

def onRightMouseDown(mode):
    #mode == 1: in map
    getCoords(mouseX, mouseY)
    global rTileSetTile, tileSetType
    onTileA = 0

    if (rCollisionToggle == False):
        tileSetType = 1
    else:
        tileSetType = 2


    if (mode == 1):
        if (tileSetType == 2):
            if (tile not in tileTypeOnScreen):
                tileTypeOnScreen.append(tile)
        else:
            if (tile in tileTypeOnScreen):
                tileTypeOnScreen.remove(tile)
                
        tileIdList[tile] = rTileSetTile
        tileTypeList[tile] = tileSetType
        updateMapGui()
        updateTile()

    elif (mode == 2):
        onTileA = 0
        origX = tilePanelLeft + ((WWIDTH - tilePanelLeft) / 2) - 2 * tileWidth - padding
        for i in range(0, 5):
            if (mouseX >= (origX + (i * padding +  (i * tileWidth)))):
                if (mouseX <= (origX + tileWidth + (i * padding + (i * tileWidth)))):
                    onTileA += i
                    for i in range(0, 9):
                        if (mouseY >= tileWidth + (i * padding + (i * tileWidth))):
                            if (mouseY <= 2 * tileWidth + (i * padding +  (i * tileWidth))):
                                onTileA += i * 4
                                rTileSetTile = onTileA + (tileMoveY // tileWidth) * 4        
                    
        updateRight()        
        #rTileSetTile = onTileA + (tileMoveY // tileWidth) * 4 
    
#################################################################
    
def getText(text, colour, x, y):
    textSurfaceObject = font.render(text, True, colour)
    textRectObj = textSurfaceObject.get_rect()
    textRectObj.topleft = (x,y)
    window.blit(textSurfaceObject, textRectObj)

#################################################################

def updateText():
    pygame.draw.rect(window, tilePanel, (tilePanelLeft + scrollBarWidth, tilePanelBottom + (tilePanelBottom *0.25), tilePanelRight - scrollBarWidth, tilePanelBottom / 2))
    getText("[" + str(tileX) + ", " + str(tileY) + ", " + str(tile) + "]", black, screenSizeX * tileWidth + scrollBarWidth + 1, tilePanelBottom + (tilePanelBottom * 0.25))
    getText("(" + str(mapList[mapNum]) + ")", black, screenSizeX * tileWidth + scrollBarWidth + 1, tilePanelBottom + (tilePanelBottom * 0.25) + 20)

#################################################################
    
#Init Everything
    
getMaps()
createTemps()

switchMap(0)
drawTileSetBg()
drawButtonPanel()

drawScrollBars()

drawTileSet()

drawCollisions()
drawTile(tile, 3, 0, buttonPanelLeft, buttonPanelTop)
drawTile(tile, 3, rTileSetTile, buttonPanelLeft + padding + tileWidth, buttonPanelTop)
drawToggleCollisions(-1)

#################################################################

while True: #Main loop
            
#################################################################
##EVENTS
#################################################################

    for event in pygame.event.get():
        
        (button1, button2, button3) = pygame.mouse.get_pressed()
        if event.type == QUIT:
            destroyTemps()
            pygame.quit()
            sys.exit()
        if event.type ==  MOUSEMOTION:
            mouseX, mouseY = event.pos

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                destroyTemps()
                pygame.event.post(pygame.event.Event(QUIT))

        ##Mouse in grid
        if (mouseX < tilePanelLeft and mouseY < (screenSizeY * tileWidth)):
            updateTile()

            if (event.type == MOUSEBUTTONDOWN):
                ##Scroll up
                if (event.button == 4):
                    if (mapMoveY == 0):
                        continue
                    else:
                        mapMoveY -= tileWidth
                        updateLeft()
                #Scroll down
                if (event.button == 5):
                    if (mapMoveY == (mapSizeY - screenSizeY) * tileWidth):    
                        continue
                    else:
                        mapMoveY += tileWidth
                        updateLeft()
                        
            if event.type == KEYDOWN:

                ##MapMove with arrow keys
                if event.key == K_LEFT:
                    if (mapMoveX == 0):
                        continue
                    else:
                        mapMoveX -= tileWidth
                        updateLeft()
                if event.key == K_RIGHT:
                    if (mapMoveX == (mapSizeX - screenSizeX) * tileWidth):
                        continue
                    else:
                        mapMoveX += tileWidth
                        updateLeft()

                if event.key == K_UP:
                    if (mapMoveY == 0):
                        continue
                    else:
                        mapMoveY -= tileWidth
                        updateLeft()

                if event.key == K_DOWN:
                    if (mapMoveY == (mapSizeY - screenSizeY) * tileWidth):
                        
                        continue
                    else:
                        mapMoveY += tileWidth
                        updateLeft()
        
            if (button1 == 1):
                onLeftMouseDown(1)

            if (button3 == 1):
                onRightMouseDown(1)
            ##Tileset move with arrow keys
        if (mouseX >= tilePanelLeft):

            if (event.type == MOUSEBUTTONDOWN):
                ##Scroll up
                if (event.button == 4):
                    tileMoveY -= tileWidth
                    if (tileMoveY < 0):
                        tileMoveY += tileWidth
                #Scroll down
                if (event.button == 5):
                    tileMoveY += tileWidth
                    if (tileWidth * 8 + tileMoveY > 512):
                        tileMoveY -= tileWidth
                        
            if event.type == KEYDOWN:
                if (event.key == K_DOWN):
                    tileMoveY += tileWidth
                    if (tileWidth * 8 + tileMoveY > 512):
                        tileMoveY -= tileWidth

                if (event.key == K_UP):
                    tileMoveY -= tileWidth
                    if (tileMoveY < 0):
                        tileMoveY += tileWidth
                   
            if (event.type == MOUSEBUTTONDOWN):
                if (event.button == 1):
                    onLeftMouseDown(2)
                    onLeftMouseDown(3)
                    drawTile(tile, 3, tileSetTile, buttonPanelLeft, buttonPanelTop)

                if (event.button == 3):
                    onRightMouseDown(2)
                    drawTile(tile, 3, rTileSetTile, buttonPanelLeft + padding + tileWidth, buttonPanelTop)
               
            updateRight()


        #General key down
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                saveTempMap(mapNum)
                mapNum += 1
                switchMap(mapNum)
            elif event.key == K_b:
                saveTempMap(mapNum)
                mapNum = mapNum - 1
                switchMap(mapNum)

            #Grid toggle
            if event.key == K_g:
                if (gridToggle == True):
                    gridToggle = False
                else:
                    gridToggle = True
                if (gridToggle == False):
                    drawMap(mapSizeX, mapSizeY)

            #collision toggle
            if event.key == K_c:
                if(collisionToggle == True):
                    collisionToggle = False
                else:
                    collisionToggle = True
                if (collisionToggle == False):
                    drawMap(mapSizeX, mapSizeY)
                
            updateMapGui()
                
                
#################################################################

        
    updateText()
    pygame.display.set_caption(str(fpsClock.get_fps()))
    pygame.display.flip()
    #fpsClock.tick(300)
