from cmu_graphics import *
import copy, random, math


def onAppStart(app):
    app.rows = 10
    app.cols = 10
    app.boardLeft = 250
    app.boardTop = 30
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.colorList = ['green', 'orange', 'gold', 'red', 'lime', 'blue', 'lightcoral', 'purple', 'brown', 'grey', 'pink', 'maroon']
    app.polynomials = [ ] 
    app.rectColorOne = 'white'
    app.clickedButton = 0 # Zero if no button is selected; 1, 2, 3, 4, or 5 if that button is currently selected
    app.currPoly = ''
    app.clickedTwoString = '5'
    app.clickedThreeString = '-5'
    app.clickedFourString = '-5'
    app.clickedFiveString = '5'
    app.parameters = Graph(5, 5, 5, 5)
    app.isDrawn = False
    app.validPoly = False
    app.origin = [400, 180]
    colorApp(app)
    
def colorApp(app):
    app.color = rgb(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    
    
def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    Polynomials(app)
    drawLabels(app)
    if app.parameters.maxX - app.parameters.minX != 0:
        drawLine(225, 180 + 1/2*(app.boardHeight/(app.parameters.maxX + app.parameters.minX)) * (app.parameters.maxX - app.parameters.minX) , 575, 180 + 1/2*(app.boardHeight/(app.parameters.maxX + app.parameters.minX)) * (app.parameters.maxX - app.parameters.minX), lineWidth = 3, fill = 'black', arrowStart=True, arrowEnd=True)
    else:
        drawLine(225, 180, 575, 180, lineWidth = 3, fill = 'black', arrowStart=True, arrowEnd=True)
    
    if app.parameters.maxY - app.parameters.minY != 0:
        drawLine(400 - 1/2*(app.boardWidth/(app.parameters.maxY + app.parameters.minY)) * (app.parameters.maxY - app.parameters.minY), 5, 400 - 1/2*(app.boardWidth/(app.parameters.maxY + app.parameters.minY)) * (app.parameters.maxY - app.parameters.minY), 355, lineWidth = 3, fill = 'black', arrowStart=True, arrowEnd=True )
    else:
        drawLine(400, 5, 400, 355, lineWidth = 3, fill = 'black', arrowStart=True, arrowEnd=True)
        
        
def drawLabels(app):
    drawLabel('GraphApp', 110, 50, size = 30)
    drawLabel('Enter a polynomial', 110, 100)
    drawLabel('in the form ax^n', 110, 120)
    if app.clickedButton != 1:
        color1 = 'white'
    else:
        color1 = 'lightgrey'
    drawRect(45, 150, 130, 30, fill = color1, border = 'black')
    drawRect(60, 355, 100, 20, fill = 'white', border = 'black')
    drawLabel('Clear All', 110, 365)
    drawLabel('max y', 223, 25)
    drawLabel('min y', 223, 335)
    drawLabel('min x', 263, 380)
    drawLabel('max x', 538, 380)
    drawLabel('Reset Axes', 400, 380)
    drawLabel(f'{app.currPoly}', 110, 165)
    
    if app.clickedButton != 2:
        color2 = 'white'
    else:
        color2 = 'lightgrey'
    drawRect(210, 30, 25, 20, fill = color2, border = 'black')
    
    if app.clickedButton != 3:
        color3 = 'white'
    else:
        color3 = 'lightgrey'
    drawRect(210, 310, 25, 20, fill = color3, border = 'black')
    
    if app.clickedButton != 4:
        color4 = 'white'
    else:
        color4 = 'lightgrey'
    drawRect(250, 355, 25, 20, fill = color4, border = 'black')
    
    if app.clickedButton != 5:
        color5 = 'white'
    else:
        color5 = 'lightgrey'
    drawRect(525, 355, 25, 20, fill = color5, border = 'black')
    drawRect(365, 370, 70, 20, fill = None, border = 'black')
    
    numHorizontalLines = (app.parameters.minX + app.parameters.maxX)
    numVerticalLines = (app.parameters.minY + app.parameters.maxY)
    constX = app.boardHeight / numHorizontalLines
    constY = app.boardWidth / numVerticalLines
    
    for i in range(1, app.parameters.maxX):
        drawLabel(f'{app.parameters.maxX - i}', 240, app.boardTop + (constX * i))
        
    for i in range(app.parameters.maxX, app.parameters.maxX + app.parameters.minX):
        if app.parameters.maxX - i != 0: 
            drawLabel(f'{app.parameters.maxX - i}', 240, app.boardTop + (constX * i))
    
    for i in range(1, app.parameters.minY):
        drawLabel(f'{-(app.parameters.minY - i)}', app.boardLeft + (constY * i), 340)
        
    for i in range(app.parameters.minY, app.parameters.maxY + app.parameters.minY):
        if app.parameters.minY - i != 0:
            drawLabel(f'{-(app.parameters.minY - i)}', app.boardLeft + (constY * i), 340)
    
    drawLabel(f'{app.clickedTwoString}', 223, 40)
    drawLabel(f'{app.clickedThreeString}', 223, 320)
    drawLabel(f'{app.clickedFiveString}', 538, 365)
    drawLabel(f'{app.clickedFourString}', 263, 365)
    
    if app.isDrawn == True:
        for i in range(len(app.polynomials)):
            drawLabel(f'{app.polynomials[i]}', 110, 200 + 20*i, size = 16, fill = app.colorList[i % len(app.colorList)])
 
    
    
class Graph:
    def __init__(self, maxY, maxX, minX, minY):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
            
def drawBoard(app):
    for row in range(app.parameters.maxX + app.parameters.minX):
        for col in range(app.parameters.maxY + app.parameters.minY):
            drawCell(app, row, col)
    

def drawBoardBorder(app):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, borderWidth = 1, border='black')

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / (app.parameters.minY + app.parameters.maxY)
    cellHeight = app.boardHeight / (app.parameters.minX + app.parameters.maxX)
    return (cellWidth, cellHeight)


def Polynomials(app):
    for i in range(len(app.polynomials)):
        polynomial = app.polynomials[i]
        drawPolynomialPlus(app, polynomial, i)
     
class Polynomial:  # Modified the Polynomial class so that it works for any order of coefficients, ie. [2, 3] == [3, 2]
                                                                            # depending on user input 2x + 3 == 3 + 2x
    def __init__(self, coeffs):
        self.coeffs = coeffs
        self.color = rgb(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))

    def __repr__(self):
        return f'{coefficientsToString(self.coeffs)}'

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return False
        elif (other.coeffs == self.coeffs):
            return True
            

    def __hash__(self):
        return hash(str(self))

    def evalAt(self, x):
        answer = 0
        for i in range(len(self.coeffs)):
            answer += self.coeffs[i] * x ** (len(self.coeffs) - 1 - i)
        return answer
        
    

def insertSpaces(s): # proper format of an input ax^n + bx + c, spaces between operators 
    newS = ''
    for elem in s:
        if elem == '-' or elem == '+':
            newS += ' ' + elem + ' '
        else:
            newS += elem
    if newS != '' and newS[0] == ' ':
        return newS[1:]
    else:
        return newS
    


def getExponent(s): # needed this for making dictionary of degrees
    if len(s) == 3:
        if s[0:2].isdigit():
            return 1
        else:
            return s[2]
    elif len(s) == 4 and '.' not in s:
            return s[3]
    elif len(s) == 5 and '.' not in s:
        return s[4]
    elif len(s) == 6:
        return s[5]
    elif len(s) == 7:
        return s[6]
    elif len(s) == 8:
        return s[7]
    elif len(s) == 9:
        return s[8]
    else:
        return 1

 
def getLargestExponent(s): # needed this for initializing dictionary of degrees
    if 'x' not in s:
        return 0
    elif '^' not in s:
        return 1
    newList = [ ]
    largest = 0
    for elem in s.split('x'):
        if '^' in elem and elem != '^':
            if elem[1].isdigit():
                newList.append(int(elem[1]))
    for num in newList:
        if num > largest:
            largest = num
    return largest
    
def coefficientsToString(coeffs):
    if len(coeffs) == 1:
        return str(coeffs[0])
    else:
        terms = [ ]
        for i in range(len(coeffs)):
            coeff = coeffs[i]
            if (coeff != 0):
                isNegative = (coeff < 0)
                coeff = abs(coeff)
                if (terms != [ ]):
                    terms.append(' - ' if isNegative else ' + ')
                if (terms == [ ]) and isNegative:
                    terms.append('-')
                if ((coeff != 1) or (i == len(coeffs)-1)):
                    terms.append(str(coeff))
                power = len(coeffs)-1-i
                if (power == 1): terms.append('x')
                elif (power > 1): terms.append(f'x**{power}')
        return ''.join(terms)
        
def polyDict(s): # gives me a dictionary with the degree of the element and its coefficient, and returns a list in the necessary order
    s = insertSpaces(s)
    newDict = dict()
    newList = [ ]
    sign = -1
    for i in range((getLargestExponent(s)), -1, -1):
        newDict[f'degree{i}'] = 0
    
    for char in s.split(' '):
        if char == '+':
            sign = -1
        elif char == '-':
            sign = 1
            
        if char != '+' and char != '-':
            if 'x' not in char and char != '':
                newDict['degree0'] = sign * float(char)
            elif 'x' in char:
                if char[0] == 'x':
                    newDict[f'degree{getExponent(char)}'] += sign * float(1)
                else:
                    if '.' in char:
                        newCoeff = FloatCoeff(char)
                        if isFloat(newCoeff):
                            newDict[f'degree{getExponent(char)}'] += sign * float(newCoeff)
                    else:
                        newDict[f'degree{getExponent(char)}'] += sign * float(char[0])
    
    for key in newDict:
        newList.append(newDict[key])
        
    return newList

def isFloat(s):
    if s[len(s) - 1] == '.':
        return False
    if '.' in s:
        for char in s:
            if char == '.':
                continue
            elif not char.isdigit():
                return False
    return True

def FloatCoeff(s):
    newS = ''
    for char in s:
        if char == '^':
            break
        elif char != 'x':
            newS += char
    return newS
    
def drawPolynomialPlus(app, poly, k): # a lot of calculations so it may look overwhelming
    convertString = polyDict(poly) # input string to be turned into list of coefficients 
    polyClassRight = Polynomial(convertString) # use OOP to get me the polynomial in the form of a string 
    convertStringCopy = copy.copy(convertString) # use a copy of the list for the left side of the drawing
    convertStringCopy[-1] = convertStringCopy[-1] 
    polyClassLeft = Polynomial(convertStringCopy) # same here 
    scaleToGridX = app.boardHeight / (app.parameters.maxX + app.parameters.minX)
    scaleToGridY = app.boardHeight / (app.parameters.maxY + app.parameters.minY)
  
    if len(convertString) > 1 and convertString[1] == 0: # specific functions require special drawing conditions 
        polyClassRight = Polynomial(convertString)
        convertStringCopy = copy.copy(convertString)
        convertStringCopy[-1] = - convertStringCopy[-1]
        polyClassLeft = Polynomial(convertStringCopy)
        
        for i in range(0, 280):   
            scale = 4
            n1 = i/10
            n2 = (i+scale-7)/10
            
            evaluatePlusR1 = -1 * polyClassRight.evalAt(n1) 
            evaluateMinusR1 = 1 * polyClassRight.evalAt(n1) 
            evaluatePlusL1 = -1 * polyClassLeft.evalAt(n1) 
            evaluateMinusL1 = 1 * polyClassLeft.evalAt(n1) 
            
            evaluatePlusR2 = -1 * polyClassRight.evalAt(n2) 
            evaluateMinusR2 = 1 * polyClassRight.evalAt(n2) 
            evaluatePlusL2 = -1 * polyClassLeft.evalAt(n2) 
            evaluateMinusL2 = 1 * polyClassLeft.evalAt(n2) 
            
            newOriginX = 180 + 1/2*(scaleToGridX) * (app.parameters.maxX - app.parameters.minX)
            newOriginY = 400 - 1/2*(scaleToGridY) * (app.parameters.maxY - app.parameters.minY)
            
            
            rightX1 = (newOriginY + n1 * scaleToGridY)
            leftX1 = (newOriginY - n1 *  scaleToGridY)
            yOne1 = newOriginX - (-1 * polyClassRight.evalAt(n1)) * scaleToGridX
            yOne2 = newOriginX - (-1 * polyClassRight.evalAt(n1)) *  scaleToGridX
            yMinus1 = newOriginX - (polyClassLeft.evalAt(n1)) * scaleToGridX
            yPlus1 = newOriginX + (polyClassRight.evalAt(n1)) * scaleToGridX
            
            rightX2 = (newOriginY + n2 * scaleToGridY)
            leftX2 = (newOriginY - n2 * scaleToGridY)
            yTwo1 = newOriginX - (-1 * polyClassRight.evalAt(n2)) * scaleToGridX
            yTwo2 = newOriginX - (-1 * polyClassRight.evalAt(n2)) * scaleToGridX
            yMinus2 = newOriginX - (polyClassLeft.evalAt(n2)) * scaleToGridX
            yPlus2 = newOriginX + (1 * polyClassRight.evalAt(n2)) * scaleToGridX
            
            if (250 <= rightX1 <= 550 and 30 <= yOne1 <= 330) and (250 <= rightX2 <= 550 and 30 <= yTwo1 <= 330) and getLargestExponent(poly) % 2 == 1:
                drawLine(rightX1, yOne1, rightX2, yTwo1, fill = app.colorList[k % len(app.colorList)])
            
            elif (250 <= rightX1 <= 550 and 30 <= yOne2 <= 330) and  (250 <= rightX2 <= 550 and 30 <= yTwo2 <= 330) and getLargestExponent(poly) % 2 == 0:
                drawLine(rightX1, yOne2, rightX2, yTwo2, fill = app.colorList[k % len(app.colorList)])
    
            if (250 <= leftX1 <= 550 and 30 <= yMinus1 <= 330) and (250 <= leftX2 <= 550 and 30 <= yMinus2 <= 330) and getLargestExponent(poly) % 2 == 1:
                drawLine(leftX1, yMinus1, leftX2, yMinus2, fill = app.colorList[k % len(app.colorList)])
            
            elif (250 <= leftX1 <= 550 and 30 <= yPlus1 <= 330) and (250 <= leftX2 <= 550 and 30 <= yPlus2 <= 330) and getLargestExponent(poly) % 2 == 0:
                drawLine(leftX1, yPlus1, leftX2, yPlus2, fill = app.colorList[k % len(app.colorList)])

    else:                                       # any other function 
        for i in range(0, 180): 
            scale = 0.3
            n3 = (i+scale)/10
            n4 = ((i+1) + scale)/10
            newOriginX = 180 + 1/2*(scaleToGridX) * (app.parameters.maxX - app.parameters.minX)
            newOriginY = 400 - 1/2*(scaleToGridY) * (app.parameters.maxY - app.parameters.minY)
            
            rightX3 = newOriginY + n3 * scaleToGridY
            leftX3 = newOriginY - n3 * scaleToGridY
            yOne3 = newOriginX + polyClassLeft.evalAt(-n3) * scaleToGridX
            yTwo3 = newOriginX + polyClassLeft.evalAt(n3) * scaleToGridX
            yMinus3 = newOriginX - polyClassLeft.evalAt(- n3) * scaleToGridX
            yPlus4 = newOriginX + polyClassLeft.evalAt(n3) * scaleToGridX
        
            
            rightX4 = (newOriginY + n4 * scaleToGridY)
            leftX4 = (newOriginY - n4 * scaleToGridY)
            yOne4 = newOriginX + polyClassLeft.evalAt(- n4) * scaleToGridX
            yTwo4 = newOriginX + polyClassLeft.evalAt(n4) * scaleToGridX
            yMinus2 = newOriginX - polyClassLeft.evalAt(- n4) * scaleToGridX
            yPlus2 = newOriginX + polyClassLeft.evalAt(n4) * scaleToGridX
            
            
            if (250 <= leftX3 <= 550 and 30 <= yOne3 <= 330) and (250 <= leftX4 <= 550 and 30 <= yOne4 <= 330):
                drawLine(leftX3, yOne3, leftX4, yOne4, lineWidth = 2, fill = app.colorList[k % len(app.colorList)])
            if (250 <= rightX4 <= 550 and 30 <= yTwo4 <= 330) and (250 <= rightX3 <= 550 and 30 <= yTwo3 <= 330): 
                drawLine(rightX3, yTwo3, rightX4, yTwo4, lineWidth = 2, fill = app.colorList[k % len(app.colorList)])
  
def onMousePress(app, mouseX, mouseY):
    if (45 <= mouseX <= 175) and (150 <= mouseY <= 180):
        if app.clickedButton == 1:
            app.clickedButton = 0
        else:
            app.clickedButton = 1
    elif (210 <= mouseX <= 235) and (30 <= mouseY <= 50):
        if app.clickedButton == 2:
            app.clickedButton = 0
        else:
            app.clickedButton = 2
    elif (210 <= mouseX <= 235) and (310 <= mouseY <= 330):
        if app.clickedButton == 3:
            app.clickedButton = 0
        else:
            app.clickedButton = 3
    elif (250 <= mouseX <= 275) and (355 <= mouseY <= 375):
        if app.clickedButton == 4:
            app.clickedButton = 0
        else:
            app.clickedButton = 4
    elif (525 <= mouseX <= 550) and (355 <= mouseY <= 375):
        if app.clickedButton == 5:
            app.clickedButton = 0
        else:
            app.clickedButton = 5
    elif (60 <= mouseX <= 160) and (355 <= mouseY <= 375):
        app.polynomials = [ ]
    elif (365 <= mouseX <= 435) and (370 <= mouseY <= 390):
        app.parameters.maxX = 5
        app.parameters.maxY = 5
        app.parameters.minX = 5
        app.parameters.minY = 5
       
        app.clickedTwoString = '5'
        app.clickedThreeString = '-5'
        app.clickedFourString = '-5'
        app.clickedFiveString = '5'

def onKeyPress(app, key):
    if app.clickedButton == 1:
        if key == 'backspace':
            app.currPoly = app.currPoly[:-1]
        elif key != 'enter' and key.isdigit() or (key == 'x' or key == '^' or key == '+' or key == '-' or key == '.'):
            app.currPoly += key 
        if key == 'enter' and isValidPoly(app.currPoly):
            app.polynomials.append(app.currPoly)
            app.isDrawn = True
            app.currPoly = ''
            if len(app.polynomials) > 8:
                app.polynomials.pop(0)
            
            
    if app.clickedButton == 2:
        if key == 'backspace':
            app.clickedTwoString = app.clickedTwoString[:-1]
        if key.isdigit():
            app.clickedTwoString += key
        if key == 'enter' and app.clickedTwoString != '' and len(app.clickedTwoString) > 0 and 0 <= int(app.clickedTwoString) <= 30:
            app.parameters.maxX = int(app.clickedTwoString)
        elif key == 'enter' and app.clickedTwoString != '' and int(app.clickedTwoString) >= 30:
            app.parameters.maxX = 30
            app.clickedTwoString = '30'
    
    if app.clickedButton == 3:
        if key == 'backspace':
            app.clickedThreeString = app.clickedThreeString[:-1]
        if key.isdigit() or key == '-' and '-' not in app.clickedThreeString:
            app.clickedThreeString += key
        if key == 'enter' and app.clickedThreeString != '' and 4 >= int(app.clickedThreeString) >= -30 and len(app.clickedThreeString) > 0:
            app.parameters.minX = -int(app.clickedThreeString)
        elif key == 'enter' and app.clickedThreeString != '' and int(app.clickedThreeString) >= 30:
            app.parameters.minX = -30
            app.clickedThreeString = '30'
    
    if app.clickedButton == 4:
        if key == 'backspace':
            app.clickedFourString = app.clickedFourString[:-1]
        if key.isdigit() or key == '-' and '-' not in app.clickedFourString:
            app.clickedFourString += key
        if key == 'enter' and app.clickedFourString != '' and 4 >= int(app.clickedFourString) >= -30:
            app.parameters.minY = -int(app.clickedFourString)
        elif key == 'enter' and app.clickedFourString != '' and int(app.clickedFourString) >= 30:
            app.parameters.minY = -30
            app.clickedFourString = '30'
    
    if app.clickedButton == 5:
        if key == 'backspace':
            app.clickedFiveString = app.clickedFiveString[:-1]
        if key.isdigit():
            app.clickedFiveString += key
        if key == 'enter' and app.clickedFiveString != '' and  0 <= int(app.clickedFiveString) <= 30:
            app.parameters.maxY = int(app.clickedFiveString)
        elif key == 'enter' and app.clickedFiveString != '' and int(app.clickedFiveString) >= 30:
            app.parameters.maxY = 30
            app.clickedFiveString = '30'
            
def isValidPoly(s): # verify if what is being typed is a polynomial 
    s = insertSpaces(s)
    if (len(s) > 1) and s[-1] == 'x' or s[-1] == '^' or s[-1].isdigit():
        if '.' in s and s[-2] == '.':
            return False
    testList = [ ]
    if len(s) == 4 and ('-' in s) and ('x' not in s):
        return True
    if s == 'x^':
        return False
    for elem in s.split(' '):
        if elem.count('x') > 1:
            return False
        if elem != '' and elem[len(elem) - 1] == '.':
            return False
        if elem != '' and elem[len(elem) - 1] == '^':
            return False
        if (elem != '-' and elem != '+') and (not elem.isdigit()):
            if 'x' not in elem or elem == 'x^':
                return False
        testList.append(elem)
    return True 
        

def main():
    runApp(600, 400)

main()
