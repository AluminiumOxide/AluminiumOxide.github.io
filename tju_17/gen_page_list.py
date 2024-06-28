import os

# 用于生成markdown列表文件,懒的手操了
if __name__ == '__main__':
    gen_path = []  # 存储相对路径 :[[当前目录,时间目录,md文件名],...]
    gen_dict = {}   # 文件夹集合  :{时间目录:生成内容,...}

    #step1遍历本目录 和 本目录下的目录,并遍历下一层目录的md文件
    current_dir = os.getcwd()
    base_dir = os.path.basename(current_dir)  # 本目录名称
    for time_dir in os.listdir(current_dir):      # 本目录下其他文件夹名称
        if os.path.isdir(os.path.join(current_dir, time_dir)):

            sub_path = os.path.join(current_dir, time_dir) 
            for sub_file in os.listdir(sub_path):  # 遍历文件夹下的md文件
                if os.path.isfile(os.path.join(sub_path, sub_file)) and sub_file.split('.')[-1]=='md':

                    # print(base_dir,time_dir,sub_file') # 把目录信息添加到列表里
                    gen_path.append([base_dir,time_dir,sub_file])
                    gen_dict[time_dir] = ''

    #step2 拼接字符串到文件夹集合的值里
    cache_dict = gen_dict.copy()  # 我忘记能不能一边遍历一边修改了,总之复制一份用来循环
    for key, value in cache_dict.items():  # 遍历拷贝后的字典
        gen_dict[key] = f'- {key}\n'       # 先生成一集列表
        for dir1,dir2,dir3 in gen_path:    
            if dir2 == key: # 属于本类别
                gen_dict[key] += f'  - [{dir3}](/{dir1}/{dir2}/{dir3})\n'  # 再生成二级列表


    #step3 创建文件,写入
    with open('page_list.md', 'w') as file: 
        for key, value in gen_dict.items():
            file.write(value)


