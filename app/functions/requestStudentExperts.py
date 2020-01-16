import canvas_api_caller as canvas
from flask import Flask, jsonify, request
from werkzeug.datastructures import MultiDict
import json
import os
import psycopg2




# Add "self" parameter when working with Google Cloud.
#@app.route('/requestStudentExpert', methods=['POST'])
def requestStudentExperts(request):

    #sets headers for cors
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type, x-canvas-authorization '
    }
    if request.method == 'OPTIONS':
        return '', 204, headers

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    #read json from request
    jsonobject = request.get_json("force=true")

    #calling canvas user account
    access_token = request.headers.get('X-Canvas-Authorization');
    canvas.translate_access_token(access_token)
    result = canvas.call(access_token, "users/self", MultiDict())
    decoded_response = json.loads(result)
    #get user id
    id = decoded_response['message']['id']

    #get outcomeId
    courseId = jsonobject["courseId"]
    rubricId = jsonobject["rubricId"]
    outcomeId = jsonobject["outcomeId"]
    str = f"courses/{courseId}/rubrics/{rubricId}";
    rubric = canvas.call(access_token, str, MultiDict())
    decoded_response = json.loads(rubric)

    #get outcome from rubric
    outcomes = decoded_response['message']['data']
    foundOutcome = None;
    for i in range(len(outcomes)):
        if outcomes[i]["id"] == outcomeId:
            foundOutcome = outcomes[i]

    #find not empty description
    for i in range(len(foundOutcome['ratings'])):
        temp = foundOutcome['ratings'][i]['long_description']
        if temp != '':
            description = temp;


    #connect and commit to database
    conn = psycopg2.connect(os.environ.get('DATABASE_URI'))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.expertrequest WHERE userId=%s AND KPI=%s;", (id, foundOutcome['description']))
    expertRequest = cursor.fetchone()
    if expertRequest is None:
        cursor.execute("INSERT INTO public.expertrequest(userId,KPI,description) values(%s,%s,%s);", (id, foundOutcome['description'] ,description))
        conn.commit()
    cursor.close()
    conn.close()

    #return succes
    return "succes",200, headers
