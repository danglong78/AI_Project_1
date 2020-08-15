from graph import *
from level3_4 import *
from search import *
level=int(input("Mời bạn nhập level: "))
result=False
filename=input("Mời bạn nhập tên File input: ")
map=Map(filename)
if level==1 or level==2:
    path=Lv12_A_Star(filename)
    result=map.level1_2(path)
if level==3:
    [pm_path,ghost_path]=lv3(filename)
    temp=int(input("Nhập 1 nếu bạn muốn bản độ hiện ra hết.\n Nhập 2 nếu bạn muốn bản đồ chỉ hiện phần Pacman thấy\n Mời bạn chọn:   "))
    if temp==1:
        result=map.level3_4_show(pm_path,ghost_path)
    if temp==2:
        result=map.level3_4_hide(pm_path,ghost_path)

if level==4:
    [pm_path,ghost_path]=lv4(filename)
    temp=int(input("Nhập 1 nếu bạn muốn bản độ hiện ra hết.\n Nhập 2 nếu bạn muốn bản đồ chỉ hiện phần Pacman thấy\n Mời bạn chọn:   "))
    if temp==1:
        result=map.level3_4_show(pm_path,ghost_path)
    if temp==2:
        result=map.level3_4_hide(pm_path,ghost_path)
# tra ve path cua pacman va list cac path cua moster
map.print_result(result)
done()
