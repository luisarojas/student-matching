from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import requests
from py2neo import Graph

import os

app = Flask(__name__)
api = Api(app)

#Create auth endpoint
AUTH_ENDPOINT = ('http://' +
			  os.getenv('AUTH_SERVER_HOST') +
			  ':' +
			  os.getenv('AUTH_SERVER_PORT') +
			  '/auth/status')

PORT = os.getenv('SERVER_PORT', 5002)

#Connect to the graph
#graph = Graph("bolt://localhost:7687/db/data")
graph = Graph(bolt=True,
              host=os.getenv('DB_HOST', 'localhost'),
              user=os.getenv('DB_USER', 'neo4j'),
              password=os.getenv('DB_PSWD'))

def checkToken(token):
	print("Checking token")
	s = requests.Session()	
	s.headers.update({"Content-Type":"application/json"})
	s.headers.update({"Authorization": "Bearer " + token})
	response = s.get(AUTH_ENDPOINT)
	print(list(response))
	return response

class Students(Resource):
	def get(self):
		try:
			print("Received")
			token = request.headers['Authorization']			
			response = checkToken(token).json()
			print("received:")			
			print(response)
			if response['status'] is 'success':
				result = graph.data("MATCH (student:Person) RETURN student")
				responseObject = {
					'status': 'success',
					'data': result
				}				
				res = jsonify(responseObject)
				res.status_code = 201
			else:
				responseObject = {
					'status': response['status'],
					'message': response['message']
				}
				print("Sendind back:")
				print(responseObject)
				print(jsonify(responseObject))
				res = jsonify(responseObject)
				res.status_code = 401
				return res
		except Exception as e:
			print(e)
			responseObject = {
				'status': 'fail',
				'message': 'Try again'
			}
			res = jsonify(responseObject)
			res.status_code = 500

class GetGroup(Resource):
	def get(self):
		tutor = {}
		#args = request.args
		#faculty = args['faculty']
		cursor = graph.run(("MATCH (p1:Person {isTutor:true})"
						"-[s:SIMILARITY]-"
						"(p2:Person {isTutor:false}) "
						"WHERE	p1.name <> p2.name "
						"WITH     p1, p2, s.euclidian AS e "
						"ORDER BY e ASC, p2 DESC "
						"RETURN   p1.name AS Person, p2.name AS Neighbor, e AS Similarity"))

		cand_pair = None
		assigned_students = []

		while cursor.forward():
			#print("test")
			cur_tutor = cursor.current()['Person']
			cur_student = cursor.current()['Neighbor']
			similarity = cursor.current()['Similarity']
			
			if cur_student in assigned_students:
				continue

			if cur_tutor not in tutor:
				tutor[cur_tutor] = []

			if cand_pair is not None:
				if cand_pair[1] == cur_student and cand_pair[2] == similarity:
					if len(tutor[cand_pair[0]]) > len(tutor[cur_tutor]):
                              #print("Changing " + cand_pair[0] + " to " + cur_tutor)
                              #print(str(len(tutor[cand_pair[0]])) + " > " + str(len(tutor[cur_tutor])))
						cand_pair = (cur_tutor, cand_pair[1], cand_pair[2])
				else:
					tutor[cand_pair[0]].append(cand_pair[1])
					assigned_students.append(cand_pair[1])
					cand_pair = (cur_tutor, cur_student, similarity)
					continue
			else:
				if len(tutor[cur_tutor]) <= 5:
					print("Assigning to " + cur_tutor)
					cand_pair = (cur_tutor, cur_student, similarity)
				continue
		
			if len(tutor[cur_tutor]) <= 5:
				print("Assigning " + cur_student + " to " + cur_tutor + " " + str(len(tutor[cur_tutor])))
				if cur_student not in assigned_students:
					#Save as possible solution
					candidate_pair = (cur_tutor, cur_student, similarity)

		#print(tutor)
		return tutor

api.add_resource(Students, '/students') # Route_1
api.add_resource(GetGroup, '/groups') # Route_1

#api.add_resource('student.txt','/download')
if __name__ == '__main__':
     app.run(host='0.0.0.0', port= int(PORT))

