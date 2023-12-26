
from model import db, Dictionary

class DictionaryService:
    @staticmethod
    def create_dictionary(name):
        try:
            # Yeni bir Dictionary kaydı oluştur
            dictionary = Dictionary(name=name)
            db.session.add(dictionary)
            db.session.commit()
            return {"message": "Sözlük başarıyla oluşturuldu"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def get_dictionary(dictionary_id):
        try:
            # Belirtilen sözlüğü al
            dictionary = Dictionary.query.get(dictionary_id)
            if dictionary is not None:
                dictionary_data = {
                    "id": dictionary.id,
                    "name": dictionary.name,
                    "translations": [
                        {
                            "id": translation.id,
                            "source_language": translation.source_language,
                            "target_language": translation.target_language,
                            "source_text": translation.source_text,
                            "target_text": translation.target_text,
                        }
                        for translation in dictionary.translations
                    ],
                }
                return dictionary_data, 200
            else:
                return {"message": "Sözlük bulunamadı"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def update_dictionary(dictionary_id, name):
        try:
            # Belirtilen sözlüğü güncelle
            dictionary = Dictionary.query.get(dictionary_id)
            if dictionary is not None:
                dictionary.name = name
                db.session.commit()
                return {"message": "Sözlük başarıyla güncellendi"}, 200
            else:
                return {"message": "Sözlük bulunamadı"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def delete_dictionary(dictionary_id):
        try:
            # Belirtilen sözlüğü sil
            dictionary = Dictionary.query.get(dictionary_id)
            if dictionary is not None:
                db.session.delete(dictionary)
                db.session.commit()
                return {"message": "Sözlük başarıyla silindi"}, 200
            else:
                return {"message": "Sözlük bulunamadı"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def list_dictionaries():
        try:
            # Tüm sözlükleri al
            dictionaries = Dictionary.query.all()
            dictionaries_data = [
                {
                    "id": dictionary.id,
                    "name": dictionary.name,
                    "translations": [
                        {
                            "id": translation.id,
                            "source_language": translation.source_language,
                            "target_language": translation.target_language,
                            "source_text": translation.source_text,
                            "target_text": translation.target_text,
                        }
                        for translation in dictionary.translations
                    ],
                }
                for dictionary in dictionaries
            ]
            return dictionaries_data, 200
        except Exception as e:
            return {"error": str(e)}, 500
