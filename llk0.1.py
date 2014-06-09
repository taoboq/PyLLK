#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author: GeekSword
website: onestraw.net
"""

import sys, random
from PyQt4 import QtGui, QtCore

'''implement queue operation using list()'''
def enQueue(q,e):
	q.append(e)
def deQueue(q):
	ret = q[0]
	q.remove(ret)
	return ret
def isEmpty(q):
	if len(q)==0:
		return 1
	return 0

''' LLK MAIN WINDOW class '''
class LLK_MAIN_WIN(QtGui.QWidget):
    def __init__(self):
        super(LLK_MAIN_WIN, self).__init__()
        self.painter = QtGui.QPainter()
        self.width=800
        self.height=640
        self.grid_width=80
        self.grid_height=80

        self.initUI()
        self.preClick=[-1,-1]
        self.curClick=[-1,-1]
        self.cols = self.width/self.grid_width
        self.rows = self.height/self.grid_height
        self.imageNum=10
        self.image=list()
        for i in range(0, self.rows):
                images=list()
                for j in range(0, self.cols):
                        no = (self.cols *i + j)%self.imageNum
                        iname="image/%d.jpg" %no
                        images.append(iname)
                self.image.append(images)
        self.confuse()
		
    def initUI(self):
            self.setGeometry(300, 300, self.width,self.height)
            self.setWindowTitle('One Straw LLK')
            self.show()

    def showPixmap(self, image, x, y):
            pm = QtGui.QPixmap(image)
            pm = pm.scaled(self.grid_width, self.grid_height)
            self.painter.drawPixmap(x, y, pm)

    def paintEvent(self, event):
            print "this is an event"
            self.painter.begin(self)
            for i in range(0, self.height, self.grid_height):
                    for j in range(0, self.width, self.grid_width):
                            self.showPixmap(self.image[i/self.grid_height][j/self.grid_width], j, i)
            self.painter.end()

    def confuse(self):
            '''
                randomize the self.image[][]
                '''
            for k in range(self.imageNum*10):
                    irow = random.randint(0, self.rows-1)
                    icol = random.randint(0, self.cols-1)
                    jrow = random.randint(0, self.rows-1)
                    jcol = random.randint(0, self.cols-1)
                    temp = self.image[irow][icol]
                    self.image[irow][icol] = self.image[jrow][jcol]
                    self.image[jrow][jcol] = temp
			
    def x(self, pos):
	    return pos.x()/self.grid_width
    def y(self, pos):
	    return pos.y()/self.grid_height

    def mousePressEvent(self, event):
            clickPos = event.pos()
            x=self.y(clickPos)
            y=self.x(clickPos)
            self.preClick=self.curClick
            self.curClick=[x,y]
            if self.preClick[0] > -1:
                    px = self.preClick[0]
                    py = self.preClick[1]
                    self.image[px][py]='image/'+self.image[px][py].split('/')[1]
                    self.repaint()
            if event.button()==QtCore.Qt.LeftButton:
                    print "left click"
                    if self.image[self.preClick[0]][self.preClick[1]] == self.image[self.curClick[0]][self.curClick[1]] and self.curClick!=self.preClick and self.findPath(self.curClick, self.preClick) == 1:
                            print "find path"
                            self.image[self.preClick[0]][self.preClick[1]]="image/bg.jpg"
                            self.image[self.curClick[0]][self.curClick[1]]="image/bg.jpg"
                            self.preClick=[-1,-1]
                            self.curClick=[-1,-1]
                    if self.image[x][y].split('/')[0]=='image':
                            self.image[x][y]="image_select/"+self.image[x][y].split('/')[1]
                            self.repaint()

            if event.button()==QtCore.Qt.RightButton:
                    print "right click"
                    if self.image[x][y].split('/')[0]=='image_select':
                            self.image[x][y]='image/'+self.image[x][y].split('/')[1]
                            self.repaint()

    def findPath(self, curClick, preClick):
            '''
                find reachable path in less than 3 turnings
	    '''
            q=list()
            curClick.append(0)
            enQueue(q, curClick)
            while isEmpty(q)==0:
                    e=deQueue(q)
                    if e[2]>2:
                            return 0
                    #to top
                    for x in range(e[0]-1, -1, -1):
                            if self.image[x][e[1]].split('/')[1]=="bg.jpg":
                                    enQueue(q,[x, e[1], e[2]+1])
                            elif preClick[0]==x and preClick[1] ==e[1]:
                                    return 1
                            else:
                                    break
		    #to down
                    for x in range(e[0]+1, self.rows, 1):
                            if self.image[x][e[1]].split('/')[1]=="bg.jpg":
                                    enQueue(q,[x, e[1], e[2]+1])
                            elif preClick[0]==x and preClick[1] ==e[1]:
                                    return 1
                            else:
                                    break
		    #to left
                    for x in range(e[1]-1, -1, -1):
                            if self.image[e[0]][x].split('/')[1]=="bg.jpg":
                                    enQueue(q,[e[0], x, e[2]+1])
                            elif preClick[0]==e[0] and preClick[1] ==x:
                                    return 1
                            else:
                                    break
		    #to right
                    for x in range(e[1]+1, self.cols, 1):
                            if self.image[e[0]][x].split('/')[1]=="bg.jpg":
                                    enQueue(q,[e[0], x, e[2]+1])
                            elif preClick[0]==e[0] and preClick[1] ==x:
                                    return 1
                            else:
                                    break

def main():
    app = QtGui.QApplication(sys.argv)
    ex = LLK_MAIN_WIN()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
