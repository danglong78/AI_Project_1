from turtle import *
from search import *
import numpy as np
from time import *
square=24

scr=Screen()
scr.bgcolor("black")
scr.setup(1000,1000,0,0)
ht()
penup()
setpos(0,300)
color("white")
write("PROJECT 1",align="center" ,font=("Arial",50,"normal"))


def input_shape():
    move=["d","u","r","l"]
    wall_shape=r"Pic\wall.gif"
    food_shape=[r"Pic\food"+str(i)+".gif" for i in range(1,6)]
    monster_shape=[[[r"Pic\monster"+str(k)+"_"+i+str(j)+".gif" for j in range(1,4)] for i in move]for k in range(1,3)]
    player_shape=[["Pic\\"+i+str(j)+".gif" for j in range(1,4)] for i in move]
    win_effect=[["Pic\\"+str(j)+"win"+str(i)+".gif" for i in range(1,9)] for j in range(1,3)]
    lose_effect=[r"Pic\lose"+ str(i)+".gif" for i in range(1,9)]
    return wall_shape,food_shape,monster_shape,player_shape,win_effect,lose_effect

wall_shape,food_shape,monster_shape,player_shape,win_effect,lose_effect=input_shape()



scr.addshape(wall_shape)
for i in food_shape:
    scr.addshape(i)
for i in win_effect:
    for j in i:
        scr.addshape(j)
for i in player_shape:
    for j in i:
        scr.addshape(j)
for i in monster_shape:
    for j in i:
        for k in j:
            scr.addshape(k)
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
    global x_left_top,y_left_top
    x_left_top= -((m//2)+1)*24
    y_left_top=(n//2 + 1)*24


    return map_game,np.array(food),np.array(monster),np.array(pac_man),n,m


class Pen(Turtle):
    def __init__(self,wall):
        Turtle.__init__(self)
        self.speed(0)
        self.penup()
        self.shape(wall)
    def draw_outline(self,h,w):
        x0= -((w//2)+1)*square
        y0=(h//2 + 1)*square
        outline_stamp=[]
        for i in range(w+2):
            self.goto(x0+i*square,y0)
            outline_stamp+=[self.stamp()]
        for i in range(1,h+2):
            self.goto(x0+(w+1)*square,y0-i*square)
            outline_stamp+=[self.stamp()]
        for i in range(w+1):
            self.goto(x0+i*square,y0-(h+1)*square)
            outline_stamp+=[self.stamp()]
        for i in range(1,h+1):
            self.goto(x0,y0-i*square)
            outline_stamp+=[self.stamp()]
        return outline_stamp
    def draw_map(self,map,h,w):
        outline_stamp=self.draw_outline(h,w)
        x=-((w//2)+1)*square+square
        y=(h//2 + 1)*square-square
        food=[]
        monster=[]
        list_wall={}
        self.st()
        for i in range(h):
            for j in range(w):
                if map[i][j]==1:
                    temp=self.clone()
                    list_wall[(i,j)]=temp
                    temp.goto(x+j*square,y-i*square)
   
                else:
                    continue
        return x,y,list_wall,outline_stamp





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
    def down(self):
        self.seth(270)
        for i in range(4):
            self.shape(self.s[0][i%2])
            self.fd(6)
        self.shape(self.s[0][2])
    def up(self):
        self.seth(90)
        for i in range(4):
            self.shape(self.s[1][i%2])
            self.fd(6)
        self.shape(self.s[1][2])
    def right(self):
        self.seth(0)
        for i in range(4):
            self.shape(self.s[2][i%2])
            self.fd(6)
        self.shape(self.s[2][2])
    def left(self):
        self.seth(180)
        for i in range(4):
            self.shape(self.s[3][i%2])
            self.fd(6)
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
    def lose(self,s):  
        for i in range(len(s)):
                self.shape(s[i])
                sleep(0.01)
        self.ht()
class Food(Turtle):
    def __init__(self,s,effect,x,y):
        Turtle.__init__(self)
        self.ht()
        self.speed(0)
        self.penup()
        self.s=s
        self.effect=effect
        self.x=x
        self.y=y
    def start(self,x,y):
        self.shape(self.s)
        self.goto(x,y)
        self.st()
        self.speed(5)   
    def win_effect(self,index):
        for _ in range(2):
            for i in self.effect[index%2]:
                self.shape(i)
                sleep(0.01)
        self.ht()

class Map:
    def __init__(self, filename):
        self.map,self.food,monster,pacman,self.h,self.w=graphic_loadmap(filename)
        self.outline=Pen(wall_shape)
        x0,y0,self.list_wall,self.outline_stamp=self.outline.draw_map(self.map,self.h,self.w)
        self.p=Player(player_shape,pacman[0],pacman[1])
        self.m=[Player(monster_shape[i%2],monster[i][0],monster[i][1]) for i in range(len(monster))]
        self.f=[Food(food_shape[i%5],win_effect,self.food[i][0],self.food[i][1])for i in range(len(self.food))]
        for i in range(len(self.m)):
            self.m[i].start(x0+monster[i][1]*square,y0-monster[i][0]*square)
            self.list_wall[(monster[i][0],monster[i][1])]=self.m[i]
        for i in range(len(self.f)):
            self.f[i].start(x0+self.food[i][1]*24,y0-self.food[i][0]*24)
            self.list_wall[(self.food[i][0],self.food[i][1])]=self.f[i]
        self.p.start(x0+pacman[1]*square,y0-pacman[0]*square)
        self.p.st()
        self.eaten=0
        self.score=0
    def eat_food(self):
        list_eaten=np.argwhere((self.food==np.array([self.p.row,self.p.col])).prod(axis=1)==1)
        if list_eaten.size!=0:
            self.p.ht()
            self.f[list_eaten.item(0)].win_effect(np.random.randint(1,2))
            self.food[list_eaten.item(0)]=[-1,-1]
            self.p.st()
            self.eaten+=1
            self.score+=20

    def is_beat(self):
        monster=[(i.row,i.col) for i in self.m]
        list_beaten=np.argwhere((monster==np.array([self.p.row,self.p.col])).prod(axis=1)==1)
        if list_beaten.size!=0:
           self.m[list_beaten.item(0)].ht()
           self.p.lose(lose_effect)
           self.m[list_beaten.item(0)].st()
           return True
        return False

    def explore(self):
        a,b,c,d=self.p.row-2 if self.p.row-2>=0 else 0,self.p.row+3 if self.p.row+3<=self.h else self.h,self.p.col-2 if self.p.col-2>=0 else 0,self.p.col+3 if self.p.col+3<=self.w else self.w
        temp=[(x,y) for x in range(a,b) for y in range(c,d)]
        for i in temp:
            if i in self.list_wall:
                self.list_wall[i].st()
                if type(self.list_wall[i])==Food:
                    self.list_wall.pop(i)
    def monster_visual(self):
        a,b,c,d=self.p.row-2 if self.p.row-2>=0 else 0,self.p.row+3 if self.p.row+3<=self.h else self.h,self.p.col-2 if self.p.col-2>=0 else 0,self.p.col+3 if self.p.col+3<=self.w else self.w
        temp=[(x,y) for x in range(a,b) for y in range(c,d)]
        pos=[(i.row,i.col,i) for i in self.m]
        for i in pos:
            if i not in temp:
                i[2].ht()
    def hide_all(self):
        for i in self.list_wall.values():
            i.ht()


    def level1_2(self,path):
        if (type(path)==list):
            for i in path:
                self.p.move(i)
                self.score-=1
                self.eat_food()
            return True
        else:
            self.p.lose(lose_effect)
            return False

    def level3_4_hide(self,path_pacman,path_monster):
        self.hide_all()
        self.explore()
        if (type(path_pacman)==list):
            for i in range(len(path_pacman)):
                self.p.move(path_pacman[i])
                self.score-=1
                self.eat_food()
                if  self.eaten==len(self.f):
                    return True
                for j in range(len(self.m)):
                    self.m[j].move(path_monster[j][i])
                if self.is_beat():
                    return False
                self.explore()
    def level3_4_show(self,path_pacman,path_monster):
 
        if (type(path_pacman)==list):
            for i in range(len(path_pacman)):
                self.p.move(path_pacman[i])
                if self.is_beat():
                    return False
                self.score-=1
                self.eat_food()
                if  self.eaten==len(self.f):
                    return True
                for j in range(len(self.m)):
                    self.m[j].move(path_monster[j][i])
                if self.is_beat():
                    return False
    def print_result(self,isWin):
        self.outline.clearstamps(len(self.outline_stamp))
        self.hide_all()
        self.p.ht()
        self.outline.ht()
        output=""
        if isWin:
            output="YOU WIN"
        else:
            output="YOU LOSE"
        penup()
        setpos(-50,50)
        color("yellow")
        write(output,align="center" ,font=("STCaiyun",60,"normal"))
        setpos(-50,0)
        write("SCORE: "+str(self.score),align="center" ,font=("Arial",40,"normal"))
