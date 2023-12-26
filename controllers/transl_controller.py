# controllers/transl_controller.py
from flask import Blueprint, render_template,request,jsonify
from services.dictionary_service import DictionaryService
from services.translation_service import TranslationService
from api import translate_text

service = DictionaryService()
translation_service = TranslationService()

transl_bp = Blueprint('transl', __name__)

#home page
@transl_bp.route('/')
def translate_text():
    dicts = service.list_dictionaries()
    return render_template('word.html',dicts=dicts[0])


#list all translations
@transl_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        data = request.get_json()
        target_language = data.get('language')
        source_text = data.get('word')
        result = translate_text(target_language, source_text)  
        return result
    
    return jsonify(result)

#list all translations
@transl_bp.route("/create", methods=['POST'])
def create_translation():
    if request.method == 'POST':
        data = request.get_json()
        source_language = data.get('source_language')
        target_language = data.get('target_language')
        source_text = data.get('source_text')
        target_text = data.get('target_text')
        dictionary_id = data.get('dictionary_id')
        print("dict id ",dictionary_id)
        temp_word = translation_service.get_translation_by_source(source_text, source_language, dictionary_id)
        if temp_word is None:
            success = translation_service.create_translation(source_language, target_language, source_text, target_text, dictionary_id)
            return jsonify({'success': success})
        else :
            return jsonify({'success': False})
        
    return jsonify({'success': False})


#del translation by id
@transl_bp.route("/delete", methods=['POST'])
def delete_translation():
    if request.method == 'POST':
        data = request.get_json()
        translation_id = data.get('word_id')
        success = translation_service.delete_translation(translation_id)
        return jsonify({'success': success})
    return jsonify({'success': False})

def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "api_key.json"

    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)


    
    return result