import canvas_api_caller as canvas
from flask import Flask, jsonify, request
from werkzeug.datastructures import MultiDict
import json
import os
import psycopg2



#@app.route('/addUser', methods=['GET'])
def addUser(request):
    access_token = request.headers.get('X-Canvas-Authorization')
    canvas.translate_access_token(access_token)
    result = canvas.call(access_token, "/users/self", MultiDict())
    decoded_response = json.loads(result)
    id = decoded_response['message']['id']
    conn = psycopg2.connect(os.environ.get('DATABASE_URI'))
    cursor = conn.cursor();
    cursor.execute("SELECT * FROM public.user WHERE id=%s;", [id])
    user = cursor.fetchone()
    if user is None:
        name = decoded_response['message']['name'];
        cursor.execute("INSERT INTO public.user(id,name) values(%s,%s);", (id, name))
        conn.commit()
        cursor.execute("SELECT * FROM public.user WHERE id=%s;", [id])
        user = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(user)
