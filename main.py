import cv2 as cv
import numpy as np
from collections import deque

# billedet vi tager udgangspunkt i:
inputImage = cv.imread("4.jpg")

# to billeder af sorte pixels:
tileTypeImage = np.array([[0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0]])

crownImage = np.array([[0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0]])

# Vi giver hver af de 6 forskellige tiles et bestemt ID.
ocean = 1
desert = 2
field = 3
forest = 4
stone = 5
wasteland = 6

# Vi giver mængden af kroner et bestemt ID.
oneCrown = 1
twoCrowns = 2

#
def sliceImage(img):
    """
    :param img:
    :return:
    Denne funktion tager imod et billede og skærer det ud i 25 slices.
    """
    slices = []
    for y in range(0,img.shape[0],int(img.shape[0]/5)):
        horizontalSlices = []
        for x in range(0,img.shape[1],int(img.shape[1]/5)):
            slice = img[y: y+int(img.shape[0]/5), x: x+int(img.shape[1]/5)]
            horizontalSlices.append(slice)
        slices.append(horizontalSlices)
    return slices

# Vi bruger denne funktion til at finde color thresholds til de forskellige typer af tiles.
def findMeanBGR(img):
    """
    :param img:
    :return:
    Denne funktion tager imod et billede og finder dets gennemsnitlige BGR værdi.
    Disse BGR værdier blev brugt til at finde thresholds for de forskellige typer af tiles.
    """
    meanBGRRow = np.average(img,axis=0)
    meanBGR = np.average(meanBGRRow,axis=0)
    return meanBGR

# Denne funktion finder ud hvad hvert slice er for en type og ændrer placeringen i vores 0-image til det givne ID.
def defineTileTypes(slices):
    """
    :param slices:
    :return:
    Denne funktion giver et passende ID (tile type) til hvert slice, baseret på hvilket BGR threshold slicet passer ind i.
    """
    yAxis = -1
    xAxis = -1
    for y in slices:
        yAxis+=1
        if yAxis == 5:
            yAxis = 0
        for x in y:
            xAxis+=1
            if xAxis == 5:
                xAxis = 0
            currentSliceBGRMean = findMeanBGR(x)
            if currentSliceBGRMean[0] > 108 and currentSliceBGRMean[0] < 163 and currentSliceBGRMean[1] > 77 and currentSliceBGRMean[1] < 87 and currentSliceBGRMean[2] > 4 and currentSliceBGRMean[2] < 50:
                tileTypeImage[yAxis][xAxis] = ocean
            elif currentSliceBGRMean[0] > 4 and currentSliceBGRMean[0] < 18 and currentSliceBGRMean[1] > 145 and currentSliceBGRMean[1] < 169 and currentSliceBGRMean[2] > 170 and currentSliceBGRMean[2] < 192:
                tileTypeImage[yAxis][xAxis] = desert
            elif currentSliceBGRMean[0] > 28 and currentSliceBGRMean[0] < 34 and currentSliceBGRMean[1] > 119 and currentSliceBGRMean[1] < 143 and currentSliceBGRMean[2] > 93 and currentSliceBGRMean[2] < 113:
                tileTypeImage[yAxis][xAxis] = field
            elif currentSliceBGRMean[0] > 28 and currentSliceBGRMean[0] < 30 and currentSliceBGRMean[1] > 62 and currentSliceBGRMean[1] < 67 and currentSliceBGRMean[2] > 59 and currentSliceBGRMean[2] < 62:
                tileTypeImage[yAxis][xAxis] = forest
            elif currentSliceBGRMean[0] > 100 and currentSliceBGRMean[0] < 105 and currentSliceBGRMean[1] > 110 and currentSliceBGRMean[1] < 115 and currentSliceBGRMean[2] > 100 and currentSliceBGRMean[2] < 105:
                tileTypeImage[yAxis][xAxis] = stone
            elif currentSliceBGRMean[0] > 62 and currentSliceBGRMean[0] < 67 and currentSliceBGRMean[1] > 105 and currentSliceBGRMean[1] < 110 and currentSliceBGRMean[2] > 120 and currentSliceBGRMean[2] < 125:
                tileTypeImage[yAxis][xAxis] = wasteland
    print("These are the location of all tile types: "+str(tileTypeImage))
    return tileTypeImage

def defineCrowns(slices):
    """
       :param slices:
       :return:
       Denne funktion giver et passende ID (crown count) til hvert slice, baseret på hvilket BGR threshold slicet passer ind i.
       """
    yAxis = -1
    xAxis = -1
    for y in slices:
        yAxis += 1
        if yAxis == 5:
            yAxis = 0
        for x in y:
            xAxis += 1
            if xAxis == 5:
                xAxis = 0
            currentSliceBGRMean = findMeanBGR(x)
            if currentSliceBGRMean[0] > 109 and currentSliceBGRMean[0] < 116 and currentSliceBGRMean[1] > 80 and currentSliceBGRMean[1] < 83 and currentSliceBGRMean[2] > 43 and currentSliceBGRMean[2] < 50:
                crownImage[yAxis][xAxis] = oneCrown
            elif currentSliceBGRMean[0] > 16 and currentSliceBGRMean[0] < 18 and currentSliceBGRMean[1] > 145 and currentSliceBGRMean[1] < 147 and currentSliceBGRMean[2] > 170 and currentSliceBGRMean[2] < 173:
                crownImage[yAxis][xAxis] = oneCrown
            elif currentSliceBGRMean[0] > 27 and currentSliceBGRMean[0] < 30 and currentSliceBGRMean[1] > 119 and currentSliceBGRMean[1] < 122 and currentSliceBGRMean[2] > 111 and currentSliceBGRMean[2] < 114:
                crownImage[yAxis][xAxis] = twoCrowns
            elif currentSliceBGRMean[0] > 28 and currentSliceBGRMean[0] < 29 and currentSliceBGRMean[1] > 62 and currentSliceBGRMean[1] < 66 and currentSliceBGRMean[2] > 60 and currentSliceBGRMean[2] < 61:
                crownImage[yAxis][xAxis] = oneCrown
    print("These are the locations of crowns: "+str(crownImage))
    return(crownImage)

# Denne funktion tjekker efter en bestemt type tile og hvor mange af samme type der er ved siden af hinanden.
# Efterfølgende tjekker den hvor mange kroner der er i den givne blob.
# Til sidst ganger den mængden af tiles i en blob og mængden af kroner i den samme blob sammen og leder videre i billedet efter andre blobs.
def checkForConnectivity(tileTypeImage, crownImage, tileType):
    """
    :param tileTypeImage:
    :param crownImage:
    :param tileType:
    :return:
    Denne funktion checker efter en bestemt type tile og hver mange sammenhængende der er af disse.
    Funktion tjekker også for ikke sammenhængende blobs.
    Efterfølgende, tjekker funktionen hvilken mængde kroner der er i en given blob.
    Så bliver mængden af tiles og mængden crowns i en blob ganget sammen for at finde frem til blobbens score.
    Til sidst bliver alle blobsenes scorer lagt sammen og den samlede score for den givne tile type bliver returnet.
    """
    hitCoordinates = deque()
    burnQueue = deque()
    score = 0
    tileCount = 0
    crownCount = 0

    for y, row in enumerate(tileTypeImage):
        for x, pixel in enumerate(row):
            if tileTypeImage[y, x] == tileType:
                burnQueue.append((y,x))
                hitCoordinates.append((y,x))

            while burnQueue:
                tileCount+=1
                current_coordinate = burnQueue.pop()
                y,x = current_coordinate
                if tileTypeImage[y, x] == tileType:
                    tileTypeImage[y, x] = 69

                if x + 1 < tileTypeImage.shape[1] and tileTypeImage[y, x + 1] == tileType and (y, x + 1) not in hitCoordinates:
                    burnQueue.append((y, x + 1))
                    hitCoordinates.append((y, x+1))
                    tileTypeImage[y, x + 1] = 69
                if y + 1 < tileTypeImage.shape[0] and tileTypeImage[y + 1, x] == tileType and (y + 1, x) not in hitCoordinates:
                    burnQueue.append((y + 1, x))
                    hitCoordinates.append((y+1, x))
                    tileTypeImage[y + 1, x] = 69
                if x - 1 >= 0 and tileTypeImage[y, x - 1] == tileType and (y, x - 1) not in hitCoordinates:
                    burnQueue.append((y, x - 1))
                    hitCoordinates.append((y, x-1))
                    tileTypeImage[y, x - 1] = 69
                if y - 1 >= 0 and tileTypeImage[y - 1, x] == tileType and (y - 1, x) not in hitCoordinates:
                    burnQueue.append((y - 1, x))
                    hitCoordinates.append((y-1, x))
                    tileTypeImage[y - 1, x] = 69

                if not burnQueue:
                    """
                    Når koden når hertil, betyder det at vi har fundet en blob af den type tiles som vi leder efter.
                    Mængden af tiles i den blob er givet ved variablen "tileCount".
                    Koordinaterne af de enkelte tiles er givet ved elementerne i "hitCoordinates" dequet.
                    Vi skal nu bruges koordinaterne i "hitCoordinates" til at finde ud af hvor mange kroner der er i denne blob.
                    """
                    for coord in hitCoordinates:
                        if crownImage[coord] == 1:
                            crownCount+=1
                        elif crownImage[coord] == 2:
                            crownCount+=2
                    currentBlobScore = tileCount*crownCount
                    score += currentBlobScore
                    return score
                    hitCoordinates.clear()

"""
Funktionskald forklaret i punktform:
1. Vi skærer vores game board billede ud i 25 slices.
2. Vi definerer hvor de forskellige tiles er og lægger det passende ID ind i vores tileTypeImage.
3. Vi definerer hvor mange kroner der er på hvert slice og giver et passende ID i vores crownImage herefter.
4. Vi finder scoren for alle individuelle typer af tile types (ocean, desert, field, forest, stone og wasteland)
5. Vi lægger disse score sammen og printer den samlede score.
"""
slices = sliceImage(inputImage)
tileTypeImage = defineTileTypes(slices)
crownImage = defineCrowns(slices)
oceanScore = checkForConnectivity(tileTypeImage,crownImage,1)
print("The combined score for ocean tiles is: "+str(oceanScore))
desertScore = checkForConnectivity(tileTypeImage,crownImage,2)
print("The combined score for desert tiles is: "+str(desertScore))
fieldScore = checkForConnectivity(tileTypeImage,crownImage,3)
print("The combined score for field tiles is: "+str(fieldScore))
forestScore = checkForConnectivity(tileTypeImage,crownImage,4)
print("The combined score for forest tiles is: "+str(forestScore))
stoneScore = checkForConnectivity(tileTypeImage,crownImage,5)
print("The combined score for stone tiles is: "+str(stoneScore))
wastelandScore = checkForConnectivity(tileTypeImage,crownImage,6)
print("The combined score for wasteland tiles is: "+str(wastelandScore))
totalScore = oceanScore+desertScore+fieldScore+forestScore+stoneScore+wastelandScore
print("The total score for this game board is: "+str(totalScore))

