from graph_server import graph
import json


def create_data(faculty):
    '''
    :param students: student dictionary in the following format
        "group": {
            "mentor-id": <int>,
            "student":[{ "student":
                            {
                             "is_mentor: False/True
                             "id": 100xxxxxx,
                             "name": <student_name>,
                             "surname": <student_surname>,
                             "email": <email>
                             "program": <program>,
                             "answers": [{
                                           "name": question,
                                           "answer": answer (0...4)
                                          },
                                          {
                                           "name": question,
                                           "answer": answer (0...4)
                                          },
                                      ...]
                            }
                        }
                     ...]
            }

    :return:
    '''

    stmt = """
WITH {json} as data
UNWIND data.Faculty as f
FOREACH (g IN f.group |
  FOREACH (s IN g.students |
    MERGE (p:Person {student_id:s.student.id}) 
      ON CREATE SET p.student_id = s.student.id, p.name = s.student.name, p.surname = s.student.surname, p.email = s.student.email, p.program = s.student.program, p.faculty = f.name, p.is_mentor = s.student.is_mentor
      ON MATCH SET  p.name = s.student.name, p.surname = s.student.surname, p.email = s.student.email, p.program = s.student.program, p.faculty = f.name, p.is_mentor = s.student.is_mentor
     
    MERGE (mentor:Person {student_id:g.mentor_id})
      ON CREATE SET mentor.student_id = g.mentor_id
         
    MERGE (p)-[:PART_OF_GROUP]-(mentor)

    FOREACH (a IN s.student.answers |
      MERGE (q:Question {question_name: a.question_name})
        ON CREATE SET q.question_name = a.question_name
      MERGE (p)-[:ANSWERED {answer:a.student_answer}]-(q)
    )
  )
)
"""
    # Open transaction
    tx = graph.begin()
    #stmt = """CREATE (n:Person {name:{NAME}, surname:{SURNAME}, isTutor:{isTutor}})"
    #for student in students:
        #tx.run(stmt, {"NAME": student.name, "SURNAME": student.surname, "isTutor": student.isTutor})
    # Commit transaction
    tx.run(stmt, json=faculty)
    tx.commit()

