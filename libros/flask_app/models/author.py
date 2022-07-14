from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book




class Author:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []

#CREATE--------------------
    @classmethod
    def save(cls,data):
        query = "INSERT INTO authors (name,created_at,updated_at) VALUES (%(name)s,NOW(),NOW())"
        return connectToMySQL('esquema_libros').query_db(query,data)

#READ----------------

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        authors_db =  connectToMySQL('esquema_libros').query_db(query)
        authors =[]
        for a in authors_db:
            authors.append(cls(a))
        return authors


    @classmethod
    def getAuthor_withBooks(cls,data):
        query = "SELECT * FROM authors LEFT JOIN favorites on favorites.author_id = authors.id LEFT JOIN books on favorites.book_id = books.id where authors.id = %(id)s;"
        results = connectToMySQL('esquema_libros').query_db(query,data)
        author = cls(results[0])
        for row in results:
            if row['books.id'] == None:
                break
            book_data = {
                "id" : row["books.id"],
                "title" : row["title"],
                "num_pages": row["num_pages"],
                "created_at" : row["books.created_at"],
                "updated_at" : row["books.updated_at"]
            }
            author.favorite_books.append( book.Book( book_data ) )
        return author

    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL("esquema_libros").query_db(query,data)
    
    @classmethod
    def unfavorited_authors(cls,data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s);"
        authors = []
        results = connectToMySQL("esquema_libros").query_db(query,data)
        for row in results:
            authors.append(cls(row))
        return authors