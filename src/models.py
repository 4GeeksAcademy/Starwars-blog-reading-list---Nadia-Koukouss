from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favoritos_personajes = relationship("FavoritoPersonaje", back_populates="user")
    favoritos_planetas = relationship("FavoritoPlaneta", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class Planeta(db.Model):
    __tablename__ = "planeta"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    clima: Mapped[str] = mapped_column(String(50))
    poblacion: Mapped[int] = mapped_column(Integer)
    terreno: Mapped[str] = mapped_column(String(50))
    diametro: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return '<Planeta %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "poblacion": self.poblacion,
            "terreno": self.terreno,
            "diametro": self.diametro,
        }
    

class Personaje(db.Model):
    __tablename__ = "personaje"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    altura: Mapped[int] = mapped_column(Integer)
    peso: Mapped[int] = mapped_column(Integer)
    color_cabello: Mapped[str] = mapped_column(String(30))
    color_piel: Mapped[str] = mapped_column(String(30))
    color_ojos: Mapped[str] = mapped_column(String(30))
    fecha_nacimiento: Mapped[str] = mapped_column(String(20))
    genero: Mapped[str] = mapped_column(String(20))

    def __repr__(self):
        return  '<Personaje %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "peso": self.peso,
            "color_cabello": self.color_cabello,
            "color_piel": self.color_piel,
            "color_ojos": self.color_ojos,
            "fecha_nacimiento": self.fecha_nacimiento,
            "genero": self.genero,
      
        }


class FavoritoPersonaje(db.Model):
    __tablename__ = "favorito_personaje"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personaje.id"))
   
    user = relationship("User", back_populates="favoritos_personajes")
    personaje = relationship("Personaje")

    def __repr__(self):
         return '<FavoritoPersonaje user_id=%r, personaje_id=%r>' % (self.user_id, self.personaje_id)

    def serialize(self):
        return {
        "id": self.id,
        "user_id": self.user_id,
        "personaje_id": self.personaje_id,
        "personaje": self.personaje.serialize()
    
        }
    
class FavoritoPlaneta(db.Model):
    __tablename__ = "favorito_planeta"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"))
   
    user = relationship("User", back_populates="favoritos_planetas")
    planeta = relationship("Planeta")

    def __repr__(self):
        return '<FavoritoPlaneta user_id=%r, planeta_id=%r>' % (self.user_id, self.planeta_id)

    def serialize(self):
        return {
        "id": self.id,
        "user_id": self.user_id,
        "planeta_id": self.planeta_id,
        "planeta": self.planeta.serialize()
    
        }

   
 


