import argparse
import os

parser = argparse.ArgumentParser()#创建一个解析对象

#向该对象中添加你要关注的命令行参数和选项
parser.add_argument("-v","--verbosity",help="increase output verbosity")

args = parser.parse_args()#进行解析

path1 = args.verbosity

path2 = os.path.join(path1,'test')

print(path2)