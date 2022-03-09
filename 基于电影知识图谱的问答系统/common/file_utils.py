import os
def get_file_list(source_path):
    file_path_list = []
    file_name = []
    walk = os.walk(source_path)
    for root,dirs,files in walk:
        for name in files:
            filepath = os.path.join(root,name)
            file_name.append(name)
            file_path_list.append(filepath)
    return file_path_list

# for root,dirs,files in os.walk(os.path.join(constant.DATA_DIR,"question")):
#     print("root",root)
#     print("dirs",dirs)
#     print("files",files)
#这个函数的目的就是获取 root E:\面试工作\基于电影知识图谱的问答系统\data\questionfiles ['question_classification.txt', 'vocabulary.txt', '【0】评分.txt',