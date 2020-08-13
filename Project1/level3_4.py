import numpy as np

#Hàm  load map
def loadmap_lv34(pathh):
    map_game=[]
    path=[] #[axis_x,axis_y]
    wall=[] 
    food=[]
    monster=[]
    fi=pathh
    f = open(pathh, 'r')
    if f.mode == 'r':
        line =f.readline()
        temp=line.split()
        n=int(temp[0])
        m=int(temp[1])
        temp.clear()

        for row in range(n):
            line = f.readline()
            for number,y in zip(line.split(),range(m)):
                temp.append(int(number))
                if int(number) ==0:
                    path.append([row*10,y*10])
                if int(number) ==1:
                    wall.append([row*10,y*10])
                if int(number)==2:
                    food.append([row*10,y*10])
                if int(number)==3:
                    monster.append([row*10,y*10])
            map_game.append(temp.copy())
            temp.clear()
        line =f.readline()
        pac_man=[]
        for x in line.split():
            pac_man.append(int(x))
        
        f.close()
    return map_game,pac_man,n,m



def count_expend(maze,pos,h,w):
    count=0
    for i in range(-2,3):
        if(pos[0]+i>=0)and(pos[0]+i<h):
            for z in range(-2,3):
                if(pos[1]+z>=0)and(pos[1]+z<w):
                    if(maze[pos[0]+i][pos[1]+z]==-1):
                        count=count+1
    return count


def where2go(maze,cur_pos,re_pos,h,w):
    can_move=[]
    for i,z in zip([cur_pos[0]-1,cur_pos[0],cur_pos[0],cur_pos[0]+1],[cur_pos[1],cur_pos[1]-1,cur_pos[1]+1,cur_pos[1]]):
        if([i,z]!=re_pos) and (i>=0) and (i<h) and (z>=0) and (z<w) and ((maze[i][z]==0) or(maze[i][z]==2)):
            if not(is_danger(maze,[i,z],h,w)):
                can_move.append([i,z])
    if(len(can_move)==0):
        return re_pos
    else:
        can_move.sort(key = lambda x: count_expend(maze,x,h,w))
    if count_expend(maze,can_move[-1],h,w)==0:
        return can_move[np.random.randint(len(can_move))]
    return can_move[-1]



def marked_visited(maze,pm_maze,pos,h,w):
    for i in range(-2,3):
        if(pos[0]+i>=0)and(pos[0]+i<h):
            for z in range(-2,3):
                if(pos[1]+z>=0)and(pos[1]+z<w):
                    pm_maze[pos[0]+i][pos[1]+z]=maze[pos[0]+i][pos[1]+z]
                    
def un_explored_all(pm_maze,h,w):
    for i in range(h):
        for z in range(w):
            if(pm_maze[i][z]==-1):
                return True
    return False


def is_danger(maze,cur_pos,h,w):
    for i,z in zip([cur_pos[0]-1,cur_pos[0],cur_pos[0],cur_pos[0]+1],[cur_pos[1],cur_pos[1]-1,cur_pos[1]+1,cur_pos[1]]):
        if (i<h) and (i>=0) and (z<w) and (z>=0):
            if maze[i][z]>=3:
                return True
    return False


def ghost_next_step(maze,ghost_pos,cur_pos,h,w):
    if cur_pos!=ghost_pos:
        return ghost_pos.copy()
    can_move=[]
    for i,z in zip([ghost_pos[0]-1,ghost_pos[0],ghost_pos[0],ghost_pos[0]+1],[ghost_pos[1],ghost_pos[1]-1,ghost_pos[1]+1,ghost_pos[1]]):
        if(i>=0) and (i<h) and (z>=0) and (z<w) and (maze[i][z]!=1):
            can_move.append([i,z])
    return can_move[np.random.randint(len(can_move))]


# ham searh dung trong level 3 4 (BFS)
def next_stepp(maze,cur_pos,h,w):
    result=[]
    for i,z in zip([cur_pos[0]-1,cur_pos[0],cur_pos[0],cur_pos[0]+1],[cur_pos[1],cur_pos[1]-1,cur_pos[1]+1,cur_pos[1]]):
        if (i>=0) and (i<h) and (z>=0) and (z<w):
            if maze[i][z]==0 or maze[i][z]==2:
               result.append([i,z])
    return result


def lv3_4_search(maze,pos,des,h,w):
    exp_list=[]
    frontier=[]
    comp=False
    frontier.append([pos.copy(),pos.copy()])
    while(len(frontier)>0):
        cur=frontier[0]
        exp_list.append([cur[0].copy(),cur[1].copy()])
        nex_step=next_stepp(maze,cur[0],h,w)
        for i in nex_step:
            if i==des :
                exp_list.append([des,cur[0]])
                frontier.pop(0)
                comp=True
                break
        if comp :
            break
        for i in nex_step:
            check=True
            for z in exp_list:
                if i==z[0]:
                    check=False
                    break
            if check :
                for z in frontier:
                    if i==z[0]:
                        check=False
                        break
            if check :
                frontier.append([i.copy(),cur[0].copy()])
        frontier.pop(0)
    if comp==False:
        return []
    re_path=[]
    cur=exp_list[-1].copy()
    while(cur[0]!=pos):
        re_path.append(cur[0].copy())
        for i in exp_list:
            if i[0]==cur[1]:
                cur=i.copy()
                break
    #re_path.append(pos.copy())
    re_path.reverse()
    return re_path


# ham tro choi hoat dong
def lv3_play(maze,start,ghost_count,ghost_pos,h,w):
    count_food=0
    # tinh so luong thuc an
    for i in range(h):
        for z in range(w):
            if maze[i][z]==2:
                count_food=count_food+1
    # ban do cua pacman
    pm_maze=[]
    for i in range(h):
        pm_maze.append([])
        for z in range(w):
            pm_maze[i].append(-1)
    # tao ban do ban dau cua pacman
    marked_visited(maze,pm_maze,start,h,w)
    # duong di cua pacman trong tro choi
    pm_path=[]
    pm_path.append(start.copy())
    cur_pos=start.copy()
    # duong di tam thoi cua pacman
    path=[]
    # duong di cua ghost
    ghost_path=[]
    cur_ghost_pos=ghost_pos.copy()
    for i in range(ghost_count):
        ghost_path.append([])
        ghost_path[i].append(cur_ghost_pos[i].copy())
    # danh sach vi tri cac food pacman da thay
    food_pos_list=[]
    for i in range(h):
        for z in range(w):
            if pm_maze[i][z]==2 or pm_maze[i][z]==5:
                food_pos_list.append([i,z])
                
                
    # vong lap tro choi dien ra
    for turn in range(800):
        if not(un_explored_all(pm_maze,h,w)) and len(food_pos_list)>0:
            break
            
            
        #--------------------------------------------#
        #        xu ly di chuyen cua pacman          #
        #--------------------------------------------#
        
        pm_tur=True
        
        # khi da co san duong da tim den food
        if len(path)>0 :
            # kiem tra xem vi tri tiep theo co la moster - neu la moster se xoa path dang di va den phan sau
            if pm_maze[path[0][0]][path[0][1]]==3 or pm_maze[path[0][0]][path[0][1]]==5:
                path.clear()
            # neu step tiep theo an toan - kiem tra xem cac step lan can co moster khong. neu khong thi di thoi
            elif is_danger(maze,path[0],h,w):
                pm_path.append(cur_pos.copy())
                pm_tur=False
                
            # neu cac step lan can cua next step co moster - thu doi xem moster di chuyen nhu nao
            else:
                pm_path.append(path[0].copy())
                cur_pos = path[0].copy()
                path.pop(0)
                pm_tur=False
                # neu vi tri den la thuc an
                if(maze[cur_pos[0]][cur_pos[1]]==2):
                    maze[cur_pos[0]][cur_pos[1]]=0
                    count_food=count_food-1
                    path.clear()
                
                          
        # khi dang chua co duong di den food moi hoac duong di den food chac chan bi nguy hiem
        if len(path)==0 and pm_tur:
            # tim duong di ngan nhat den cac food trong danh sach
            for food in food_pos_list:
                temp_path=lv3_4_search(pm_maze,cur_pos,food,h,w)
                if(len(temp_path)>0):
                    if len(path)>len(temp_path) or len(path)==0:
                        path = temp_path.copy()
            # neu tim duoc duong di thi di thoi
            if len(path)>0:
                pm_path.append(path[0])
                cur_pos = path[0].copy()
                path.pop(0)
                pm_tur=False
                # neu vi tri den la thuc an
                if(maze[cur_pos[0]][cur_pos[1]]==2):
                    maze[cur_pos[0]][cur_pos[1]]=0
                    count_food=count_food-1
            # neu khong tim duoc duong den thuc an thi den o co heuristic cao nhat
            else:
                re_pos=pm_path[-1].copy()
                if(re_pos==cur_pos):
                    re_pos=pm_path[len(pm_path)-2].copy()
                next_step = where2go(pm_maze,cur_pos,re_pos,h,w)
                pm_path.append(next_step.copy())
                cur_pos = next_step.copy()
                pm_tur=False
                # neu vi tri den la thuc an
                if(maze[cur_pos[0]][cur_pos[1]]==2):
                    maze[cur_pos[0]][cur_pos[1]]=0
                    count_food=count_food-1
            
        if count_food==0:
            break
        #--------------------------------------------#
        #        xu ly di chuyen cua moster          #
        #--------------------------------------------#
        for i in range(ghost_count):
            temp_pos = ghost_next_step(maze,ghost_pos[i],cur_ghost_pos[i],h,w).copy()
            ghost_path[i].append(temp_pos.copy())
            maze[cur_ghost_pos[i][0]][cur_ghost_pos[i][1]] = maze[cur_ghost_pos[i][0]][cur_ghost_pos[i][1]]-3
            maze[temp_pos[0]][temp_pos[1]]=maze[temp_pos[0]][temp_pos[1]]+3
            cur_ghost_pos[i]=temp_pos.copy()
        #--------------------------------------------#
        #        cap nhat lai ban do cho pacman      #
        #--------------------------------------------#
        for i in range(h):
            for z in range(w):
                if(pm_maze[i][z]!=-1):
                    if maze[i][z]==0 or maze[i][z]==1 or maze[i][z]==2:
                        pm_maze[i][z] = maze[i][z]
                    elif maze[i][z]==3 or maze[i][z]==5:
                        pm_maze[i][z]=maze[i][z]-3
        marked_visited(maze,pm_maze,cur_pos,h,w)
        food_pos_list.clear()
        # cap nhat lai danh sach vi tri cua food
        for i in range(h):
            for z in range(w):
                if pm_maze[i][z]==2 or pm_maze[i][z]==5:
                    food_pos_list.append([i,z])
    return[pm_path,ghost_path]


# ham tra ket qua tro choi

def lv3(path):
    [maze,start,h,w]=loadmap_lv34(path)
    count_g=0
    pos_g=[]
    for i in range(h):
        for z in range(w):
            if maze[i][z]==3:
                count_g=count_g+1
                pos_g.append([i,z])
    return lv3_play(maze,start,count_g,pos_g,h,w)


# ham cua level 4:
def ghost_heuristic(maze,pm_pos,cur_pos,re_pos,h,w):
    can_move=[]
    for i,z in zip([cur_pos[0]-1,cur_pos[0],cur_pos[0],cur_pos[0]+1],[cur_pos[1],cur_pos[1]-1,cur_pos[1]+1,cur_pos[1]]):
        if(i>=0) and (i<h) and (z>=0) and (z<w) and (maze[i][z]!=1):
            can_move.append([i,z])
    can_move.sort(key = lambda x: abs(x[0]-pm_pos[0])+abs(x[1]-pm_pos[1]))
    if(can_move[0]==re_pos) and len(can_move)>1:
        return can_move[1]
    return can_move[0]


def lv4_play(maze,start,ghost_count,ghost_pos,h,w):
    count_food=0
    # tinh so luong thuc an
    for i in range(h):
        for z in range(w):
            if maze[i][z]==2:
                count_food=count_food+1
    # ban do cua pacman
    pm_maze=[]
    for i in range(h):
        pm_maze.append([])
        for z in range(w):
            pm_maze[i].append(-1)
    # tao ban do ban dau cua pacman
    marked_visited(maze,pm_maze,start,h,w)
    # duong di cua pacman trong tro choi
    pm_path=[]
    pm_path.append(start.copy())
    cur_pos=start.copy()
    # duong di tam thoi cua pacman
    path=[]
    # duong di cua ghost
    ghost_path=[]
    cur_ghost_pos=ghost_pos.copy()
    for i in range(ghost_count):
        ghost_path.append([])
        ghost_path[i].append(cur_ghost_pos[i].copy())
    # danh sach vi tri cac food pacman da thay
    food_pos_list=[]
    for i in range(h):
        for z in range(w):
            temp=pm_maze[i][z]
            if temp>=2 and ((temp-2)%3)==0:
                food_pos_list.append([i,z])
                
                
    # vong lap tro choi dien ra
    for turn in range(800):
        if not(un_explored_all(pm_maze,h,w)) and len(food_pos_list)>0:
            break
            
            
        #--------------------------------------------#
        #        xu ly di chuyen cua pacman          #
        #--------------------------------------------#
        
        pm_tur=True
        
        # khi da co san duong da tim den food
        if len(path)>0 :
            # kiem tra xem vi tri tiep theo co la moster - neu la moster se xoa path dang di va den phan sau
            if pm_maze[path[0][0]][path[0][1]]>=3:
                path.clear()
            # neu cac step lan can cua next step co moster - thu doi xem moster di chuyen nhu nao
            elif is_danger(maze,path[0],h,w):
                pm_path.append(cur_pos.copy())
                pm_tur=False
                
            
            # neu step tiep theo an toan - kiem tra xem cac step lan can co moster khong. neu khong thi di thoi
            else:
                pm_path.append(path[0].copy())
                cur_pos = path[0].copy()
                path.pop(0)
                pm_tur=False
                # neu vi tri den la thuc an
                if(maze[cur_pos[0]][cur_pos[1]]==2):
                    maze[cur_pos[0]][cur_pos[1]]=0
                    count_food=count_food-1
                
                          
        # khi dang chua co duong di den food moi hoac duong di den food chac chan bi nguy hiem
        if len(path)==0 and pm_tur:
            # tim duong di ngan nhat den cac food trong danh sach
            for food in food_pos_list:
                temp_path=lv3_4_search(pm_maze,cur_pos,food,h,w)
                if(len(temp_path)>0):
                    if len(path)>len(temp_path) or len(path)==0:
                        path = temp_path.copy()
            # neu tim duoc duong di thi di thoi
            if len(path)>0:
                pm_path.append(path[0])
                cur_pos = path[0].copy()
                path.pop(0)
                pm_tur=False
                # neu vi tri den la thuc an
                if(maze[cur_pos[0]][cur_pos[1]]==2):
                    maze[cur_pos[0]][cur_pos[1]]=0
                    count_food=count_food-1
            # neu khong tim duoc duong den thuc an thi den o co heuristic cao nhat
            else:
                re_pos=pm_path[-1].copy()
                if(re_pos==cur_pos):
                    re_pos=pm_path[len(pm_path)-2].copy()
                next_step = where2go(pm_maze,cur_pos,re_pos,h,w)
                pm_path.append(next_step.copy())
                cur_pos = next_step.copy()
                pm_tur=False
                # neu vi tri den la thuc an
                if(maze[cur_pos[0]][cur_pos[1]]==2):
                    maze[cur_pos[0]][cur_pos[1]]=0
                    count_food=count_food-1
            
        if count_food==0:
            break
        #--------------------------------------------#
        #        xu ly di chuyen cua moster          #
        #--------------------------------------------#
        for i in range(ghost_count):
            temp_pos = ghost_heuristic(maze,cur_pos,ghost_pos[i],ghost_path[i][-1],h,w).copy()
            maze[ghost_pos[i][0]][ghost_pos[i][1]]=maze[ghost_pos[i][0]][ghost_pos[i][1]]-3
            ghost_pos[i]=temp_pos.copy()
            maze[ghost_pos[i][0]][ghost_pos[i][1]]=maze[ghost_pos[i][0]][ghost_pos[i][1]]+3
            ghost_path[i].append(temp_pos.copy())
        #--------------------------------------------#
        #        cap nhat lai ban do cho pacman      #
        #--------------------------------------------#
        for i in range(h):
            for z in range(w):
                if(pm_maze[i][z]!=-1):
                    temp= maze[i][z]
                    if maze[i][z]==0 or maze[i][z]==1 or maze[i][z]==2:
                        pm_maze[i][z] = maze[i][z]
                    else:
                        pm_maze[i][z]=temp%3
        marked_visited(maze,pm_maze,cur_pos,h,w)
        food_pos_list.clear()
        # cap nhat lai danh sach vi tri cua food
        for i in range(h):
            for z in range(w):
                temp=pm_maze[i][z]
                if temp>=2 and ((temp-2)%3)==0:
                    food_pos_list.append([i,z])
    return[pm_path,ghost_path]


def lv4(path):
    [maze,start,h,w]=loadmap_lv34(path)
    count_g=0
    pos_g=[]
    for i in range(h):
        for z in range(w):
            if maze[i][z]==3:
                count_g=count_g+1
                pos_g.append([i,z])
    return lv4_play(maze,start,count_g,pos_g,h,w)