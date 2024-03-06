import os
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

backend_host = os.getenv("BACKEND_HOST", "localhost")
backend_port = os.getenv("BACKEND_PORT", 8080)

@app.route('/', methods=['GET', 'POST'])
def index_route():
    template = "cad_user.html"
    content_title = "Cadastro de usuário"
    app.logger.info(template)

    if request.method == 'POST':
        id = request.form.get("id")
        name = request.form.get("name")
        try:
            status_code, response = create_user(id, name)
            return render_template(template, content_title=content_title, status_code=status_code, response=response)
        except Exception as e:
            app.logger.error(e)

    return render_template(template, content_title=content_title)

@app.route('/users', methods=['GET'])
def users_route():
    template = "table.html"
    content_title = "Lista de usuários cadastrados"
    app.logger.info(template)

    try:
        status_code, response = list_users()
        if response is None:
            response = ""

        return render_template(template, content_title=content_title, status_code=status_code, users=response)

    except Exception as e:
        app.logger.error(e)

@app.route('/user/delete/<id>', methods=['GET'])
def delete_user_route(id):
    app.logger.info("delete_user_route(" + str(id) +")")
    content_title = "Erro ao deletar usuário - status_code:"
    try:
        status_code = delete_user(id)

        if status_code == 200:
            return redirect(url_for('users_route'))
        else:
            app.logger.info('delete_user_route("{}") >> ERROR - status_code: {}'.format(id, status_code))
            return render_template("error.html", content_title=content_title, status_code=status_code)

    except Exception as e:
        app.logger.error(e)  

@app.route('/healthz', methods=['GET'])
def health_route():
    return jsonify({"frontend_status": "ok", "backend_status": "{}".format(backend_status())})

def backend_status():
    try:
        url = "http://{}:{}/healthz".format(backend_host, backend_port)
        app.logger.info(url)
        r = requests.get(url)
        return "ok"
    except Exception as e:
        app.logger.error(e)
        return "nok"

def create_user(id, name):
    app.logger.info("Received id: %s, name: %s", id, name)
    try:
        url = "http://{}:{}/users".format(backend_host, backend_port)
        json = {"id": int(id), "name": "{}".format(name)}
        app.logger.info("Url {}, Payload {}".format(url, json))

        r = requests.post(url, json=json)
        if r.status_code == 200:
            status_code, response = r.status_code, r.json()
        else:
            status_code, response = r.status_code, None
        
        app.logger.info("Result code {}, Reponse {}".format(status_code, response))
        return status_code, response

    except Exception as e:
        app.logger.error(e)

def list_users():
    app.logger.info("List users:")
    try:
        url = "http://{}:{}/users".format(backend_host, backend_port)
        app.logger.info("Url {}".format(url))

        r = requests.get(url)
        if r.status_code == 200:
            status_code, response = r.status_code, r.json()
        else:
            status_code, response = r.status_code, None
        
        app.logger.info("Result code {} ||| Reponse {}".format(status_code, response))
        return status_code, response

    except Exception as e:
        app.logger.error(e)

def delete_user(id):
    app.logger.info("def delete_user")
    try:
        url = "http://{}:{}/users/{}".format(backend_host, backend_port, id)
        app.logger.info("Url {}".format(url))

        r = requests.delete(url)
        if r.status_code == 200:
            status_code = r.status_code
        else:
            status_code = r.status_code
        
        app.logger.info("Result code {}".format(status_code))
        return status_code

    except Exception as e:
        app.logger.error(e)
        

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)