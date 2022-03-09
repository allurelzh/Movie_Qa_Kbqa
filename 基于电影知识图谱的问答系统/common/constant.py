#常量abspath代表的是绝对路径 __file__代表当前文件的地址，os.pardir代表其父目录
import os
BASE_DIR = os.path.abspath(os.path.join(__file__,os.pardir,os.pardir))
DATA_DIR = os.path.join(BASE_DIR,'data')