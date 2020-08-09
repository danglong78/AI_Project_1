from graph import *


file_name=['map1.1.txt','map1.2.txt','map2.1.txt','map2.2.txt']
#123123123

map,food,monster,pacman,h,w=graphic_loadmap("15x20.txt")
a=Pen(wall_shape)
x0,y0=a.draw_map(map,h,w)
p=Player(player_shape,pacman[0],pacman[1])
p.start(x0+pacman[1]*square,y0-pacman[0]*square)
m=[Player(monster_shape[i%2],monster[i][0],monster[i][1]) for i in range(len(monster))]
for i in range(len(m)):
    m[i].start(x0+monster[i][1]*square,y0-monster[i][0]*square)
f=[Food(food_shape[i%5],win_effect,food[i][1],food[i][0])for i in range(len(food))]
for i in range(len(f)):
    f[i].start(x0+food[i][1]*24,y0-food[i][0]*24)

path=Lv12_A_Star("15x20.txt")
if (type(path)==list):
    for i in path:
        p.move(i)
        list_eaten=np.argwhere((food==np.array([p.row,p.col])).prod(axis=1)==1)
        if list_eaten.size!=0:
           f[list_eaten.item()].win_effect(np.random.randint(1,2))

done()
