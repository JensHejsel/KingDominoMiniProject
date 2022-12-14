# Mini project King Domino
Image Processing miniproject for MED3 at AAU

### Disclaimer:
The program is not perfect and will often find crowns that are not present in the picture, or not find a crown at all. For this reason the scores provided are, sadly, often not accurate. Even if the score is accurate, the found crowns might not be, and vice versa.
Another problem is that the thresholds used, to figure out what tiles are where, are not precise enough, and therefore the program will sometimes recognise the wrong tiles.

## Introduction
The program will take a random provided image, of a finished King Domino game boards, then using image processing it will try to give a score (see used pictures in the "Cropped and Perspective corrected" folder).
This will be done by finding the properties (groups) of the same types of tiles, and multiplying it by the number of crowns located in that property.
The crowns are found by template matching, and the properties are found with thresholding and grouped with grassFire blob detection.

## Group participants 
- Jens Hejselbæk  jenschr21@student.aau.dk  20213478
- Niko Bach Jensen  nbfj2@student.aau.dk  20214224

## Instructions provided for the miniproject
- Make a program that can calculate the final score for the boardgame King Domino.
- The mini project is to be worked on in groups of two.
- There will be provided pictures of game boards. 
- Deadline for hand in: 27/11 2021 kl. 10.00
