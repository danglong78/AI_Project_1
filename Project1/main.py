from graph import *
from level3_4 import *

map=Map("15x20.txt")
# level 1 và level 2 thì dùng hàm này
path=Lv12_A_Star("15x20.txt")
result=map.level1_2(path)
# level 3 thì dùng hàm này
#[pm_path,ghost_path]=lv3('15x20.txt')
#map.level3(pm_path,ghost_path)
# tra ve path cua pacman va list cac path cua moster
map.print_result(result)
done()
