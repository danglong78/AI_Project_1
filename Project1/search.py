#!/usr/bin/env python
# coding: utf-8

# In[31]:


def loadmap_search(path):
    map_game=[]
    wall=[] 
    f = open(path,'r')
    if f.mode == 'r':
        line =f.readline()
        temp=line.split()
        h=int(temp[0])
        w=int(temp[1])
        temp.clear()
        for row in range(h):
            line = f.readline()
            for number in line.split():
                map_game.append(int(number))
        line =f.readline()
        pac_man=[]
        for x in line.split():
            pac_man.append(int(x))
        f.close()
        pos = pac_man[0]*w+pac_man[1]
    return [map_game,pos,w,h]
def lv1_2_heuristic(pos,des,w,h):
    return abs(pos%w - des%w)+abs(pos//w - des//w)
def Take_Prior(element):
    return element[2]


# In[32]:


def Lv12_A_Star(path):
    exp_list=[]
    frontier=[]
    son=[]
    comp=False
    [arr,start,w,h]=loadmap_search(path)
    food = arr.index(2)
    frontier.append([start,start,lv1_2_heuristic(start,food,w,h)])
    while(len(frontier)>0):
        son.clear()
        cur=frontier[0]
        exp_list.append([cur[0],cur[1]])
        if cur[0]==food :
            frontier.pop(0)
            comp=True
            break
        if (cur[0]-1)%w !=(w-1) and (cur[0]-1)>=0:
            son.append(cur[0]-1)
        if (cur[0]+1)%w !=0:
            son.append(cur[0]+1)
        if (cur[0]-w)>=0:
            son.append(cur[0]-w)
        if (cur[0]+w)<w*h:
            son.append(cur[0]+w)
        for i in son:
            check=True
            if arr[i]!=0 and arr[i]!=2:
                check=False
            if check:
                for z in exp_list:
                    if i==z[0]:
                        check=False
                        break
            if check :
                for z in frontier:
                    if int(i)==z[0]:
                        Prior= lv1_2_heuristic(i,food,w,h)+cur[2]-lv1_2_heuristic(cur[0],food,w,h)+1
                        if Prior<z[2]:
                            z=[int(i),cur[0],Prior]
                        check=False
                        break
            if check :
                Prior= lv1_2_heuristic(i,food,w,h)+cur[2]-lv1_2_heuristic(cur[0],food,w,h)+1
                frontier.append([i,cur[0],Prior])
        frontier.pop(0)
        frontier.sort(key=Take_Prior)
    if comp==False:
        return 'Can not escape the maze!!!'
    re_path=[]
    cur=exp_list[-1]
    while(cur[0]!=start):
        re_path.append(cur[0])
        for i in exp_list:
            if i[0]==cur[1]:
                cur=i
                break
    re_path.append(start)
    re_path.reverse()
    re_path_2d=[]
    for i in re_path:
        re_path_2d.append([i//w,i%w])
    return re_path_2d


# In[33]:




# In[ ]:




