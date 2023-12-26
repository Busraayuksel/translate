
from model import db, Translation, Dictionary

class TranslationService:
    @staticmethod
    def create_translation(source_language, target_language, source_text, target_text, dictionary_id):   
        try:
            # Yeni bir Translation kaydı oluştur
            # dictionary_id dictionary tablosunda mevcut olmalı
            dict = Dictionary.query.get(dictionary_id)
            if dict is None:
                return {"message": "Sözlük bulunamadı"}, 404
            translation = Translation(
                source_language=source_language,
                target_language=target_language,
                source_text=source_text,
                target_text=target_text,
                dictionary_id=dictionary_id
            )
            db.session.add(translation)
            db.session.commit()
            return {"message": "Çeviri başarıyla oluşturuldu"}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def get_translation(translation_id):
        try:
            # id'e göre istenilen translation bul
            translation = Translation.query.get(translation_id)
            if translation is not None:
                translation_data = {
                    "id": translation.id,
                    "source_language": translation.source_language,
                    "target_language": translation.target_language,
                    "source_text": translation.source_text,
                    "target_text": translation.target_text,
                    "dictionary_id": translation.dictionary_id,
                }
                return translation_data, 200
            else:
                return {"message": "Çeviri bulunamadı"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def update_translation(translation_id, source_language, target_language, source_text, target_text, dictionary_id):
        try:
            # güncelle
            translation = Translation.query.get(translation_id)
            if translation is not None:
                translation.source_language = source_language
                translation.target_language = target_language
                translation.source_text = source_text
                translation.target_text = target_text
                translation.dictionary_id = dictionary_id
                db.session.commit()
                return {"message": "Çeviri başarıyla güncellendi"}, 200
            else:
                return {"message": "Çeviri bulunamadı"}, 404
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def delete_translation(translation_id):
        try:
            # id'e göre translation silmek için
            translation = Translation.query.get(translation_id)
            if translation is not None:
                db.session.delete(translation)
                db.session.commit()
                return {"message": "Çeviri başarıyla silindi"}, 200
            else:
                return {"message": "Çeviri bulunamadı"}, 404
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def list_translations():
        try:
            # Tüm çevirileri listele
            translations = Translation.query.all()
            translation_list = [
                {
                    "id": translation.id,
                    "source_language": translation.source_language,
                    "target_language": translation.target_language,
                    "source_text": translation.source_text,
                    "target_text": translation.target_text,
                    "dictionary_id": translation.dictionary_id,
                }
                for translation in translations
            ]
            return translation_list, 200
        except Exception as e:
            return {"error": str(e)}, 500

    # get translation by source text and source language and dictionary id
    @staticmethod
    def get_translation_by_source(source_text, source_language, dictionary_id):
        try:
            # id'e göre istenilen translation bul
            translation = Translation.query.filter_by(source_text=source_text, source_language=source_language, dictionary_id=dictionary_id).first()
            if translation is not None:
                translation_data = {
                    "id": translation.id,
                    "source_language": translation.source_language,
                    "target_language": translation.target_language,
                    "source_text": translation.source_text,
                    "target_text": translation.target_text,
                    "dictionary_id": translation.dictionary_id,
                }
                return translation_data, 200
            else:
                return None
        except Exception as e:
            return {"error": str(e)}, 500
    