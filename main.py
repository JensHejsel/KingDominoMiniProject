import cv2
import numpy as np
from collections import deque
import math
from random import *

RImg = randint(1, 74) #Choose a random picture,  selected from the provided King Domino dataset, with the cropped and perspective corrected game board pictures.
InputImg = cv2.imread(f"./Cropped and perspective corrected boards/{RImg}.jpg") #Taking the chosen image and putting it into a variable to access easier.
print(f"Selected board to give score to number {RImg} ") #Display text in the console saying what board has been chosen.

cv2.imshow("Chosen Board", InputImg) #Display the chosen input image.

def sliceInputImg(InputImg): #Function that will cut the input image into 25 slices.
    Tiles = deque([]) #Make an array containing the Region of Interest for the board tiles (the slices).
    currY = 0 #Y-values within the input image, starting at position 0.

    for y in range(5): #Go through rows, which there are 5 of. Done with a for loop.
        currX = 0 #Every time the loop starts on a new row, reset the x-value.
        for x in range(5): #Go through the columns in the current row.

            currTile = InputImg[currY:(InputImg.shape[0] // 5) + currY, currX:(InputImg.shape[1] // 5) + currX] #Take out one tile from the input image to look at.

            Tiles.append(currTile) #Put the extracted tile to the output deck/array.

            currX += InputImg.shape[1] // 5 #Move where the in the column the extration happens
        currY += InputImg.shape[0] // 5 #Move which row is being extracted on
    return Tiles #Returns the list of extracted tiles

def maskTiles(tileList): #Function to mask the center of the tiles in the image, which will exclude houses etc., within the image, should make for cleaner RGB values.
    maskedTiles = deque([]) #Make an array to put the masked tiles into.

    for i in range(len(tileList)): #Going through the tiles from the input image.
        currTile = tileList[i] #Extracts the current tile to mask.
        h = currTile.shape[0] #Sets the hight in the input as a variable, avoiding super long code lines :)
        w = currTile.shape[1] #Sets the width in the input as a variable.

        mask = np.zeros(currTile.shape[:2], dtype="uint8") #Create black mask (square) to apply to picture.
        cv2.rectangle(mask, (0, 0), (w, h), 255, -1) #Applies mask to the whole image, not what we want.
        cv2.rectangle(mask, (w // 5, h // 5), (w - (w // 5), h - (h // 5)), 0, -1) #Does not apply mask to whole picutre, but only to the middle.

        masked = cv2.bitwise_and(currTile, currTile, mask=mask) #Applies mask to the current image.
        maskedTiles.append(masked) #Sends the image with the mask applied into the output array.
        # Skal bruges til billeder:
        #Used to test the displaying of the masked images.
        #cv2.imshow(f"Mask{1}", mask) #The mask on a black "picture"
        #cv2.imshow(f"CurrTile{1}", currTile) #Current extracted tile.
        #cv2.imshow(f"Mask on tile{1}", masked)  # mask applied to extracted tile.

    return maskedTiles #Returns the array of masked tiles.

def findMeanBGR(tileList, InputImg): #Function that will get the average RGB values on the individual tiles, then assemble them into a full picture again.
    newBoard = InputImg.copy() #Creates a copy of input image.
    currX = 0 #Sets the current x value to 0.
    currY = 0 #Sets the current y value to 0.

    for i in range(len(tileList)): #Go through each tile in tileList

        #Creates numpy arrays for all R, G and B values in a tile.
        Red = np.array([])
        Green = np.array([])
        Blue = np.array([])

        currImg = tileList[i]

        for y, row in enumerate(currImg):  #Go through all the pixels in the current tile.
            for x, pixel in enumerate(row):
                if not pixel[0] == 0:
                    #Put B, G and R values into an array
                    Blue = np.append(Blue, pixel[0])
                    Green = np.append(Green, pixel[1])
                    Red = np.append(Red, pixel[2])

        #Average out and round up/down the values of the R, G and B arrays.
        Red = round(np.average(Red))
        Green = round(np.average(Green))
        Blue = round(np.average(Blue))

        """ Brug til billeder i rapport
        #Testing if the RGB values work correctly.
        #print(f"tile - {i} = [{B}, {G}, {R}]")
        """
        #Assembles the averaged colored tiles into an image like the original game board.
        if currX == InputImg.shape[1]:
            currY += InputImg.shape[0] // 5
            currX = 0

        cv2.rectangle(newBoard, (currX, currY), (currX + InputImg.shape[1] // 5, currY + InputImg.shape[0] // 5), (Blue, Green, Red), -1) #Draw a square(rectangle) that will match the size of the tile onto a blank image, with the averaged RGB color filled in.
        currX += InputImg.shape[1] // 5
    """brug til billede i rapporten
    #cv2.imshow("Assembled Board", newBoard)
    """
    return newBoard

def thresholdBoard(InputBoard): #Using HSV for thresholding of new gameboard, to find what kind of tiles are on it.
    InputBoard = cv2.cvtColor(InputBoard, cv2.COLOR_BGR2HSV)

    #Billede i rapport
    #Check if HSV conversion worked.
    #cv2.imshow("HSV Tiles", InputBoard)

    Arr0 = np.zeros((5, 5), dtype="uint8") #Making a 5x5 array contraining zeros, to add the output thresholding into.

    xOffset = 2 #Offsetting the X value.
    yOffset = 2 #Offsetting the Y value.

    for y, row in enumerate(Arr0):
        for x, entry in enumerate(row):
            Value = InputBoard[yOffset + y * (InputBoard.shape[0] // 5), xOffset + x * (InputBoard.shape[1] // 5)]

            #Get the H, S and V values from each tile.
            H = Value[0]
            S = Value[1]
            V = Value[2]

            #Show in report how thresholds were made
            print(f"{x},{y} - {Value}")

            #Assigning a number id to each kind of tile.
            Ocean = 1
            Field = 2
            Grassland = 3
            Forest = 4
            Wasteland = 5
            Mine = 6

            #Threshold the obtained HSV values and give a number to the tiles in the output array.
            if (28 <= H <= 55) and (118 <= S <= 248) and (82 <= V <= 176):
                Arr0[y, x] = Grassland
            elif (87 <= H <= 126) and (92 <= S <= 278) and (88 <= V <= 202):
                Arr0[y, x] = Ocean
            elif (14 <= H <= 42) and (178 <= S <= 277) and (78 <= V <= 225):
                Arr0[y, x] = Field
            elif (24 <= H <= 106) and (48 <= S <= 236) and (28 <= V <= 114):
                Arr0[y, x] = Forest
            elif (16 <= H <= 37) and (36 <= S <= 176) and (58 <= V <= 153):
                Arr0[y, x] = Wasteland
            elif (8 <= H <= 22) and (6 <= S <= 173) and (16 <= V <= 83):
                Arr0[y, x] = Mine

    print(f"\nFound tiles =\n{Arr0}") #Print found tiles into the console.
    return Arr0

def grassFire(board, coord, currId, targetTile): #Counting the connected found tiles

    bQ = deque([])  #Create a burn queue array to keep track of coordiantes to burn.
    hasBurnt = False #Starting off as false, cause nothing has been burnt yet.

    if board[coord[0], coord[1]] == targetTile: #If the coordinates fit with the current tile being looked at, then add it to the burn queue.
        bQ.append(coord)
        hasBurnt = True #Set to true because now something has been burnt.

    while len(bQ) > 0: #As long as theres coordinates in the burn queue, keep running.
        currPos = bQ.pop()  #Pop last coordinate from the burn queue, and burn it.
        y, x = currPos
        board[y, x] = currId

        if y - 1 >= 0 and board[y - 1, x] == targetTile: #Add connected tiles to burn queue
            bQ.append((y - 1, x))
        if x - 1 >= 0 and board[y, x - 1] == targetTile:
            bQ.append((y, x - 1))
        if y + 1 < board.shape[0] and board[y + 1, x] == targetTile:
            bQ.append((y + 1, x))
        if x + 1 < board.shape[1] and board[y, x + 1] == targetTile:
            bQ.append((y, x + 1))
    if hasBurnt:
        currId += 1

    return currId, board

def findCrowns(): #Function for detecting crowns, and putting their coordinates into a 5x5 array.
    ImgGS = cv2.cvtColor(InputImg, cv2.COLOR_BGR2GRAY) #Conversion of the image to greyscale
    """Show the grayscale image in report
   # cv2.imshow("greyscale",imgGS) #Show the grayscale image
   """
    croArr = []  #Make an empty array for crown coordinates

    template = cv2.imread('crownTemplate.jpg', 0) #Template of a crown, with the background removed, to use for template matching.
    templateField = cv2.imread('fieldCrownTemplate.jpg', 0) #The crowns on the field tiles will not get detected like all other crowns, for some reason, so make a template for that.

    croArr = templateSearching(croArr, ImgGS, template, 0.7)
    croArr = templateSearching(croArr, ImgGS, templateField, 0.6)

    croMat = np.zeros((5, 5), dtype="uint8") #Put the coordinates for the crowns into a 5x5 matrix.
    for crown in croArr:
        croMat[int(crown[1] / 100), int(crown[0] / 100)] += 1

    #print(f"\n{len(croArr)} crowns found on this board") #Print found result to the console.
    #print(croMat)

    return croMat

def templateSearching(crowns, source, template, threshold): #Function for searching through the board for crowns, with a given template and a threshold.
    for i in range(4): #Run this loop 4 times, rotating the crown templates 90 degrees each time.
        template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)
        """Show in report
        #Test if the rotation works.
        #cv2.imshow(f"test{i}", template)
        """

        w, h = template.shape[::-1] #Setting the size of the drawn box to fit arond the found crowns.

        result = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED) #Template matching using the TM_CCOEFF_NORMED formula.
        #cv2.imshow("result", result) #Show the result of the template matching.
        location = np.where(result >= threshold)  #Find all locations on the image with a value greater than or equal to the threshold

        #Trying to prevent the template matching to hit the same crown multiple times.
        check = False
        for pt in zip(*location[::-1]):
            for [x, y] in crowns:
                check = False
                if (math.isclose(x, pt[0], abs_tol=15)) and (math.isclose(y, pt[1], abs_tol=15)): #Checking if the found crowns are closer than 15 pixels.
                    check = True
                    break
                else:
                    continue

            if not check: #If the currently dectected crown has not been seen before, then send into the crowns array.
                crowns.append(pt)
                cv2.rectangle(InputImg, pt, (pt[0] + w, pt[1] + h), (255, 255, 0), 2) #Draw a box around the found crowns.

   # cv2.imshow("Crowns found", InputImg) #Display image with the boxes drawn onto around the found crowns.
    return crowns

def calculateScore(StartBoard, crownArr): #Calculate the score for the selected board, using the found grouping of tiles and the crowns.
    GivenScore = 0 #Starts off as 0, as no score has been calculated yet.

    for id in range((np.amax(StartBoard) - 5) + 1): #Loop through each group of connected tiles on the board.
        numberOfCrowns = 0 #Set to 0, cause we havent found any crowns yet.
        sizeOfProperty = 0 #Set to 0, cause we havent calculated the size of the property yet.

        for y in range(5): #Divide the tile matrix into 5 rows.
            x = np.where(StartBoard[y] == id + 5)[0]
            sizeOfProperty += len(x) #Find the size of a property by taking the length.
            for n in x:
                numberOfCrowns += crownArr[y, n] #Go throught each found property and look for a crown on each tile, then take the sum of total crowns in that property.
        """Show the calculation in the report
        #print(f"{sizeOfProperty} * {numberOfCrowns} = {sizeOfProperty * numberOfCrowns}")
        """
        GivenScore += sizeOfProperty * numberOfCrowns #Calculate the final score for the board, by taking the size of the properties and multiply by number of crowns in the property.

    #print(f"\nCalculated score = {GivenScore}\n") #Display the score in console.
    return GivenScore

tiles = sliceInputImg(InputImg)
maskedTiles = maskTiles(tiles)
newBoard = findMeanBGR(maskedTiles, InputImg)
StartBoard = thresholdBoard(newBoard)
next = 5 #Next id variable for grassFire() function.

for i in range(5):
    for y, row in enumerate(StartBoard):
        for x, pixel in enumerate(row): #On each pixel in the StartBoard, call and run the grassFire() function.
            next, StartBoard = grassFire(StartBoard, (y, x), next, i + 1)

CrownBoard = findCrowns()
calculateScore(StartBoard, CrownBoard)

cv2.waitKey(0)