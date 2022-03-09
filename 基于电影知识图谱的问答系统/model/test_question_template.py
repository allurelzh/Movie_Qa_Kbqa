from model.question_template import QuestionTemplate
def test_template():
    qs = QuestionTemplate()
    answer = qs.get_question_answer("李连杰演过多少部电影？",12)
    print(answer)