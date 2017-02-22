'''
Created on Nov 5, 2015

@author: Zhongyi Yan
'''
import os
from pickle import FALSE

class Polygon(object):
    def __init__(self):
        self.sideNum = 0
        self.originXY = []
        self.currentXY = []
        self.xMove = 0
        self.yMove = 0
        
    def CopyInital( self, polygonInput ):
        self.sideNum = int(polygonInput[0])
        if self.sideNum < 3:
            print("invalid input file")
            exit()
        for i in range( 1, self.sideNum * 2, 2 ) :
            self.originXY.append( ( polygonInput[i], polygonInput[i+1] ) )
        self.currentXY = self.originXY
        self.xMove = polygonInput[i+2]
        self.yMove = polygonInput[i+3]
        #print( self.sideNum )
        #print( self.xy )
        #print( self.xMove, self.yMove )
        
    def addPoint(self, newX, newY):
        if self.sideNum == 0:
            self.sideNum += 1
            newPoint = ( newX, newY )
            self.currentXY.append( newPoint )
        else:
            thisLen = len( self.currentXY )
            isExist = False
            for i in range( thisLen ):
                if self.currentXY[i][0] == newX and self.currentXY[i][1] == newY:
                    isExist = True
            if not isExist:
                self.sideNum += 1
                newPoint = ( newX, newY )
                self.currentXY.append( newPoint )
                
    def Sort(self):
        thisLen = len( self.currentXY )
        if thisLen == 0:
            return
        x, y = 0, 0
        for i in range(thisLen):
            x += self.currentXY[i][0]
            y += self.currentXY[i][1]
        center = ( x / thisLen, y / thisLen )
        for i in range(thisLen - 1):
            for j in range(thisLen - i - 1):
                if self.IsCount( self.currentXY[j], self.currentXY[j+1], center ):
                    tmpP = self.currentXY[j]
                    self.currentXY[j] = self.currentXY[j+1]
                    self.currentXY[j+1] = tmpP
                
        
    def IsCount(self, a, b, c):
        if a[0] >= 0  and b[0] < 0:
            return True
        if a[0] == 0  and b[0] == 0:
            return a[1] > b[1]
        det = ( a[0] - c[0] ) * ( b[1] - c[1] ) - ( b[0] - c[0] ) * ( a[1] - c[1] )
        if det < 0:
            return True
        if det > 0:
            return False
        d1 = ( a[0] - c[0] )**2 + ( a[1] - c[1] )**2
        d2 = ( b[0] - c[0] )**2 + ( b[1] - c[1] )**2
        return d1 > d2
    
    
    def isEmpty(self):
        if self.sideNum == 0:
            return True
        else:
            return False
        
    def Move(self, mInc):
        thisLen = len( self.currentXY )
        for i in range( thisLen ):
            x, y = self.currentXY[i]
            x += ( self.xMove * mInc )
            y += ( self.yMove * mInc )
            self.currentXY[i] = x, y
        #print( self.currentXY )
     
    def Vertex(self, p2, p3):
        p2Len = len( p2.currentXY )
        p1Len = len( self.currentXY )
        for i in range( p2Len ):
            p2x, p2y = p2.currentXY[i]
            nCross = 0
            for j in range( p1Len ):
                k = ( j + 1 ) % p1Len
                p1x1, p1y1 = self.currentXY[j]
                p1x2, p1y2 = self.currentXY[k]
                if p1x2 == p1x1:
                    p1Slope = 1
                else:
                    p1Slope = ( p1y2 - p1y1 ) / ( p1x2 - p1x1 )
                    
                p1Offset = p1y2 - ( p1Slope * p1x2 )
                if( p2x * p1Slope + p1Offset ) == p2y:
                    if p2x >= min( p1x1, p1x2 ) and p2x <= max( p1x1, p1x2 ):
                        p3.addPoint( p2x, p2y )
                        break
                    else:
                        continue
                else:
                    if p1y1 == p1y2:
                        continue
                    if p2y < min( p1y1, p1y2 ):
                        continue
                    if p2y >= max( p1y1, p1y2 ):
                        continue
                    x = (p2y - p1y1) * (p1x2 - p1x1) / (p1y2 - p1y1) + p1x1
                    if x > p2x:
                        nCross += 1
            if ( nCross % 2 ) == 1:
                p3.addPoint( p2x, p2y )

    
    def Intersection(self, p2, p3):
        p1Len = len( self.currentXY )
        p2Len = len( p2.currentXY )
        for i in range( p1Len ):
            j = ( i + 1 ) % p1Len
            p1x1, p1y1 = self.currentXY[i]
            p1x2, p1y2 = self.currentXY[j]
            if p1x1 > p1x2:
                rightP1x = p1x1
                leftP1x = p1x2
            else:
                rightP1x = p1x2
                leftP1x = p1x1
            if p1y1 > p1y2:
                upP1y = p1y1
                downP1y = p1y2
            else:
                upP1y = p1y2
                downP1y = p1y1
            if p1x2 == p1x1:
                p1Slope = 1
            else:
                p1Slope = ( p1y2 - p1y1 ) / ( p1x2 - p1x1 )
            p1Offset = p1y2 - ( p1Slope * p1x2 )
            for m in range( p2Len ):
                n = ( m + 1 ) % p2Len
                p2x1, p2y1 = p2.currentXY[m]
                p2x2, p2y2 = p2.currentXY[n]
                if p2x1 > p2x2:
                    rightP2x = p2x1
                    leftP2x = p2x2
                else:
                    rightP2x = p2x2
                    leftP2x = p2x1
                if p2y1 > p2y2:
                    upP2y = p2y1
                    downP2y = p2y2
                else:
                    upP2y = p2y2
                    downP2y = p2y1
                    
                if p2x2 == p2x1:
                    p2Slope = 1
                else:
                    p2Slope = ( p2y2 - p2y1 ) / ( p2x2 - p2x1 )
                p2Offset = p2y2 - ( p2Slope * p2x2 )
                if p1Slope == p2Slope:
                    if p1Offset == p2Offset:
                        if p1Slope == 0:
                            if p1x1 <= max( p2x1, p2x2 ) and p1x1 >= min( p2x1, p2x2 ):
                                p3.addPoint( p1x1, p1y1 )
                            if p1x2 <= max( p2x1, p2x2 ) and p1x2 >= min( p2x1, p2x2 ):
                                p3.addPoint( p1x2, p1y2 )
                            if p2x1 <= max( p1x1, p1x2 ) and p2x1 >= min( p1x1, p1x2 ):
                                p3.addPoint( p2x1, p2y1 )
                            if p2x2 <= max( p1x1, p1x2 ) and p2x2 >= min( p1x1, p1x2 ):
                                p3.addPoint( p2x2, p2y2 )
                        else:
                            if p1y1 <= max( p2y1, p2y2 ) and p1y1 >= min( p2y1, p2y2 ):
                                p3.addPoint( p1x1, p1y1 )
                            if p1y2 <= max( p2y1, p2y2 ) and p1y1 >= min( p2y1, p2y2 ):
                                p3.addPoint( p1x2, p1y2 )
                            if p2y1 <= max( p1y1, p1y2 ) and p2y1 >= min( p1y1, p1y2 ):
                                p3.addPoint( p2x1, p2y1 )
                            if p2y2 <= max( p1y1, p1y2 ) and p2y2 >= min( p1y1, p1y2 ):
                                p3.addPoint( p2x2, p2y2 )
                    else:
                        continue
                else: 
                    newX = ( p2Offset - p1Offset ) / ( p1Slope - p2Slope )
                    newY = newX * p2Slope + p2Offset
                    if newX <= rightP1x and newX >= leftP1x and newX <= rightP2x and newX >= leftP2x and newY <= upP1y and newY >= downP1y and newY <= upP2y and newY >= downP2y:
                        p3.addPoint( newX, newY )
     
    def CalArea(self):           
        if self.sideNum < 3:
            return 0
        else:
            area = 0
            thisLen = len( self.currentXY )
            for i in range( 0, thisLen ):
                j = (i - 1) % thisLen
                area += self.currentXY[i][0] * self.currentXY[i-1][1] - self.currentXY[i][1] * self.currentXY[i-1][0]
            return abs( area / 2 )
    
        
if os.path.exists('input.dat'):
    fileIn = open( 'input.dat' , 'r' )
    fileOut = open( 'output.dat', 'w+' )
    lineCount = 0
    polygon1 = Polygon()
    polygon2 = Polygon()
    for line in fileIn:
        polygonInput = list( map( int, line.split(' ') ) )
        print( polygonInput )
        if lineCount == 0:
            polygon1.CopyInital(polygonInput)
        elif lineCount == 1:
            polygon2.CopyInital(polygonInput)
        else:
            print("invalid input file")
            exit()
        lineCount += 1
    cutCount = 0

    firstTouchTime = 0
    maxTime = 0
    tmpArea = 0
    movingTM = 0
    movinginc = 0.00005
    #movinginc = 0.1
    polygon1.CalArea()
    #print(polygon1.CalArea(), "   ", polygon2.CalArea() )
    while movingTM < 10:
         
        polygon1.Move(movinginc)
        polygon2.Move(movinginc)
        #print( polygon1.currentXY, "   ", polygon2.currentXY )
        
        polygonTmp = Polygon()
        polygon1.Vertex(polygon2, polygonTmp)
        polygon2.Vertex(polygon1, polygonTmp)
        polygon1.Intersection(polygon2, polygonTmp)
        #print( polygonTmp.currentXY )
        polygonTmp.Sort()
        if firstTouchTime == 0 and not polygonTmp.isEmpty():
            firstTouchTime = movingTM
        currentArea = polygonTmp.CalArea()
        #print( currentArea )
        if currentArea > tmpArea:
            tmpArea = currentArea
            maxTime = movingTM
        movingTM += movinginc
        
    if  tmpArea != 0:
        #print( tmpArea,"     ",  maxTime )
        fileOut.write( ' maximum area is {0:.6f}, and the time is {1:.6f} '.format(tmpArea, maxTime))
    elif firstTouchTime != 0:
        #print( "first touch time",  firstTouchTime )
        fileOut.write( ' first touch time is{0:.6f}'.format(firstTouchTime))
    else:
        fileOut.write( ' Never')
        #print("Never")
    #fileOut.write('The largest decline is {0:.6f} \n ')
    #print('The largest decline is {0:.6f} ' .format(MaxDec(price)))
else:
    print("input file dosen't exist")
    
    
