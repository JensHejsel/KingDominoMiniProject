import cv2
import numpy as np
from collections import deque
import math
from random import *

RImg = randint(1, 74) #Vælg et tilfældigt tal mellem 1 og 74, som bruges til at vælge et billede fra folderen "cropped and perspective corrected".
InputImg = cv2.imread(f"./Cropped and perspective corrected boards/{RImg}.jpg") #Hent det valgte billede og sæt det som en variabel, så det er nemmere at få det frem.
print(f"Selected board to give score to number {RImg}") #Fortæl hvilket billede er valgt i console.
cv2.imshow("Chosen Board", InputImg) #Vis det valgte billede i et vindue.

def sliceInputImg(InputImg): #Funktion som skærer billedet op i 25 brikker.
    Tiles = deque([]) #Opret et tomt array som kommer til at indeholde brikkerne.
    currY = 0 #Den y-værdi vi bruger starter på 0, sådan den starter fra starten af billedet.

    for y in range(5): #Loop igennem søjlerne, som der er 5 af i billedet.
        currX = 0 #Hver gang loopet starter i en ny søjle bliver x-værdien sat til 0, så man starter fra starten af.
        for x in range(5): #Loop gennem alle rækkerne som er i søjlerne.

            currTile = InputImg[currY:(InputImg.shape[0] // 5) + currY, currX:(InputImg.shape[1] // 5) + currX] #Lav en brik ud fra x- og y-værdierne, og størrelsen af startsbilldet.

            Tiles.append(currTile) #Læg alle brikker ind i det tidligere oprettede array.

            currX += InputImg.shape[1] // 5
        currY += InputImg.shape[0] // 5
    return Tiles

def maskTiles(tileList): #Funktion som skjuler det midterste af brikkerne.
    maskedTiles = deque([]) #Opret et tomt array som de nye brikker skal ind i.

    for i in range(len(tileList)): #Loop igennem alle brikker fra arrayet med brikkerne i.
        currTile = tileList[i] #Tager den nuværende brik som skal opereres på.
        h = currTile.shape[0] #Opret en variabel for højden af den brik man arbejder med.
        w = currTile.shape[1] #Opret en variabled for bredden af den brik man arbejder med.

        mask = np.zeros(currTile.shape[:2], dtype="uint8") #Opret en sort kasse som skal puttes over brikken.
        cv2.rectangle(mask, (0, 0), (w, h), 255, -1) #Putter kassen over hele brikken.
        cv2.rectangle(mask, (w // 5, h // 5), (w - (w // 5), h - (h // 5)), 0, -1) #Instiller kassen til at fylde ca 3/5 af brikken.

        masked = cv2.bitwise_and(currTile, currTile, mask=mask) #Lægger kassen hen over brikken.
        maskedTiles.append(masked) #Lægger de nye brikker ind i det array der blev oprettet tidligere.

    return maskedTiles

def findMeanBGR(tileList, InputImg): #Funktion som finder de gennemsitlige RGB værdier for hver brik og samler dem i en ny spilleplade.
    newBoard = InputImg.copy() #Opret en kopi af den originale spilleplade.
    currX = 0 #Sætter start x-positionen til 0.
    currY = 0 #Sætter start y-positionen til 0.

    for i in range(len(tileList)): #Loop gennem alle brikker i tileList arrayet.

        #Opret arrays til alle R-, G- og B-værdier i en brik.
        Red = np.array([])
        Green = np.array([])
        Blue = np.array([])

        currImg = tileList[i]

        for y, row in enumerate(currImg): #Loop gennem alle pixels i den nuværende brik.
            for x, pixel in enumerate(row):
                if not pixel[0] == 0:
                    #Læg R-, G- og B-værdierne ind i arrayet.
                    Blue = np.append(Blue, pixel[0])
                    Green = np.append(Green, pixel[1])
                    Red = np.append(Red, pixel[2])

        #Find gennemsnittet af hver værdi og rund dem op eller ned.
        Red = round(np.average(Red))
        Green = round(np.average(Green))
        Blue = round(np.average(Blue))

        #Samler alle nye farvede brikker ind i et nyt billede af en spilleplade.
        if currX == InputImg.shape[1]:
            currY += InputImg.shape[0] // 5
            currX = 0

        cv2.rectangle(newBoard, (currX, currY), (currX + InputImg.shape[1] // 5, currY + InputImg.shape[0] // 5), (Blue, Green, Red), -1) #Tegn en kasse som har samme størrelse som brikker, og put dem ind i et billede med farvede brikker.
        currX += InputImg.shape[1] // 5

    return newBoard

def thresholdBoard(newBoard): #Funktion til at finde H-, S- og V-værdier til at lave thresholds med.
    HSVBoard = cv2.cvtColor(newBoard, cv2.COLOR_BGR2HSV)

    Arr0 = np.zeros((5, 5), dtype="uint8") #Opret et 5x5 array som threshold værderine bliver lagt ind i.

    xOffset = 1
    yOffset = 1

    for y, row in enumerate(Arr0):
        for x, entry in enumerate(row):
            Value = HSVBoard[yOffset + y * (HSVBoard.shape[0] // 5), xOffset + x * (HSVBoard.shape[1] // 5)]

            #Tag H-, S- og V-værdierne fra hver brik.
            H = Value[0]
            S = Value[1]
            V = Value[2]

            #Giv hver type brik et id, så vi kan se om programmet har fundet de rigtige.
            Ocean = 1
            Field = 2
            Grassland = 3
            Forest = 4
            Wasteland = 5
            Mine = 6

            #Threshold med de fundne HSV værdier, og giv hver brik et id der passer sammen.
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

    print(f"\nFound tiles =\n{Arr0}") #Vis de fundne brikker i console.
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

def findCrowns():
    ImgGS = cv2.cvtColor(InputImg, cv2.COLOR_BGR2GRAY)

    croArr = []

    template = cv2.imread('crownTemplate.jpg', 0)
    templateField = cv2.imread('fieldCrownTemplate.jpg', 0)

    croArr = foundCrownsImage(croArr, ImgGS, template, 0.7)
    croArr = foundCrownsImage(croArr, ImgGS, templateField, 0.6)

    croMat = np.zeros((5, 5), dtype="uint8")
    for crown in croArr:
        croMat[int(crown[1] / 100), int(crown[0] / 100)] += 1

    print(f"\n{len(croArr)} crowns found on this board")
    print(croMat)

    return croMat

def foundCrownsImage(crowns, source, template, threshold): #Funktion som laver og viser hvad template matching på et billede.
    for i in range(4): #Kør loopet 4 gange, hver gang roteres templates med 90 grader for at få alle mulige vinkler med.
        template = cv2.rotate(template, cv2.ROTATE_90_CLOCKWISE)

        w, h = template.shape[::-1] #Bestem størrelsen på en kasse som tegnes rundt om de funde kroner.

        result = cv2.matchTemplate(source, template, cv2.TM_CCOEFF_NORMED) #Template matching ved brug af TM_CCOEFF_NORMED formlen.

        location = np.where(result >= threshold) #Find alle lokationer på billedet hvor template matching er større end eller lig med treshold.

        #Forsøger at forhindre at template matching rammer den samme krone flere gange.
        check = False
        for pt in zip(*location[::-1]):
            for [x, y] in crowns:
                check = False
                if (math.isclose(x, pt[0], abs_tol=15)) and (math.isclose(y, pt[1], abs_tol=15)): #Tjekker om kronerne er tættere på hinanden end 15 pixels.
                    check = True
                    break
                else:
                    continue

            if not check: #Hvis der bliver fundet en ny krone, som ikke er set før, læg den i krone arrayet.
                crowns.append(pt)
                cv2.rectangle(InputImg, pt, (pt[0] + w, pt[1] + h), (255, 255, 0), 2) #Tegn en kasse rundt om de fundne kroner.

    cv2.imshow("Crowns found", InputImg) #Vis billedet med kasserne tegnet på.
    return crowns

def calculateScore(StartBoard, crownArr): #Udregn point score for den valgte spilleplade. Gøres ved: fundne properties * antal af kroner = score.
    GivenScore = 0 #Denne værdi starter på 0, da der ikke er givet en score endnu.

    for id in range((np.amax(StartBoard) - 5) + 1): #Loop gennem hver funden property (sammenhængende brikker af samme type).
        numberOfCrowns = 0 #Starter som 0, da der ikke er fundet nogle kroner endnu.
        sizeOfProperty = 0 #Starter som 0, da der ikke er udregnet nogen størrelse på properties endnu.

        for y in range(5): #Opdel arrayet i 5 søjler.
            x = np.where(StartBoard[y] == id + 5)[0]
            sizeOfProperty += len(x) #Find størrelsen af en property, ved at tage længden af søjlen.
            for n in x:
                numberOfCrowns += crownArr[y, n] #Find alle kroner placeret i hver property.

        GivenScore += sizeOfProperty * numberOfCrowns #Udregn den endelige score for spillepladen.

    print(f"\nCalculated score = {GivenScore}\n") #Vis scoren i console.
    return GivenScore

tiles = sliceInputImg(InputImg)
maskedTiles = maskTiles(tiles)
newBoard = findMeanBGR(maskedTiles, InputImg)
StartBoard = thresholdBoard(newBoard)
next = 5 #Bruges i grassFire().

#Bruges til scoring på det sammensatte bræt.
for i in range(5):
    for y, row in enumerate(StartBoard):
        for x, pixel in enumerate(row): #På hver pixel i det originale spillebræt og kald grassFire().
            next, StartBoard = grassFire(StartBoard, (y, x), next, i + 1)

CrownBoard = findCrowns()
calculateScore(StartBoard, CrownBoard)

cv2.waitKey(0)