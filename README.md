# Mini project King Domino
Image Processing miniproject for MED3 at AAU

### Disclaimer:
The program is not perfect and will often find crowns that are not present in the picture, or not find a crown at all. For this reason the scores provided are, sadly, often not accurate. Even if the score is accurate, the found crowns might not be, and vice versa.

## Introduction
The program will take a random provided image, of a finished King Domino game boards, then using image processing it will try to give a score.
This will be done by finding the properties (groups) of the same types of tiles, and multiplying it by the number of crowns located in that property.
The crowns are found by template matching, and the properties are found with thresholding and grouped with grassFire blob detection.

## Group participants 
- Jens Hejselbæk  jenschr21@student.aau.dk  20213478
- Niko Bach Jensen  nbfj2@student.aau.dk  20214224

## Instructions provided for the miniproject
"King Domino er et brætspil, hvor spillerne bygger små kongeriger af farvede dominobrikker. Vinderen er den, som har flest point når spillet er slut, og pointene afhænger af, hvordan spillerens farvede dominobrikker ligger. I dette miniprojekt skal I udvikle et system, der beregner hvor mange point en given opsætning giver, baseret på et billede af spilleområdet."

- The mini project is to be worked on in groups of two.
- There will be provided pictures of game boards. The provided dataset can be found in the folder "King Domino datasæt".
- Deadline for hand in: 27/11 2021 kl. 10.00
