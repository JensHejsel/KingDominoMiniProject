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

    for row in slices:
        yValue += 1
        if yValue == 6:
            yValue = 1
        for column in row:
            xValue += 1
            if xValue == 6:
                xValue = 1
            if pixelImage[yValue][xValue] == tileType and pixelImage[yValue][xValue] not in adjacentTiles:
                currentPos = [[yValue,xValue]]
                adjacentPixel = []
                adjacentTiles.append([yValue,xValue])
                burnQueue.append([yValue,xValue])
                while len(burnQueue) > 0:
                    print("thisinBQ"+str(burnQueue))
                    print("thisinAT"+str(adjacentTiles))
                    currentPos = [burnQueue.pop()]
                    if pixelImage[yValue][xValue]+1 == tileType and adjacentPixel not in adjacentTiles:
                        print("Igethere")
                        adjacentPixel = currentPos
                        adjacentPixel[0][1] = adjacentPixel[0][1]+1
                        adjacentTiles.append(adjacentPixel)
                        burnQueue.append(adjacentPixel)

                    if pixelImage[yValue][xValue] == tileType:
                        print("igethere")
                        adjacentPixel = currentPos
                        adjacentPixel[0][0] = adjacentPixel[0][0]+1
                        adjacentTiles.append(adjacentPixel[0].copy())
                        burnQueue.append(adjacentPixel[0])

                    if pixelImage[currentPos[0][0]][currentPos[0][1]-1] == tileType and adjacentPixel not in adjacentTiles:
                        adjacentPixel = currentPos
                        adjacentPixel[0][1] = adjacentPixel[0][1]-1
                        adjacentTiles.append(adjacentPixel)
                        burnQueue.append(adjacentPixel)

                    if pixelImage[currentPos[0][0]-1][currentPos[0][1]] == tileType and adjacentPixel not in adjacentTiles:
                        adjacentPixel = currentPos
                        adjacentPixel[0][0] = adjacentPixel[0][0]-1
                        adjacentTiles.append(adjacentPixel)
                        burnQueue.append(adjacentPixel)

    print("These are the coordinates for adjacent tiles"+str(adjacentTiles))
    return pixelImage




wig = checkForConnectivity(1)
meanRGB = findMeanBGR(slices[3][3])
cv.imshow("slice", slices[0][2])
cv.waitKey(0)

