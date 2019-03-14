#读取txt文件每一行内容，并进行空格分割，获取最后一个字符串内容
#path1为txt文件，path2为存储文件

path1 = 'F:\\test.txt'

path2 = 'F:\\test1.txt'


def get_last_information(path1,path2):
    content = open(path2,'w')
    with open(path1) as f:
        for line in f.readlines():
            s = str(line).split(" ")
            if 'song' in s:
                content.write(str((s[-1])))
    content.close()


if __name__ == '__main__':
	get_last_information(path1,path2)