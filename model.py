
from database import db

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_language = db.Column(db.String(255))
    target_language = db.Column(db.String(255))
    source_text = db.Column(db.Text)
    target_text = db.Column(db.Text)
    dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionary.id', ondelete='CASCADE'), nullable=False)
    
    def __str__(self):
        return f'Translation(id={self.id}, ' \
               f'source_language={self.source_language},' \
               f'target_language={self.target_language},' \
               f'source_text={self.source_text},' \
               f'target_text={self.target_text}, ' \
               f'dictionary_id={self.dictionary_id})'

class Dictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    translations = db.relationship('Translation', backref='dictionary', lazy=True, cascade='all, delete-orphan')
    
    def __str__(self):
        return f'Dictionary(id={self.id}, ' \
               f'name={self.name},' \
               f' translations={self.translations})'
