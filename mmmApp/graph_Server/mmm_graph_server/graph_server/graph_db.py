from graph_server import graph


class Student(object):
    student_id = 0
    name = ""
    surname = ""
    faculty = ""
    is_mentor = False

    def __init__(self, student_id, name, surname, faculty, is_mentor):
        self.student_id = student_id
        self.name = name
        self.surname = surname
        self.faculty = faculty
        self.is_mentor = is_mentor


class Question(object):
    question = ""

    def __init__(self, question):
        self.question = question


def load_data(data_dict):
    for faculty in data_dict:
        print(faculty)


def create_students(students):
    '''
    :param students: student dictionary in the following format
            "students":[{
                         "id": 100xxxxxx,
                         "name": "student_name",
                         "surname": "student_surname",
                         "faculty": "student_faculty",
                         "is_mentor: False/True
                         "answered": [{
                                      "question":{
                                                  "question_name": question,
                                                  "question_answer": answer (0...4)
                                                  }
                                      },
                                      {
                                      "question":{
                                                  "name": question,
                                                  "answer": answer (0...4)
                                                 }
                                      },
                                      ...
                                     }]
                        }
                        ...
            }]

    :return:
    '''

    stmt = """
WITH {json} as data
UNWIND data.students as s
MERGE (p:Person {student_id:s.id}) ON CREATE
  SET p.student_id = s.id, p.name = s.name, p.surname = s.surname, p.faculty = s.faculty, p.is_mentor = s.is_mentor

FOREACH (a IN s.answered |
  MERGE (p)-[:ANSWERED {answer:a.answer}]-(q:Question {question_name: a.name})
  )
"""
    # Open transaction
    tx = graph.begin()
    #stmt = """CREATE (n:Person {name:{NAME}, surname:{SURNAME}, isTutor:{isTutor}})"
    #for student in students:
        #tx.run(stmt, {"NAME": student.name, "SURNAME": student.surname, "isTutor": student.isTutor})
    # Commit transaction
    tx.run(stmt, json=students)
    tx.commit()


def create_questions(questions):
    """
    :param questions: dictionary with all questions in the following format:
        "questions": [{
                      "name": question
                     },
                     {
                      "name": question
                     },
                     ...
                    ]
    :return:
    """
    stmt = """
WITH {json} as data
UNWIND data.questions as question
MERGE (id:UniqueId{name:'Question'})
    ON CREATE SET id.count = 1
    ON MATCH SET id.count = id.count + 1
    WITH id.count as uid, question
MERGE (q:Question {name:question.name}) ON CREATE
  SET q.id = uid
"""
    tx = graph.begin()
    #stmt = "CREATE (n:Question {name:{NAME}})"
    #for question in questions:
    #    tx.run(stmt, {"NAME": question.name})
    tx.run(stmt, json=questions)
    tx.commit()


'''
def create_students_question_relationship(students, questions):
    stmt = "MATCH (p:Person {name:{PNAME}, surname:{PSURNAME}}), (q:Question {name:{QNAME}}) CREATE (p)-[:ANSWERED {answer:{ANSWER}}]->(q)"
    tx = graph.begin()
    for rows in ws.iter_rows(min_col=4, max_col=ws.max_column, min_row=2, max_row=ws.max_row):
        for cell in rows:
            student = studentsArray[cell.row - 2]
            question = questionArray[opExcel.utils.column_index_from_string(cell.column) - 4]
            tx.run(stmt, {"PNAME": student.name,
                          "PSURNAME": student.surname,
                          "QNAME": question.name,
                          "ANSWER": cell.value
                          })
    tx.commit()
'''

''' Should we keep similarity in our database?
def create_similarity(students):
    # stmt = ("MATCH (p1:Person {name:{P1NAME}, surname:{P1SURNAME}}), "
    #             "(p2:Person {name:{P2NAME}, surname:{P2SURNAME}}) "
    #            "MERGE (p1)-[:SIMILARITY {euclidian:{ANSWER}}]-(p2)")

    stmt = (
        "MATCH (p1:Person {name:{P1NAME}, surname:{P1SURNAME}})-[x:ANSWERED]->(m:Question)<-[y:ANSWERED]-(p2:Person {isTutor:false})"
        "WITH  SUM((x.answer - y.answer)^2) AS xyDotProduct,"
        "p1, p2 "
        "MERGE (p1)-[s:SIMILARITY]-(p2) "
        "SET s.euclidean = SQRT(xyDotProduct)")

    for student in students:
        tx = graph.begin()
        if student.is_mentor:
            tx.run(stmt, {"P1NAME": student.name,
                          "P1SURNAME": student.surname
                          })
        tx.commit()
'''

'''
def create_group_relationship():
    stmt = ("")
'''