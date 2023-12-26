# controllers/dict_controller.py
from flask import Blueprint, render_template, request,redirect, url_for, jsonify
from services.dictionary_service import DictionaryService

dict_bp = Blueprint('dict', __name__)

dict_service = DictionaryService()



#list all dicts
@dict_bp.route('/dict', methods=['GET','POST'])
def create_dict():
    if request.method == 'POST':
        dict_name = request.form.get('dictionary-name')
        dict_service.create_dictionary(dict_name)
        return redirect(url_for('dict.create_dict'))
    dicts = dict_service.list_dictionaries()
    return render_template('index.html', dicts=dicts[0])


#get dict by id
@dict_bp.route('/dict/<int:id>')
def get_dict(id):
    dicts = dict_service.list_dictionaries()
    dict = dict_service.get_dictionary(id)
    print(dict)
    if dict[1] == 404:
        return render_template('404.html')
    translations = dict[0]['translations']
    return render_template('index.html', dicts=dicts[0], dict=dict[0], translations=translations)

#delete dict 


@dict_bp.route('/dict/delete', methods=['POST'])
def delete_dict():
    if request.method == 'POST':
        data = request.get_json()
        dict_id = data.get('dict_id')
        print(dict_id)
        success = dict_service.delete_dictionary(dict_id)
        return jsonify({'success': success})
        
    return jsonify({'success': False})
