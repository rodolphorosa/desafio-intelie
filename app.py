from flask import Flask, request, render_template, flash, redirect, session
from markupsafe import escape
from datetime import datetime

from schemaFacts import SchemaFacts
from xmlHandler import DataHandler, HistoryHandler, UserHandler

import os

app = Flask(__name__, template_folder='template')


@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["password"]
        user = user_handler.retrieve_user(username, password)

        if user is None:
            flash("Username or password incorrect!")
            return redirect("/login")
        else:
            session['user'] = user
            return redirect('/home')

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


@app.route("/home")
def home():
    if 'user' in session:
        flash('You are logged in as %s' %escape(session['user']['username']))
        return render_template("index.html", schema=sf.get_schema(), facts=sf.get_facts())
    else:
        flash("You are not logged in!")
        return redirect('/login')


@app.route("/facts")
def get_facts():
    current_facts = []
    for fact in sf.get_current_facts():
        current_facts.append({
            "entity": fact[0].replace('/', '%2F'),
            "attribute": fact[1],
            "value": fact[2]
        })
    return render_template("facts.html", facts=current_facts)


@app.route("/schema")
def get_schema():
    attributes = []
    for attribute in sf.get_schema():
        attributes.append({
            "name": attribute[0],
            "cardinality": attribute[2]
        })
    return render_template("schema.html", schema=attributes)


@app.route("/add_fact", methods=["POST"])
def add_fact():
    if request.method == "POST":
        if session['user']['role'] == 'admin':
            entity = request.form["entity"]
            attribute = request.form["attribute"]
            value = request.form["value"]
            try:
                sf.insert_fact(entity, attribute, value)
                data_handler.save_data(sf.get_schema(), sf.get_facts())
                insertion = {
                    "action": "insertion",
                    "entity": entity,
                    "attribute": attribute,
                    "value": value,
                    "datetime": datetime.now().strftime("%y/%m/%d %H:%M:%S")
                }
                history_handler.register_modification(insertion)
                flash("Fact successfully added.")
            except Exception as e:
                flash(str(e))
        else:
            flash("You need admin role to perform this action.")
        return redirect('/facts')


@app.route("/add_attribute", methods=["POST"])
def add_schema():
    if request.method == "POST":
        if session['user']['role'] == 'admin':
            try:
                attribute = request.form["attribute"]
                cardinality = request.form["cardinality"]
                sf.insert_attribute(attribute, cardinality)
                data_handler.save_data(sf.get_schema(), sf.get_facts())
                flash("Attribute successfully added.")
            except Exception as e:
                flash(str(e))
        else:
            flash("You need admin role to perform this action.")
        return redirect('/schema')


@app.route("/update_schema/<attribute_name>")
def update_schema_form(attribute_name):
    if session['user']['role'] == 'admin':
        attribute = sf.get_attribute(attribute_name)
        return render_template("update-schema.html", attribute={"name": attribute[0], "cardinality": attribute[2]})
    else:
        flash("You need admin role to perform this action.")
        return redirect('/schema')


@app.route("/update_attribute", methods=["POST"])
def update_attribute():
    if request.method == "POST":
        try:
            attribute = request.form["attribute"]
            cardinality = request.form["cardinality"]
            sf.update_attribute(attribute, cardinality)
            data_handler.save_data(sf.get_schema(), sf.get_facts())
            flash("Attribute successfully update.")
        except Exception as e:
            flash(str(e))
        return redirect('/schema')


@app.route("/delete_attribute/<attribute>")
def delete_attribute(attribute):
    if session['user']['role'] == 'admin':
        try:
            sf.delete_attribute(attribute)
            data_handler.save_data(sf.get_schema(), sf.get_facts())
            flash("Attribute successfully deleted.")
        except Exception as e:
            flash(str(e))
    else:
        flash("You need admin role to perform this action.")
    return redirect('/schema')


@app.route("/delete_fact/<entity>/<attribute>/<value>")
def delete_fact(entity, attribute, value):
    if session['user']['role'] == 'admin':
        entity = entity.replace('%2F', '/')
        try:
            sf.delete_fact(entity, attribute, value)
            data_handler.save_data(sf.get_schema(), sf.get_facts())
            deletion = {
                "action": "deletion",
                "entity": entity,
                "attribute": attribute,
                "value": value,
                "datetime": datetime.now().strftime("%y/%m/%d %H:%M:%S")
            }
            history_handler.register_modification(deletion)
            flash("Fact successfully deleted")
        except Exception as e:
            flash(str(e))
    else:
        flash("You need admin role to perform this action.")
    return redirect("/facts")


@app.route("/history/<entity>")
def detail_entity(entity):
    entity = entity.replace("%2F", "/")
    history = history_handler.retrieve_entity_modification_history(entity)

    if history is not None and len(history) > 0:
        return render_template("history.html", history=history)

    return render_template("history.html")


if __name__ == "__main__":
    xml_dump_file = "data/dump.xml"
    xml_user_file = "data/users.xml"
    xml_history_file = "data/history.xml"

    data_handler = DataHandler("data/dump.xml")
    schema, facts = data_handler.restore_data()

    user_handler = UserHandler("data/users.xml")
    history_handler = HistoryHandler("data/history.xml")

    sf = SchemaFacts(schema, facts)

    app.secret_key = 'super secret key'
    app.config["DEBUG"] = True
    app.run()

    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
