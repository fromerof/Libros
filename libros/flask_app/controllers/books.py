from flask import render_template,redirect,request,session
from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book


@app.route("/books")
def books():
    books = Book.get_all()
    return render_template("index.html",books=books)

@app.route("/addBook")
def addBook():
    books = Book.get_all()
    return render_template("books.html",books=books)


@app.route("/create_book", methods=["POST"]) 
def create_book():
    Book.save(request.form)
    return redirect("/addBook")


@app.route("/showAllbooks/<int:id>") #######
def showAllbooks(id):
    data = {
        "id": id
    }
    return render_template("/show_books.html", books = Book.
    getBook_withAuthor(data), unfavorited_authors = Author.unfavorited_authors(data))

@app.route("/join/author",methods=["POST"])
def join_author():
    data = {
        "author_id": request.form["author_id"],
        "book_id": request.form["book_id"]
    }
    Author.add_favorite(data)
    return redirect (f"/showAllbooks/{request.form['book_id']}")
