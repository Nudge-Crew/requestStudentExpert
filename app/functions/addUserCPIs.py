import os
import requests
import canvas_api_caller as canvas
import psycopg2
from werkzeug.datastructures import MultiDict
import json


# adds all user CPI's to the database
def addUserCPIs(request):
    # sets headers for cors
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



    # get course id from request
    jsonobject = request.get_json("force=true")
    courseId = jsonobject['courseId']

    access_token = request.headers.get('X-Canvas-Authorization');
    canvas.translate_access_token(access_token)
    result = canvas.call(access_token, "users/self", MultiDict())
    decoded_response = json.loads(result)
    # get user id
    userId = decoded_response['message']['id']


    # calling canvas user account
    done = False
    unfiltererd = []
    pageCounter = 1;
    while done == False:
        result = canvas.call(access_token, f"courses/{courseId}/rubrics?page={pageCounter}", MultiDict())
        pageCounter+=1
        decoded_response = json.loads(result)
        if decoded_response['message'] != []:
            unfiltererd.extend(decoded_response['message'])
        else:
            done = True
    CPIs = filterKPIs(unfiltererd)

    conn = psycopg2.connect(os.environ.get('DATABASE_URI'))
    cursor = conn.cursor()
    for cpi in CPIs:
        context = call_emotion_api(CPIs)
        cursor.execute("INSERT INTO public.cpi(id,userId,kpi,description,context) values(%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;",(cpi[0],userId, cpi[1], cpi[2], context))
    conn.commit()
    cursor.close()
    conn.close()

    return "okay", 200, headers





def filterKPIs(unfiltered):
    CPIs = []
    #loops through all rubrics
    for data in unfiltered:
        rubricId = data['id']
        #loops trough all CPI/KPIs
        for cpi in data['data']:
            if 'learning_outcome_id' not in cpi:
                print(cpi)
                kpidescription = cpi['description']
                id = cpi['id']
                ratingAdded = False
                for rating in cpi['ratings']:
                    if rating['long_description'] != "":
                        cpiDescription = rating['long_description']
                        cpiId = f"{rubricId}_{id}"
                        CPIs.append((cpiId,kpidescription,cpiDescription))
                        ratingAdded = True
                if(ratingAdded == False):
                    print("added")
                    cpiDescription = cpi['ratings'][1]['description']
                    CPIs.append((id,kpidescription,cpiDescription))
    return CPIs

def call_emotion_api(content):
    default_emotion_api_url = 'https://us-central1-school-230709.cloudfunctions.net/translate_data'

    data = {
        "data": content
    }

    headers = {
        'Content-Type': 'application/json'
    }

    url = requests.post(
        os.environ.get('EMOTION_API_URL', default_emotion_api_url),
        json=data,
        headers=headers
    )

    if url.status_code is 500:
        return {
            "error": "Unable to read emotions from text"
        }

    return url.json()