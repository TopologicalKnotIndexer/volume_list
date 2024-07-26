# 桥接：https://github.com/TopologicalKnotIndexer/name_to_pd_code
import os
DIRNOW = os.path.dirname(os.path.abspath(__file__))
SUBDIR = os.path.join(DIRNOW, "name_to_pd_code", "src") # 子包路径

# ======================================== BEGIN IMPORT FROM PATH ======================================== #
import importlib
import json
import sys
def load_module_from_path(path: str, mod_name: str): # 从指定路径导入一个包
    assert os.path.isdir(path)                       # 路径必须存在
    path         = os.path.abspath(path)             # 获得绝对路径
    old_sys_path = json.loads(json.dumps(sys.path))  # 存档旧的 sys.path
    sys.path     = [path] + sys.path                 # 将新的路径加入 sys.path
    mod          = importlib.import_module(mod_name) # 加载指定的包
    sys.path     = old_sys_path                      # 恢复旧的 sys.path
    return mod
# ======================================== END IMPORT FROM PATH ======================================== #

def name_to_pd_code(knotname: str) -> list:
    return load_module_from_path(SUBDIR, "get_knot_pd_code_by_name").get_knot_pd_code_by_name(knotname)

if __name__ == "__main__":
    print(name_to_pd_code("K3a1,K5a1"))