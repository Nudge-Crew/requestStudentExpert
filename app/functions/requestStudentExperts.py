import canvas_api_caller as canvas
from flask import Flask, jsonify, request
from werkzeug.datastructures import MultiDict
import json
import os
import psycopg2

app = Flask(__name__)


# Add "self" parameter when working with Google Cloud.
#@app.route('/requestStudentExpert', methods=['POST'])
def requestStudentExperts(request):
    jsonobject = request.get_json();
    access_token = request.headers.get('X-Canvas-Authorization');
    canvas.translate_access_token(access_token);

    result = canvas.call(access_token, "users/self", MultiDict())
    decoded_response = json.loads(result)
    id = decoded_response['message']['id']
    kpi = jsonobject.get("KPI")
    description = "test"
    conn = psycopg2.connect(os.environ.get('DATABASE_URI'))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO public.expertrequest(userId,KPI,description) values(%s,%s,%s);", (id, kpi, description))
    conn.commit()
    cursor.close()
    conn.close()
    print(id)
    return kpi