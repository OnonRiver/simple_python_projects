import tkinter
import random

# constans
WIDTH = 640
HEIGHT = 480
BG_COLOR = "white"
BLACK_COLOR = "black"
BAD_COLOR = "red"
COLORS = ["aqua", "fuchsia", BAD_COLOR, "pink", "yellow", BAD_COLOR, "gold", "chartreuse"]
ZERO = 0
MAIN_BALL_RADIUS = 30
MAIN_BALL_COLOR = "blue"
INIT_DX = 1
INIT_DY = 1
DELAY = 5
NUM_OF_BALLS = 5


#balls class
class Balls():
    def __init__(self, x, y, r, color, dx = 0, dy = 0):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy

    def draw(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
                           fill = self.color, outline = self.color if self.color != BAD_COLOR else BLACK_COLOR)

    def hide(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
                           fill= BG_COLOR, outline = BG_COLOR)

    def is_collision(self, ball):
        a = abs(self.x + self.dx - ball.x)
        b = abs(self.y + self.dy - ball.y)
        return (a*a + b*b)**0.5 <= self.r + ball.r

    def move(self):
        # colliding with walls
        if (self.x + self.r + self.dx >= WIDTH) or (self.x - self.r + self.dx <= ZERO):
            self.dx = -self.dx
        if (self.y + self.r + self.dy >= HEIGHT) or (self.y - self.r + self.dy <= ZERO):
            self.dy = -self.dy
        # colliding with other balls
        for ball in balls:
            if self.is_collision(ball):
                if ball.color != BAD_COLOR:
                    ball.hide()
                    balls.remove(ball)
                    self.dx = -self.dx
                    self.dy = -self.dy
                else:
                    self.dx = self.dy = 0
        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()


# mouse events
def mouse_click(event):
    global main_ball
    if event.num == 1:
        if 'main_ball' not in globals():
            main_ball = Balls(event.x, event.y, MAIN_BALL_RADIUS, MAIN_BALL_COLOR, INIT_DX, INIT_DY)
            main_ball.draw()
        else: # turn to the left
            if main_ball.dx * main_ball.dy > 0:
                main_ball.dy = -main_ball.dy
            else:
                main_ball.dx = -main_ball.dx
    elif event.num == 3: # turn right
        if main_ball.dx * main_ball.dy > 0:
            main_ball.dx = -main_ball.dx
        else:
            main_ball.dy = -main_ball.dy

#creating list of balls
def create_list_of_balls(number):
    lst = []
    while len(lst) < number:
        next_ball = Balls(random.choice(range(0, WIDTH)),
                        random.choice(range(0, HEIGHT)),
                        random.choice(range(15, 35)),
                        random.choice(COLORS))
        lst.append(next_ball)
        next_ball.draw()
    return lst


# count of bad balls
def count_bad_balls(list_of_balls):
    res = 0
    for ball in list_of_balls:
        if ball.color == BAD_COLOR:
            res += 1
    return res


#main game cycle
def main():
    if "main_ball" in globals(): # if main object is created
        main_ball.move() # then move main object
        if len(balls) - num_of_bad_balls == 0:
            canvas.create_text(WIDTH/2, HEIGHT/2, text = "You are Winner!!!", font = "Arial 20", fill = "green")
            main_ball.dx = main_ball.dy = 0
        elif main_ball.dx == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text="You are Loser!!!", font="Arial 20", fill= BAD_COLOR)
    root.after(DELAY, main)


root = tkinter.Tk() #создаём корневое окно
root.title("Colliding Balls") #задаем заголовок для окна
canvas = tkinter.Canvas(root, width = WIDTH, height = HEIGHT, bg = BG_COLOR) # создаём канву и задаем ее размеры
canvas.pack() # команда для отражения окна
canvas.bind("<Button-1>", mouse_click) #метод перехвата нажатий на мышь
canvas.bind("<Button-3>", mouse_click, "+")
if "main_ball" in globals():
    del main_ball
balls = create_list_of_balls(NUM_OF_BALLS)
num_of_bad_balls = count_bad_balls(balls)
main()
root.mainloop() # команд, которой заканчивается любая программа с tkinter