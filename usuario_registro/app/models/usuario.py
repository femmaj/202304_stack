import re
from app.config.mysqlconnection import connectToMySQL
from flask import flash

SEGURA_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$')

class Usuario:

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validar(data):
        todo_ok = True
        if not SEGURA_REGEX.match(data['password']):
            flash("Tu contraseña debe tener 8 caracteres, una mayuscula, minuscula, numero y caracter especial", "danger")
            todo_ok = False
        return todo_ok

    @classmethod
    def get_all(cls):
        usuarios = []
        query = """
        SELECT id, nombre, email, password, created_at, updated_at FROM usuarios;
        """
        result = connectToMySQL().query_db(query);
        for usuario in result:
            usuarios.append(cls(usuario))
        return usuarios

    def create(self):
        query = """INSERT INTO usuarios (nombre, email, password, created_at, updated_at) VALUES (%(nombre)s, %(email)s, %(password)s, NOW(), NOW());"""
        data = {
            'nombre': self.nombre,
            'email': self.email,
            'password': self.password,
        }
        self.id = connectToMySQL().query_db(query, data)
        return self

    @classmethod
    def save(cls, data):
        query = """INSERT INTO usuarios (nombre, email, password, created_at, updated_at) VALUES (%(nombre)s, %(email)s, %(password)s, NOW(), NOW());"""
        id = connectToMySQL().query_db(query, data)
        resultado = None
        if id:
            resultado = cls.get(id)
        return resultado

    @classmethod
    def get(cls, id):
        query = """
        SELECT id, nombre, email, password, created_at, updated_at FROM usuarios where id = %(id)s;
        """
        data = {
            'id': id
        }
        result = connectToMySQL().query_db(query, data);
        return cls(result[0])

    @classmethod
    def get_by_email(cls, email):
        query = """
        SELECT id, nombre, email, password, created_at, updated_at FROM usuarios where email = %(email)s;
        """
        data = {
            'email': email
        }
        result = connectToMySQL().query_db(query, data);
        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def delete(cls, id):
        query = """
        DELETE FROM usuarios where id = %(id)s;
        """
        data = {
            'id': id
        }
        result = connectToMySQL().query_db(query, data);
        return result
