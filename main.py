import cv2 as cv
import numpy as np
from collections import deque

inputImage = cv.imread("4.jpg")
pixelImage = np.array([[0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0]])
ocean = 1
desert = 2
field = 3
forest = 4
stone = 5
wasteland = 6

def sliceImage(img):
    slices = []
    for y in range(0,img.shape[0],int(img.shape[0]/5)):
        horizontalSlices = []
        for x in range(0,img.shape[1],int(img.shape[1]/5)):
            slice = img[y: y+int(img.shape[0]/5), x: x+int(img.shape[1]/5)]
            horizontalSlices.append(slice)
        slices.append(horizontalSlices)
    return slices

def findMeanBGR(img):
    meanBGRRow = np.average(img,axis=0)
    meanBGR = np.average(meanBGRRow,axis=0)
    return meanBGR

slices = sliceImage(inputImage)

def defineSlices():
    sliceY = -1
    sliceX = -1
    indexY = 0
    indexX = 0
    for y in slices:
        indexY+=1
        sliceY+=1
        if sliceY == 5:
            sliceY = 0
            indexY = 1
        for x in y:
            indexX+=1
            sliceX += 1
            if sliceX == 5:
                sliceX = 0
                indexX = 1
            currentSliceBGRMean = findMeanBGR(slices[sliceY][sliceX])
            if currentSliceBGRMean[0] > 108 and currentSliceBGRMean[0] < 163 and currentSliceBGRMean[1] > 77 and currentSliceBGRMean[1] < 87 and currentSliceBGRMean[2] > 4 and currentSliceBGRMean[2] < 50:
                pixelImage[indexY][indexX] = ocean
            elif currentSliceBGRMean[0] > 4 and currentSliceBGRMean[0] < 18 and currentSliceBGRMean[1] > 145 and currentSliceBGRMean[1] < 169 and currentSliceBGRMean[2] > 170 and currentSliceBGRMean[2] < 192:
                pixelImage[indexY][indexX] = desert
            elif currentSliceBGRMean[0] > 28 and currentSliceBGRMean[0] < 34 and currentSliceBGRMean[1] > 119 and currentSliceBGRMean[1] < 143 and currentSliceBGRMean[2] > 93 and currentSliceBGRMean[2] < 113:
                pixelImage[indexY][indexX] = field
            elif currentSliceBGRMean[0] > 28 and currentSliceBGRMean[0] < 30 and currentSliceBGRMean[1] > 62 and currentSliceBGRMean[1] < 67 and currentSliceBGRMean[2] > 59 and currentSliceBGRMean[2] < 62:
                pixelImage[indexY][indexX] = forest
            elif currentSliceBGRMean[0] > 100 and currentSliceBGRMean[0] < 105 and currentSliceBGRMean[1] > 110 and currentSliceBGRMean[1] < 115 and currentSliceBGRMean[2] > 100 and currentSliceBGRMean[2] < 105:
                pixelImage[indexY][indexX] = stone
            elif currentSliceBGRMean[0] > 62 and currentSliceBGRMean[0] < 67 and currentSliceBGRMean[1] > 105 and currentSliceBGRMean[1] < 110 and currentSliceBGRMean[2] > 120 and currentSliceBGRMean[2] < 125:
                pixelImage[indexY][indexX] = wasteland
    print(pixelImage)
    return pixelImage

pixelImage = defineSlices()
adjacentTiles = []

def checkForConnectivity(tileType):
    yValue = 0
    xValue = 0
    burnQueue = []
    adjacentTiles.clear()
    for row in slices:
        yValue += 1
        if yValue == 6:
            yValue = 1
        for column in row:
            xValue += 1
            if xValue == 6:
                xValue = 1
            if pixelImage[yValue][xValue] == tileType:
                currentPos = [[yValue,xValue]]
                adjacentPixel = []
                adjacentTiles.append([yValue,xValue])
                burnQueue.append([yValue,xValue])
                while burnQueue:
                    currentPos = [burnQueue.pop()]
                    rightPixel = pixelImage[yValue][xValue + 1]
                    belowPixel = pixelImage[yValue + 1][xValue]
                    leftPixel = pixelImage[yValue][xValue - 1]
                    abovePixel = pixelImage[yValue - 1][xValue]
                    if rightPixel == tileType and adjacentPixel not in adjacentTiles:
                        hitCord = [yValue, xValue+1]
                        burnQueue.append(hitCord)
                        adjacentTiles.append(hitCord)

                    if belowPixel == tileType and adjacentPixel not in adjacentTiles:
                        currentPos[0][0] +=1
                        print(currentPos[0][0])
                        hitCord = currentPos
                        print(hitCord)
                        burnQueue.append(hitCord)
                        adjacentTiles.append(hitCord)

                    if leftPixel == tileType and adjacentPixel not in adjacentTiles:
                        hitCord = [yValue, xValue-1]
                        burnQueue.append(hitCord)
                        adjacentTiles.append(hitCord)

                    if abovePixel == tileType and adjacentPixel not in adjacentTiles:
                        hitCord = [yValue-1, xValue]
                        burnQueue.append(hitCord)
                        adjacentTiles.append(hitCord)

    print("Adjacent tiles for value "+str(tileType)+" are at the coordinates:"+str(adjacentTiles))
    return pixelImage



adjacentOceanTiles = checkForConnectivity(1)
adjacentDesertTiles = checkForConnectivity(2)
adjacentFieldTiles = checkForConnectivity(3)
adjacentForestTiles = checkForConnectivity(4)
adjacentStoneTiles = checkForConnectivity(5)
adjacentWastelandTiles = checkForConnectivity(6)

cv.imshow("slice", inputImage)
cv.waitKey(0)

