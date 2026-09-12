from flask import Flask, flash, redirect, render_template, request

from models.contact_model import Contact
from services.contact_service import ContactService

app = Flask("__name__")
app.secret_key = "secret-key"

CONTACTS_ENDPOINT: str = "/contacts"
NEW_CONTACT_ENDPOINT: str = f"{CONTACTS_ENDPOINT}/new"
service = ContactService()


@app.route("/")
def index():
    return redirect(CONTACTS_ENDPOINT)


@app.route(CONTACTS_ENDPOINT)
def contacts():
    search = request.args.get("q")
    if search is not None:
        contacts_set = service.get_by_any(search)
    else:
        contacts_set = service.all()
    return render_template("index.html", contacts=contacts_set)


@app.route(NEW_CONTACT_ENDPOINT, methods=["GET"])
def contacts_new_get():
    return render_template("new.html", contact=Contact())


@app.route(NEW_CONTACT_ENDPOINT, methods=["POST"])
def contacts_new():
    c = Contact(
        first=request.form['first_name'],
        last=request.form['last_name'],
        phone=request.form['phone'],
        email=request.form['email'])

    save = service.create(c)

    if save:
        flash("Created New Contact!", category="info")
        return redirect(CONTACTS_ENDPOINT)

    return render_template("new.html", contact=c)


@app.route("/contacts/<contact_id>", methods=["GET"])
def contacts_view(contact_id: int):
    c = service.get_by_id(contact_id)
    return render_template("show.html", contact=c)


@app.route("/contacts/<contact_id>/edit", methods=["GET"])
def contacts_edit_get(contact_id: int):
    c = service.get_by_id(contact_id)
    return render_template("edit.html", contact=c)


@app.route("/contacts/<contact_id>/edit", methods=["POST"])
def contacts_edit():
    contact = Contact(
        first=request.form['first_name'],
        last=request.form['last_name'],
        phone=request.form['phone'],
        email=request.form['email'])
    update_contact = service.update(contact)

    if update_contact:
        flash("CONTACT UPDATED!")
        return redirect(CONTACTS_ENDPOINT)

    return render_template("edit.html", contact=update_contact)
