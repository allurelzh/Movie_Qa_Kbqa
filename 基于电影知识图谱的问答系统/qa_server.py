from flask import Flask,render_template,request
from service.question_service import question_instance
app = Flask("基于知识图谱的电影问答系统")

@app.route("/")
def index():
    answer={
        "question":"请输入搜索内容",
        "content":""
    }
    return render_template("index.html",answer=answer)
@app.route("/web_answer",methods=['POST'])
def web_answer():
    question = request.form['question']
    answer_str = question_instance.get_answer(question)
    answer = {
        "question":question,
        "content":answer_str
    }
    return render_template("index.html",answer=answer)


def start_server():
    app.run()