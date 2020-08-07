from graph import *


file_name=['map1.1.txt','map1.2.txt','map2.1.txt','map2.2.txt']
#123123123

map,food,monster,pacman,h,w=graphic_loadmap(file_name[2])   
a=Pen()
x0,y0=a.draw_map(map,h,w,x_left_top,y_left_top,shape)
p=Player(player_shape,pacman[0],pacman[1])
p.start(x0+pacman[1]*square,y0-pacman[0]*square)
m=Player(monster_shape,monster[0][0],monster[0][1])
m.start(x0+monster[0][1]*square,y0-monster[0][0]*square)
f1=Food(food_shape,win_effect)
f1.start(x0+food[0][1]*square,y0-food[0][0]*square)

path=Lv12_A_Star(file_name[2])
if (type(path)==list):
    for i in path:
        p.move(i)
f1.win_effect()
done()
