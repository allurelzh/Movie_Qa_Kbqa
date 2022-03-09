import jieba,os,re
from common import file_utils,constant,nlp_util
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
class QuestionClassify:
    def __init__(self):
        self.train_x,self.train_y = load_train_data()
        # 文本向量化
        self.tfidf_vec = TfidfVectorizer()
        self.train_vec = self.tfidf_vec.fit_transform(self.train_x).toarray()
        self.model = self.train_model_nb()
    #训练模型
    def train_model_nb(self):
        nb = MultinomialNB()
        nb.fit(self.train_vec,self.train_y)
        return nb
    #预测分类
    def predict(self,question):
        text_cut_gen = nlp_util.posseg(question)
        #原始问题
        text_src_list = []
        #一般化问题
        text_normal_list = []
        for item in text_cut_gen:
            text_src_list.append(item.word)
            if item.flag in ['nr','nm','ng']:
                text_normal_list.append(item.flag)
            else:
                text_normal_list.append(item.word)
        question_normal = [" ".join(text_normal_list)]
        question_vector = self.tfidf_vec.transform(question_normal).toarray()
        predict = self.model.predict(question_vector)[0]
        return predict

def load_train_data():
    train_x = []
    train_y = []
    file_path_list = file_utils.get_file_list(os.path.join(constant.DATA_DIR,"question"))
    # print(file_path_list)
    for file_item in file_path_list:
        #获取文件名中的label  re.sub是替换函数，下面函数的意思是将非数字的内容全部替换为空
        label = re.sub(r'\D',"",file_item)
        if label.isnumeric():
            label_num = int(label)
        #读取文件内容
            with open(file_item,"r",encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    #分词
                    word_list = list(jieba.cut(str(line).strip()))
                    train_x.append(" ".join(word_list))
                    train_y.append(label_num)
    return train_x,train_y




