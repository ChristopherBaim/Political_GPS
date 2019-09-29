####Methods Only. For Import into main 
import csv
import math
import time

class Polygon:
    X = 0
    Y = 0
    ShapeID = -1
    FEDUID = 0
    Distance = -1
    Name = "null"
    Nodes = []
    Winner = "null"
    Province = "null"

####Read in all Shape data. Could probably turn into method for both Ring/Non-Ring    
def readData(Shapes,File):   
    with open(File, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        firstRow = True
        currentShape = 'none'
        tempNodes = []
        
        for row in readCSV:
            if firstRow:
                firstRow = False
                
                TempP = Polygon()
                
                TempP.ShapeID = row[0]
                TempP.Name = row[3]
                TempP.FEDUID = row[4]
                TempP.Province= row[5]
                TempP.Winner = row[6]
                TempP.X = float(row[8])
                TempP.Y = float(row[7])
                tempNodes.append((float(row[2]),float(row[1])))
                currentShape = row[0]
                
                #print("first Row")
            elif row[0] == currentShape:        
                TempP = Polygon()
                
                TempP.ShapeID = row[0]
                TempP.Name = row[3]
                TempP.FEDUID = row[4]
                TempP.Province= row[5]
                TempP.Winner = row[6]
                TempP.X = float(row[8])
                TempP.Y = float(row[7])
                tempNodes.append((float(row[2]),float(row[1])))
                
                #print("working on Shape")
            else:
                TempP.Nodes = tempNodes
                Shapes.append(TempP)

                TempP = Polygon()
                tempNodes = []
                
                TempP.ShapeID = row[0]
                TempP.Name = row[3]
                TempP.FEDUID = row[4]
                TempP.Province= row[5]
                TempP.Winner = row[6]
                TempP.X = float(row[8])
                TempP.Y = float(row[7])
                tempNodes.append((float(row[2]),float(row[1])))
                currentShape = row[0]

                #print("Starting new shape")

        TempP.Nodes = tempNodes
        Shapes.append(TempP)
                            
####Check if points (x,y) are within given array [points]
def inside_region(x, y, points):
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

###Calculates distance of a shapes centroid from a given coordinate (to become GPS values)   
def calcDistance(Lat, Lon, Shapes):
    for i in range (0,len(Shapes)):
        xDif = abs(Shapes[i].X - Lat)
        yDif = abs(Shapes[i].Y - Lon)
        dist = math.sqrt((xDif ** 2)+(yDif ** 2))
        Shapes[i].Distance = dist


def findRiding(NonRingShapes, RingShapes, Lat, Lon):
    found = False
    for i in range(0,len(RingShapes)):
        #print("looking")
        if(inside_region(Lat, Lon, RingShapes[i].Nodes)):
            Name = RingShapes[i].Name + "RING"
            Winner = RingShapes[i].Winner + "RING"
            found = True
            #print(Name)
            #print(Winner)
            return(Name, Winner)
    if(found == False):        
        for i in range(0,len(NonRingShapes)):
            if(inside_region(Lat, Lon, NonRingShapes[i].Nodes)):
                Name = NonRingShapes[i].Name
                Winner = NonRingShapes[i].Winner
                return(Name, Winner)
                break
##
##NonRingShapes = []
##RingShapes = []
##
##TestX = 45.1
##TestY = -73.1
##
##readData(NonRingShapes, 'Non-Rings.csv')
##readData(RingShapes, 'Rings.csv')
##
##calcDistance(TestX, TestY, NonRingShapes)
##calcDistance(TestX, TestY, RingShapes)
##
##NonRingShapes = sorted(NonRingShapes, key=lambda Shapes: Shapes.Distance)
##RingShapes = sorted(RingShapes, key=lambda Shapes: Shapes.Distance)
##
##for i in range(0,len(NonRingShapes)):
##    print(NonRingShapes[i].Name)
##
##findRiding(NonRingShapes, RingShapes, TestX, TestY)
##
