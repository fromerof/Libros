from flask import render_template,redirect,request,session
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book

#HOME
@app.route('/')
def index():
    return redirect("/authors")


@app.route("/authors")
def authors():
    authors = Author.get_all()
    return render_template("authors.html",authors=authors)


@app.route("/addAuthor", methods=["POST"]) 
def addAuthor():
    data = {
        "name": request.form["name"]
    }
    author_id = Author.save(data)
    return redirect("/authors")



@app.route("/showAllauthors/<int:id>") #######
def showAllauthors(id):
    data = {
        "id": id
    }
    return render_template("/show_author.html", author = Author.
    getAuthor_withBooks(data), unfavorited_books = Book.unfavorited_books(data))

@app.route("/join/book", methods = ["POST"])
def join_book():
    data = {
        "author_id": request.form["author_id"],
        "book_id": request.form["book_id"]
    }
    Author.add_favorite(data)
    return redirect(f"/showAllauthors/{request.form['author_id']}")


