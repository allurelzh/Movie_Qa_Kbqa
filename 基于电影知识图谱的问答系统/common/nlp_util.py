import jieba,re
import jieba.posseg
from common import  constant
def posseg(text):
    '''
    词性标注
    res = posseg("章子怡演过哪些电影？")
    章子怡/nr演/v过/ug哪些/r电影/n
    '''
    jieba.load_userdict(constant.DATA_DIR+"/userdict3.txt")
    #清洗数据
    clean_text = re.sub("[\s+\.\!\/_,$^*(+\"\')]+|[()?【】？“”！，。~@#（）%.....)]","",text)
    #分词
    text_cut = jieba.posseg.cut(clean_text)
    return text_cut
def question_posseg(question):
    jieba.load_userdict(constant.DATA_DIR+"/userdict3.txt")
    clean_text = re.sub("[\s+\.\!\/_,$^*(+\"\')]+|[()?【】？“”！，。~@#（）%.....)]", "", question)
    qustion_seged = jieba.posseg.cut(clean_text)
    result = []
    question_word,question_flag = [],[]
    for w in qustion_seged:
        temp_word=f"{w.word}/{w.flag}"
        result.append(temp_word)
        #预处理问题
        word,flag = w.word,w.flag
        question_word.append(str(word).strip())
        question_flag.append(str(flag).strip())
    assert len(question_flag) == len(question_word)
    return result

if __name__ =="__main__":
    res = posseg("章子怡演过哪些电影？")
    for s in res:
        print(s)
    result = question_posseg("花样年华和英雄的电影评分是多少")
    #['章子怡/nr', '演/v', '过/ug', '哪些/r', '电影/n']
    print(result)
    # pass