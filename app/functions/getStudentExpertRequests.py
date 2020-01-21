import canvas_api_caller as canvas
from flask import Flask, jsonify, request
from werkzeug.datastructures import MultiDict
import json
import os
import psycopg2
import psycopg2.extras



# Add "self" parameter when working with Google Cloud.
#@app.route('/requestStudentExpert', methods=['POST'])
def getStudentExpertRequests(request):

    #sets headers for cors
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type, x-canvas-authorization '
    }
    if request.method == 'OPTIONS':
        return '', 204, headers

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    #calling canvas user account
    access_token = request.headers.get('X-Canvas-Authorization');
    canvas.translate_access_token(access_token)
    result = canvas.call(access_token, "users/self", MultiDict())
    decoded_response = json.loads(result)
    #get user id
    id = decoded_response['message']['id']



    #connect and commit to database
    conn = psycopg2.connect(os.environ.get('DATABASE_URI'), cursor_factory=psycopg2.extras.DictCursor)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT userId, kpi, description, id FROM public.expertrequest WHERE userId=%s;", [id])
    expertRequests = []
    for row in cursor:
        print(row)
        dict = {
            "userId": row[0],
            "kpi": row[1],
            "description": row[2],
            "id": row[3]
        }
        expertRequests.append(dict)
    cursor.close()
    conn.close()


    #return succes
    return jsonify(expertRequests),200, headers
