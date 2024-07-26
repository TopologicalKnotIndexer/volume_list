# 不要执行此文件
# 此文件只用于生成常见复合扭结的 volume 列表
import os
try:
    from tqdm import tqdm
except:
    tqdm = lambda x:x # 如果没有 tqdm 的进度条，那就凑合跑一下
DIRNOW   = os.path.dirname(os.path.abspath(__file__))
KNOTLIST = os.path.join(DIRNOW, "combined_knot_name.txt")
INFOLIST = os.path.join(DIRNOW, "volume_info_list.txt")
assert os.path.isfile(KNOTLIST)

from name_to_pd_code import name_to_pd_code
from get_volume      import get_volume

def main():
    lines = list(open(KNOTLIST))
    fp    = open(INFOLIST, "w")
    for idx in tqdm(range(len(lines))):
        line = lines[idx].strip()
        if line == "" or line[0] == "#": # 跳过空行以及井号开头的行
            continue
        if idx in [1733, 1734, 1735]: # 这几个例子会让 sanpypy 的 volume 函数卡住
            volume = "non_hyperbolic"
        else:
            pd_code = name_to_pd_code(line)
            volume  = get_volume(pd_code)
        if isinstance(volume, float): # 浮点数保留二十位小数，将来也是要通过 EPS 比较的
            volume = "%.20f" % volume
        fp.write("[%s|%s]\n" % (line, volume))
        fp.flush()

if __name__ == "__main__":
    main()
