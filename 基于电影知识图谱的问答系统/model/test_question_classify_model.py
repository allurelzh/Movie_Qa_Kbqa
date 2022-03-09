from model.question_classify_model import QuestionClassify

def test_question_classify():
    question = "演过多少电影"
    question_classify = QuestionClassify()
    result = question_classify.predict(question)
    print(f"{question}的分类是{result}")