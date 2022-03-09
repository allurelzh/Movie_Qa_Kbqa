from common import nlp_util
from common.neo4j_util import Neo4jQuery
import re
class QuestionTemplate:
    def __init__(self):
        self.q_template_dict = {
            0:self.get_movie_rating,
            1:self.get_movie_releasedate,
            2:self.get_movie_type,
            3:self.get_movie_introduction,
            4:self.get_movie_actor_list,
            5:self.get_actor_info,
            6:self.get_actor_act_type_movie,
            7:self.get_actor_act_movie_list,
            8:self.get_movie_rating_bigger,
            9:self.get_movie_rating_smaller,
            10:self.get_actor_movie_type,
            11:self.get_cooperation_movie_list,
            12:self.get_actor_movie_num,
            13:self.get_actor_birthday
        }
        self.neo4j_conn = Neo4jQuery()


    def get_question_answer(self,question,template_id):
        question = nlp_util.question_posseg(question)
        question_word,question_flag = [],[]
        for one in question:
            #question_posseg分词的结果为['章子怡/nr', '演/v', '过/ug', '哪些/r', '电影/n']
            word,flag = one.split("/")
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        # print("question_word",question_word)
        # print("question_flag",question_flag)
        self.question_word = question_word
        self.question_flag = question_flag
        self.raw_question = question
        answer = self.q_template_dict[template_id]()
        if len(answer)<=8:
            answer = "抱歉，没有搜索到相关内容"
        return answer


    def get_movie_name(self,type_str):
        '''
        获取电影的名字
        :param type_str:
        :return:
        '''
        name_count = self.question_flag.count(type_str)
        if name_count == 1:
            # 获取nm在原问题中的下标
            tag_index = self.question_flag.index(type_str)
            # 获取问题中的电影名称
            name = self.question_word[tag_index]
            return name
        else:
            result_list = []
            for i, flag in enumerate(self.question_flag):
                if flag == str(type_str):
                    result_list.append(self.question_word[i])
            return result_list
    def get_name(self,type_str):
        #获取人物的名字
        name_count =self.question_flag.count(type_str)
        if name_count == 1:
            #获取nr在原问题中的下标
            tag_index = self.question_flag.index(type_str)
            #获取问题中的人物名称
            name = self.question_word[tag_index]
            return name
        else:
            result_list = []
            for i,flag in enumerate(self.question_flag):
                if flag==str(type_str):
                    result_list.append(self.question_word[i])
            return result_list

    #获取数字，如评分
    def get_num(self):
        x = re.sub(r"\D","","".join(self.question_word))
        return x
    def get_movie_rating(self):
        #获取电影名称，在用户输入的问题中抽取
        movie_name = self.get_movie_name("nm")
        # print(movie_name)
        if isinstance(movie_name,str):
            cql = f"match (m:Movie)-[]->() where m.title='{movie_name}' return m.rating"
            answer = self.neo4j_conn.run(cql)[0]
            answer = round(answer,2)
            final_answer = movie_name + "电影评分为" +str(answer)+"分！"
            return final_answer
        elif isinstance(movie_name,list):
            answerlist = []
            for name in movie_name:
                cql = f"match (m:Movie)-[]->() where m.title='{name}' return m.rating"
                answer = self.neo4j_conn.run(cql)[0]
                answer = round(answer, 2)
                answer_part = name + "电影评分为" + str(answer) + "分！"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_movie_releasedate(self):
        # 获取电影的上映日期，在用户输入的问题中抽取
        movie_name = self.get_movie_name("nm")
        if isinstance(movie_name, str):
            cql = f"match (m:Movie)-[]->() where m.title='{movie_name}' return m.releasedate"
            answer = self.neo4j_conn.run(cql)[0]
            final_answer = movie_name + "的上映时间是" + str(answer) + "！"
            return final_answer
        elif isinstance(movie_name, list):
            answerlist = []
            for name in movie_name:
                cql = f"match (m:Movie)-[]->() where m.title='{name}' return m.releasedate"
                answer = self.neo4j_conn.run(cql)[0]
                answer_part = name + "的上映时间是" + str(answer) + "！"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_movie_type(self):
        # 获取电影的类型信息，在用户输入的问题中抽取
        movie_name = self.get_movie_name("nm")
        if isinstance(movie_name, str):
            cql = f"match (m:Movie)-[]->(g:Genre) where m.title='{movie_name}' return g.gname"
            answer = self.neo4j_conn.run(cql)
            answer_set = set(answer)
            answer_list = list(answer_set)
            answer = "、".join(answer_list)
            final_answer = movie_name + "是" + str(answer) + "等类型的电影！"
            return final_answer
        elif isinstance(movie_name, list):
            answerlist = []
            for name in movie_name:
                cql = f"match (m:Movie)-[]->(g:Genre) where m.title='{name}' return g.gname"
                answer = self.neo4j_conn.run(cql)
                answer_set = set(answer)
                answer_list = list(answer_set)
                answer = "、".join(answer_list)
                answer_part = name + "是" + str(answer) + "等类型的电影！"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_movie_introduction(self):
        # 获取电影的内容简介，在用户输入的问题中抽取
        movie_name = self.get_movie_name("nm")
        if isinstance(movie_name, str):
            cql = f"match (m:Movie)-[]->() where m.title='{movie_name}' return m.introduction"
            answer = self.neo4j_conn.run(cql)[0]
            final_answer = movie_name + "主要讲述了" + str(answer) + "！"
            return final_answer
        elif isinstance(movie_name, list):
            answerlist = []
            for name in movie_name:
                cql = f"match (m:Movie)-[]->() where m.title='{name}' return m.introduction"
                answer = self.neo4j_conn.run(cql)[0]
                answer_part = name + "主要讲述了" + str(answer) + "！"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_movie_actor_list(self):
        #获取电影的演员信息
        movie_name = self.get_movie_name("nm")
        if isinstance(movie_name, str):
            cql = f"match (p:Person)-[r:actedin]->(m:Movie) where m.title='{movie_name}' return p.name"
            answer = self.neo4j_conn.run(cql)
            answer_set = set(answer)
            answer_list = list(answer_set)
            answer = "、".join(answer_list)
            final_answer = movie_name + "由" + str(answer) + "等演员主演！"
            return final_answer
        elif isinstance(movie_name, list):
            answerlist = []
            for name in movie_name:
                cql = f"match (p:Person)-[r:actedin]->(m:Movie) where m.title='{name}' return p.name"
                answer = self.neo4j_conn.run(cql)
                answer_set = set(answer)
                answer_list = list(answer_set)
                answer = "、".join(answer_list)
                answer_part = name + "由" + str(answer) + "等演员主演！"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_actor_info(self):
        #查询演员的简介
        actor_name = self.get_name("nr")
        if isinstance(actor_name, str):
            cql = f"match (p:Person) where p.name='{actor_name}' return p.biography"
            answer = self.neo4j_conn.run(cql)[0]
            final_answer = actor_name + ":" + str(answer) + "！"
            return final_answer
        elif isinstance(actor_name, list):
            answerlist = []
            for name in actor_name:
                cql = f"match (p:Person) where p.name='{name}' return p.biography"
                answer = self.neo4j_conn.run(cql)[0]
                answer_part = name + ":" + str(answer) + "！"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_actor_act_type_movie(self):
        #查询演员出演过的电影的类型
        actor_name = self.get_name("nr")
        if isinstance(actor_name, str):
            cql = f"match (p:Person)-[:actedin]->(m:Movie) where p.name='{actor_name}' return m.title"
            answer = self.neo4j_conn.run(cql)
            answer_set = set(answer)
            answer_list = list(answer_set)
            answer = "、".join(answer_list)
            final_answer = actor_name + "演过的电影有" + str(answer) + "等。"
            return final_answer
        elif isinstance(actor_name, list):
            answerlist = []
            for name in actor_name:
                cql = f"match (p:Person)-[:actedin]->(m:Movie) where p.name='{name}' return m.title"
                answer = self.neo4j_conn.run(cql)
                answer_set = set(answer)
                answer_list = list(answer_set)
                answer = "、".join(answer_list)
                answer_part = name + "演过的电影有" + str(answer) + "等。"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_actor_act_movie_list(self):
        #查询某个演员演过哪些电影
        actor_name = self.get_name("nr")
        if isinstance(actor_name, str):
            cql = f"match (p:Person)-[:actedin]->(m:Movie) where p.name='{actor_name}' return m.title"
            answer = self.neo4j_conn.run(cql)
            answer_set = set(answer)
            answer_list = list(answer_set)
            answer = "、".join(answer_list)
            final_answer = actor_name + "演过" + str(answer) + "等电影。"
            return final_answer
        elif isinstance(actor_name, list):
            answerlist = []
            for name in actor_name:
                cql = f"match (p:Person)-[:actedin]->(m:Movie) where p.name='{name}' return m.title"
                answer = self.neo4j_conn.run(cql)
                answer_set = set(answer)
                answer_list = list(answer_set)
                answer = "、".join(answer_list)
                answer_part = name + "演过" + str(answer) + "等电影。"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_movie_rating_bigger(self):
        #查询某演员参演的评分超过某个值的电影
        actor_name = self.get_name("nr")
        x = self.get_num()
        if isinstance(actor_name, str):
            cql = f"match (p:Person)-[:actedin]->(m:Movie) where p.name='{actor_name}' and m.rating>={x} return m.title"
            answer = self.neo4j_conn.run(cql)
            answer_set = set(answer)
            answer_list = list(answer_set)
            answer = "、".join(answer_list)
            final_answer = actor_name + "演的电影评分高于" + x +"分的有"+ str(answer) + "等!"
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_movie_rating_smaller(self):
        # 查询某演员参演的评分低于某个值的电影
        actor_name = self.get_name("nr")
        x = self.get_num()
        if isinstance(actor_name, str):
            cql = f"match (p:Person)-[:actedin]->(m:Movie) where p.name='{actor_name}' and m.rating<{x} return m.title"
            answer = self.neo4j_conn.run(cql)
            answer_set = set(answer)
            answer_list = list(answer_set)
            answer = "、".join(answer_list)
            final_answer = actor_name + "演的电影评分低于" + x + "分的有" + str(answer) + "等!"
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_actor_movie_type(self):
        # 查询演员出演过的电影的类型
        actor_name = self.get_name("nr")
        if isinstance(actor_name, str):
            cql = f"match (p:Person)-[:actedin]->(m:Movie)-[:is]->(g:Genre) where p.name='{actor_name}' return g.gname"
            answer = self.neo4j_conn.run(cql)
            answer_set = set(answer)
            answer_list = list(answer_set)
            answer = "、".join(answer_list)
            final_answer = actor_name + "演过的电影有" + str(answer) + "等类型。"
            return final_answer
        elif isinstance(actor_name, list):
            answerlist = []
            for name in actor_name:
                cql = f"match (p:Person)-[:actedin]->(m:Movie)-[:is]->(g:Genre) where p.name='{name}' return g.gname"
                answer = self.neo4j_conn.run(cql)
                answer_set = set(answer)
                answer_list = list(answer_set)
                answer = "、".join(answer_list)
                answer_part = name + "演过的电影有" + str(answer) + "等类型。"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_cooperation_movie_list(self):
        #查询两演员合作过的电影有哪些？
        actor_name_list = self.get_name("nr")
        if isinstance(actor_name_list, list) and len(actor_name_list)==2:
            x1 = actor_name_list[0]
            x2 = actor_name_list[1]
            cql = f"match (p1:Person)-[:actedin]->(m:Movie)<-[:actedin]-(p2:Person) where p1.name='{x1}' and p2.name='{x2}' return m.title"
            answer = self.neo4j_conn.run(cql)
            answer_set = set(answer)
            answer_list = list(answer_set)
            answer = "、".join(answer_list)
            final_answer = x1 + "和" + x2 + "一起合作过的电影有：" + str(answer) + "等!"
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
    def get_actor_movie_num(self):
        #查询演员演过多少部电影
        actor_name = self.get_name("nr")
        if isinstance(actor_name, str):
            cql = f"match (p:Person)-[:actedin]->(m:Movie) where p.name='{actor_name}' return count(m)"
            answer = self.neo4j_conn.run(cql)[0]
            final_answer = actor_name + "演过" + str(answer) + "部电影。"
            return final_answer
        elif isinstance(actor_name, list):
            answerlist = []
            for name in actor_name:
                cql = f"match (p:Person)-[:actedin]->(m:Movie) where p.name='{name}' return count(m)"
                answer = self.neo4j_conn.run(cql)[0]
                answer_part = name + "演过" + str(answer) + "部电影。"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer
    def get_actor_birthday(self):
        # 查询演员的出生日期
        actor_name = self.get_name("nr")
        if isinstance(actor_name, str):
            cql = f"match (p:Person) where p.name='{actor_name}' return p.birth"
            answer = self.neo4j_conn.run(cql)[0]
            final_answer = actor_name + "的生日是" + str(answer) + "。"
            return final_answer
        elif isinstance(actor_name, list):
            answerlist = []
            for name in actor_name:
                cql = f"match (p:Person) where p.name='{name}' return p.birth"
                answer = self.neo4j_conn.run(cql)[0]
                answer_part = name + "的生日是" + str(answer) + "。"
                answerlist.append(answer_part)
            final_answer = "    ".join(answerlist)
            return final_answer
        else:
            final_answer = "抱歉，没有找到相关答案。"
            return final_answer



