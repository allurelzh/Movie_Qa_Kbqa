from model import question_template,question_classify_model
class QuestionService:
    '''
    问答核心类：接受自然问句，构造查询语句，输出答案
    '''
    def __init__(self):
        self.classify_model = question_classify_model.QuestionClassify()
        self.question_template = question_template.QuestionTemplate()
    def get_answer(self,question):
        #通过分类器获取问句的分类
        question_category = self.classify_model.predict(question)
        #根据分类和模板获取答案
        try:
            answer = self.question_template.get_question_answer(question,question_category)
        except BaseException as e:
            answer = "抱歉，没有查询到相关内容"
        return answer

question_instance = QuestionService()