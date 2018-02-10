from flask import request, jsonify
from flask_restful import Resource

from graph_server import graph, app, api

import requests
import os

def checkToken(token):
	"""Check if the token is valid"""
	s = requests.Session()	
	s.headers.update({"Content-Type":"application/json"})
	s.headers.update({"Authorization": token})
	response = s.get(app.config.get('AUTH_DATABASE_URI'))
	return response

class Students(Resource):
	def get(self):
		try:
			token = request.headers['Authorization']			
			response = checkToken(token).json()
			if response.get('status') == 'success':
				result = graph.data("MATCH (student:Person) RETURN student")		
				responseObject = {
					'status': 'success',
					'data': result
				}				
				res = jsonify(responseObject)
				res.status_code = 201
				return res
			else:
				responseObject = {
					'status': response['status'],
					'message': response['message']
				}
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
			return res

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

# Setting the routes
api.add_resource(Students, '/students') 
api.add_resource(GetGroup, '/groups') 
