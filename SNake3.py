import sys

from random import randrange

from PyQt5.QtWidgets import QMainWindow, QFrame,  QApplication, QDesktopWidget
from PyQt5.QtGui import QPen, QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QBasicTimer


class Snake(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.highscore = 0
        self.newGame()
        self.resize(600, 610)
        self.center
        self.setWindowTitle('Snake')
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawBorders(qp)
        self.drawSnake(qp)
        self.drawSpeedo(qp)
        self.drawFood(qp)
        self.information(event, qp)
        if self.isOver:
            self.gameOver(event, qp)
        qp.end()

    def keyPressEvent(self, enter):
        if not self.isPaused:
            if (enter.key() == Qt.Key_Up or enter.key() == Qt.Key_W) and self.lastKeyPress != 'UP' and self.lastKeyPress != 'DOWN' and self.snakeArray[0][1] - self.snakeArray[1][1] != 20:
                self.lastKeyPress = 'UP'
            elif (enter.key() == Qt.Key_Down or enter.key() == Qt.Key_S) and self.lastKeyPress != 'DOWN' and self.lastKeyPress != 'UP' and self.snakeArray[0][1] - self.snakeArray[1][1] != -20:
                self.lastKeyPress = 'DOWN'
            elif (enter.key() == Qt.Key_Left or enter.key() == Qt.Key_A) and self.lastKeyPress != 'LEFT' and self.lastKeyPress != 'RIGHT' and self.snakeArray[0][0] - self.snakeArray[1][0] != 20:
                self.lastKeyPress = 'LEFT'
            elif (enter.key() == Qt.Key_Right or enter.key() == Qt.Key_D) and self.lastKeyPress != 'RIGHT' and self.lastKeyPress != 'LEFT' and self.snakeArray[0][0] - self.snakeArray[1][0] != -20:
                self.lastKeyPress = 'RIGHT'
            elif enter.key() == Qt.Key_Space:
                self.pause()
        elif enter.key() == Qt.Key_Space:
            self.start()
        elif enter.key() == Qt.Key_R:
            self.newGame()
        elif enter.key() == Qt.Key_Escape:
            self.close()

    def newGame(self):
        self.score = 0
        self.x = 300
        self.y = 300
        self.lastKeyPress = 'RIGHT'
        self.timer = QBasicTimer()
        self.snakeArray = [[self.x, self.y], [self.x - 20, self.y], [self.x - 20, self.y]]
        self.foodx = 0
        self.foody = 0
        self.isPaused = True
        self.isOver = False
        self.FoodPlaced = False
        self.speed = 150
        self.pause()

    def pause(self):
        self.isPaused = True
        self.timer.stop()
        self.update()

    def start(self):
        self.isPaused = False
        self.timer.start(self.speed, self)
        self.update()

    def movement(self):
        if self.lastKeyPress == 'DOWN' and self.check(self.x, self.y + 20):
            self.y += 20
            if self.y == 580:
                self.y = 20
            self.snakeArray.insert(0, [self.x, self.y])
        elif self.lastKeyPress == 'UP' and self.check(self.x, self.y - 20):
            self.y -= 20
            if self.y == 0:
                self.y = 560
            self.snakeArray.insert(0, [self.x, self.y])
        elif self.lastKeyPress == 'RIGHT' and self.check(self.x + 20, self.y):
            self.x += 20
            if self.x == 580:
                self.x = 20
            self.snakeArray.insert(0, [self.x, self.y])
        elif self.lastKeyPress == 'LEFT' and self.check(self.x - 20, self.y):
            self.x -= 20
            if self.x == 0:
                self.x = 560
            self.snakeArray.insert(0, [self.x, self.y])

        self.update()


    def information(self, event, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('Decorative', 14))
        qp.drawText(20, 17, "Текущий счёт: " + str(self.score))
        qp.drawText(460, 17, "Рекорд: " + str(self.highscore))
        qp.setFont(QFont('Time', 8))
        qp.drawText(20, 590, "Управление - W,A,S,D(в англ.расладке) или стрелки.              Пауза - пробел, новая игра - R, выход - Escape.")
        if self.isPaused and not self.isOver:
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(0, 0, 200, 150))
            qp.drawRect(187, 71, 226, 46)
            qp.setFont(QFont('Decorative', 11))
            qp.drawText(201, 100, "Нажмите пробел для старта")

    def gameOver(self, event, qp):
        self.highscore = max(self.highscore, self.score)

        qp.setPen(QColor(255, 255, 255))
        qp.setBrush(QColor(200, 0, 0, 200))
        qp.drawRect(177, 257, 246, 86)
        qp.setFont(QFont('Decorative', 22))
        qp.drawText(223, 310, "GAME OVER")

    def check(self, x, y):

        if self.snakeArray[0] in self.snakeArray[1:len(self.snakeArray)]:
            self.pause()
            self.isPaused = True
            self.isOver = True
            return False
        elif self.y == self.foody and self.x == self.foodx:
            self.FoodPlaced = False
            self.score += 1
            if self.score >= 10:
                self.speed = 100
                self.timer.start(self.speed, self)
            if self.score >= 20:
                self.speed = 75
                self.timer.start(self.speed, self)
            if self.score >= 35:
                self.speed = 50
                self.timer.start(self.speed, self)
            if self.score >= 50:
                self.speed = 25
                self.timer.start(self.speed, self)
            return True
        self.snakeArray.pop()
        return True

    def drawSpeedo(self,  qp):
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))

        qp.setBrush(QColor(128, 255, 0, 255))
        qp.drawRect(260, 3, 16, 16)
        if self.speed <= 100:
            qp.setBrush(QColor(208, 255, 138, 255))
        else:
            qp.setBrush(QColor(255, 255, 255, 255))
        qp.drawRect(276, 3, 16, 16)
        if self.speed <= 75:
            qp.setBrush(QColor(255, 255, 128, 255))
        else:
            qp.setBrush(QColor(255, 255, 255, 255))
        qp.drawRect(292, 3, 16, 16)
        if self.speed <= 50:
            qp.setBrush(QColor(255, 128, 64, 255))
        else:
            qp.setBrush(QColor(255, 255, 255, 255))
        qp.drawRect(308, 3, 16, 16)
        if self.speed <= 25:
            qp.setBrush(QColor(255, 0, 0, 255))
        else:
            qp.setBrush(QColor(255, 255, 255, 255))
        qp.drawRect(324, 3, 16, 16)

    def drawBorders(self, qp):
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        qp.drawRect(20, 20, 560, 560)
        qp.setPen(QPen(Qt.black, 1, Qt.DotLine))
        for i in range(2, 29):
            qp.drawLine(i*20, 20, i*20, 580)
            qp.drawLine(20, i*20, 580, i*20)

    def drawFood(self, qp):
        if self.FoodPlaced == False:
            self.foodx = randrange(2, 29) * 20
            self.foody = randrange(2, 29) * 20
            if not [self.foodx, self.foody] in self.snakeArray:
                self.FoodPlaced = True
        qp.setPen(QColor(255, 255, 255))
        qp.setBrush(QColor(255, 55, 0, 160))
        qp.drawRect(self.foodx, self.foody, 20, 20)

    def drawSnake(self, qp):
        qp.setPen(QColor(128, 128, 128))
        qp.setBrush(QColor(50, 70, 50, 255))
        for i in self.snakeArray:
            qp.drawRect(i[0], i[1], 20, 20)
            self.update()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.movement()
        else:
            QFrame.timerEvent(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Snake()
    sys.exit(app.exec_())
