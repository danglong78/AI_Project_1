from turtle import *
from search import *
square=24
x_left_top=-150
y_left_top=100
scr=Screen()
scr.bgcolor("black")
scr.setup(1000,1000,0,0)
ht()
penup()
setpos(0,300)
color("white")
write("PROJECT 1",align="center" ,font=("Arial",50,"normal"))

#food_shape=[r"Pic\food1.gif",r"Pic\food2.gif",r"Pic\food3.gif"]
#wall_shape=r"Pic\wall.gif"
#monster_shape=[[r"Pic\monster_d1.gif",r"Pic\monster_d2.gif",r"Pic\monster_d3.gif"],[r"Pic\monster_u1.gif",r"Pic\monster_u2.gif",r"Pic\monster_u3.gif"],[r"Pic\monster_r1.gif",r"Pic\monster_r2.gif",r"Pic\monster_r3.gif"],[r"Pic\monster_l1.gif",r"Pic\monster_l2.gif",r"Pic\monster_l3.gif"]]
#player_shape=[[r"Pic\d1.gif",r"Pic\d2.gif",r"Pic\d3.gif"],[r"Pic\u1.gif",r"Pic\u2.gif",r"Pic\u3.gif"],[r"Pic\r1.gif",r"Pic\r2.gif",r"Pic\r3.gif"],[r"Pic\l1.gif",r"Pic\l2.gif",r"Pic\l3.gif"]]
#win_effect=[r"Pic\win1.gif",r"Pic\win2.gif",r"Pic\win3.gif",r"Pic\win4.gif",r"Pic\win5.gif",r"Pic\win6.gif",r"Pic\win7.gif",r"Pic\win8.gif"]
#lose_effect=[r"Pic\lose1.gif",r"Pic\lose2.gif",r"Pic\lose3.gif",r"Pic\lose4.gif",r"Pic\lose5.gif",r"Pic\lose6.gif",r"Pic\lose7.gif",r"Pic\lose8.gif",r"Pic\lose9.gif"]


def input_shape():
    move=["d","u","r","l"]
    wall_shape=r"Pic\wall.gif"
    food_shape=[r"Pic\food"+str(i)+".gif" for i in range(1,4)]
    monster_shape=[[r"Pic\monster_"+i+str(j)+".gif" for j in range(1,4)] for i in move]
    player_shape=[["Pic\\"+i+str(j)+".gif" for j in range(1,4)] for i in move]
    win_effect=[r"Pic\win"+str(i)+".gif" for i in range(1,9)]
    lose_effect=[r"Pic\lose"+str(i)+".gif" for i in range(1,10)]
    return wall_shape,food_shape,monster_shape,player_shape,win_effect,lose_effect

wall_shape,food_shape,monster_shape,player_shape,win_effect,lose_effect=input_shape()



scr.addshape(wall_shape)
for i in food_shape:
    scr.addshape(i)
for i in win_effect:
    scr.addshape(i)
for i in player_shape:
    for j in i:
        scr.addshape(j)
for i in monster_shape:
    for j in i:
        scr.addshape(j)
for i in lose_effect:
    scr.addshape(i)
def graphic_loadmap(fi):
    map_game=[]
    food=[]
    monster=[]
    f = open(fi, "r")
    if f.mode == "r":
        line =f.readline()
        temp=line.split()
        n=int(temp[0])
        m=int(temp[1])
        temp.clear()

        for row in range(n):
            line = f.readline()
            for number,y in zip(line.split(),range(m)):
                temp.append(int(number))
                if int(number)==2:
                    food.append([row,y])
                if int(number)==3:
                    monster.append([row,y])
            map_game.append(temp.copy())
            temp.clear()
        line =f.readline()
        pac_man=[]
        for x in line.split():
            pac_man.append(int(x))
        f.close()
    return map_game,food,monster,pac_man,n,m


class Pen(Turtle):
    def __init__(self):
        Turtle.__init__(self)
        self.color("white")
        self.speed(0)
        self.penup()
    def draw_outline(self,h,w,x0,y0):
        for i in range(w+2):
            self.goto(x0+i*square,y0)
            self.stamp()
        for i in range(1,h+2):
            self.goto(x0+(w+1)*square,y0-i*square)
            self.stamp()
        for i in range(w+1):
            self.goto(x0+i*square,y0-(h+1)*square)
            self.stamp()
        for i in range(1,h+1):
            self.goto(x0,y0-i*square)
            self.stamp()
    def draw_map(self,map,h,w,x0,y0,shape):
        self.shape(wall_shape)
        self.draw_outline(h,w,x0,y0)
        x=x0+square
        y=y0-square
        food=[]
        monster=[]
        for i in range(h):
            for j in range(w):
                if map[i][j]==1:
                    temp=self.shape(wall_shape)
                    self.goto(x+j*square,y-i*square)
                    self.stamp()
                else:
                    continue
        return x,y





class Player(Turtle):
    def __init__(self,s,row,col):
        Turtle.__init__(self)
        self.speed(0)
        self.ht()
        self.s=s
        self.penup()
        self.row=row
        self.col=col
    def start(self,x,y):
        self.shape(self.s[0][2])
        self.goto(x,y)
        self.st()
        self.speed(4)
    def down(self):
        self.seth(270)
        for i in range(8):
            self.shape(self.s[0][i%2])
            self.fd(3)
        self.shape(self.s[0][2])
    def up(self):
        self.seth(90)
        for i in range(8):
            self.shape(self.s[1][i%2])
            self.fd(3)
        self.shape(self.s[1][2])
    def right(self):
        self.seth(0)
        for i in range(8):
            self.shape(self.s[2][i%2])
            self.fd(3)
        self.shape(self.s[2][2])
    def left(self):
        self.seth(180)
        for i in range(8):
            self.shape(self.s[3][i%2])
            self.fd(3)
        self.shape(self.s[3][2])
    def move(self,index):
        if (self.row==index[0] and self.col>index[1]):
            self.left()
        elif (self.row==index[0] and self.col<index[1]):
            self.right()
        elif (self.row<index[0] and self.col==index[1]):
            self.down()
        elif (self.row>index[0] and self.col==index[1]):
            self.up()
        self.row,self.col=index
class Food(Turtle):
    def __init__(self,s,effect):
        Turtle.__init__(self)
        self.ht()
        self.speed(0)
        self.penup()
        self.s=s
        self.effect=effect
    def start(self,x,y):
        self.shape(self.s[0])
        self.goto(x,y)
        self.st()
        self.speed(5)   
    def win_effect(self):
        for _ in range(2):
            for i in self.effect:
                scr.delay(50)
                self.shape(i)
        self.ht()


    