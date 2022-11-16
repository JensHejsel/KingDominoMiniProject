import cv2 as cv
import numpy as np
from collections import deque

# billedet vi tager udgangspunkt i:
inputImage = cv.imread("4.jpg")

# et billede af sorte pixels:
pixelImage = np.array([[0,0,0,0,0],
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

# Vi skærer billedet ud i 25 slices og gemmer disse i et array.
def sliceImage(img):
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
    meanBGRRow = np.average(img,axis=0)
    meanBGR = np.average(meanBGRRow,axis=0)
    return meanBGR

# Denne funktion finder ud hvad hvert slice er for en type og ændrer placeringen i vores 0-image til det givne ID.
def defineSlices(slices):
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
                pixelImage[yAxis][xAxis] = ocean
            elif currentSliceBGRMean[0] > 4 and currentSliceBGRMean[0] < 18 and currentSliceBGRMean[1] > 145 and currentSliceBGRMean[1] < 169 and currentSliceBGRMean[2] > 170 and currentSliceBGRMean[2] < 192:
                pixelImage[yAxis][xAxis] = desert
            elif currentSliceBGRMean[0] > 28 and currentSliceBGRMean[0] < 34 and currentSliceBGRMean[1] > 119 and currentSliceBGRMean[1] < 143 and currentSliceBGRMean[2] > 93 and currentSliceBGRMean[2] < 113:
                pixelImage[yAxis][xAxis] = field
            elif currentSliceBGRMean[0] > 28 and currentSliceBGRMean[0] < 30 and currentSliceBGRMean[1] > 62 and currentSliceBGRMean[1] < 67 and currentSliceBGRMean[2] > 59 and currentSliceBGRMean[2] < 62:
                pixelImage[yAxis][xAxis] = forest
            elif currentSliceBGRMean[0] > 100 and currentSliceBGRMean[0] < 105 and currentSliceBGRMean[1] > 110 and currentSliceBGRMean[1] < 115 and currentSliceBGRMean[2] > 100 and currentSliceBGRMean[2] < 105:
                pixelImage[yAxis][xAxis] = stone
            elif currentSliceBGRMean[0] > 62 and currentSliceBGRMean[0] < 67 and currentSliceBGRMean[1] > 105 and currentSliceBGRMean[1] < 110 and currentSliceBGRMean[2] > 120 and currentSliceBGRMean[2] < 125:
                pixelImage[yAxis][xAxis] = wasteland
    print(pixelImage)
    return pixelImage


# Denne funktion tjekker efter en bestemt type tile og hvor mange af samme type der er ved siden af hinanden.
# Efterfølgende tjekker den hvor mange kroner der er i den givne blob.
# Til sidst ganger den mængden af tiles i en blob og mængden af kroner i den samme blob sammen og leder videre i billedet efter andre blobs.
def checkForConnectivity(image, coordinate, tileType):
    y, x = coordinate
    hitCoordinates = deque()
    burnQueue = deque()
    count = 0

    if image[y, x] == tileType:
        burnQueue.append((y,x))
        hitCoordinates.append((y,x))

    while burnQueue:
        current_coordinate = burnQueue.pop()
        y,x = current_coordinate
        if image[y,x] == tileType:
            count+=1

        if x + 1 < image.shape[1] and image[y, x + 1] == tileType and (y, x + 1) not in hitCoordinates:
            burnQueue.append((y, x + 1))
            hitCoordinates.append((y, x+1))
            image[y, x + 1] = 69
            count+=1
        if y + 1 < image.shape[0] and image[y + 1, x] == tileType and (y + 1, x) not in hitCoordinates:
            burnQueue.append((y + 1, x))
            hitCoordinates.append((y+1, x))
            image[y + 1, x] = 69
            count+=1
        if x - 1 >= 0 and image[y, x - 1] == tileType and (y, x - 1) not in hitCoordinates:
            burnQueue.append((y, x - 1))
            hitCoordinates.append((y, x-1))
            image[y, x - 1] = 69
            count+=1
        if y - 1 >= 0 and image[y - 1, x] == tileType and (y - 1, x) not in hitCoordinates:
            burnQueue.append((y - 1, x))
            hitCoordinates.append((y-1, x))
            image[y - 1, x] = 69
            count+=1

        if not burnQueue:
            """
            Når koden når hertil, betyder det at vi har fundet en blob af den type tiles som vi leder efter.
            Mængden af tiles i den blob er givet ved variablen "count".
            Koordinaterne af de enkelte tiles er givet ved elementerne i "hitCoordinates" dequet.
            Vi skal nu bruges koordinaterne i "hitCoordinates" til at finde ud af hvor mange kroner der er i denne blob.
            """

            print(hitCoordinates)
            hitCoordinates.clear()
            print(count)

    return count

# Denne funktion kører vores checkForConnectivity funktion på vores billede.
def grassfire(image, tileType):
    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            checkForConnectivity(pixelImage, (y, x), tileType)

slices = sliceImage(inputImage)
definedSlices = defineSlices(slices)
connectivityCount = grassfire(pixelImage, 1)
BGRMean = findMeanBGR(slices[2][0])
print(BGRMean)

cv.imshow("slice", inputImage)
cv.waitKey(0)

