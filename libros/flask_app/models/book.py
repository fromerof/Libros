from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author


class Book:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_who_favorited = []


    @classmethod
    def save(cls,data):
        query = "INSERT INTO books (title,num_pages,created_at,updated_at) VALUES (%(title)s,%(num_pages)s,NOW(),NOW())"
        return connectToMySQL('esquema_libros').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        books_from_db =  connectToMySQL('esquema_libros').query_db(query)
        books =[]
        for b in books_from_db:
            books.append(cls(b))
        return books


    @classmethod
    def getBook_withAuthor(cls,data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"
        results = connectToMySQL('esquema_libros').query_db( query , data )    
        book = cls( results[0] )
        for row in results:
            if row['authors.id'] == None:
                break
            author_data = {
                "id" : row["authors.id"],
                "name" : row["name"],
                "created_at" : row["authors.created_at"],
                "updated_at" : row["authors.updated_at"]
            }
            book.authors_who_favorited.append(author.Author(author_data))
        return book
    
    @classmethod
    def unfavorited_books(cls,data):
        query = "SELECT * FROM books where books.id NOT IN (SELECT book_id FROM favorites where author_id = %(id)s);"
        books = []
        results = connectToMySQL("esquema_libros").query_db(query,data)
        for row in results:
            books.append(cls(row))
        return books