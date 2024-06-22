import firebase_admin
from firebase_admin import credentials, firestore

path_to_key = "onlyfansbot-ac45f-firebase-adminsdk-e0fzw-4ca3a4ef20.json"

cred = credentials.Certificate(path_to_key)
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_name = 'users'


def create_user(id_user):
    doc_ref = db.collection(collection_name).document(str(id_user))
    doc_ref.set({"id": id_user})


def check_user(id_user):
    collection_ref = db.collection(collection_name)
    document_ref = collection_ref.document(str(id_user))
    document = document_ref.get()
    return document.exists


def add_text(id_user, text_user, text_bot):
    doc_ref = db.collection(collection_name).document(str(id_user))
    doc = doc_ref.get()
    dict_db = doc.to_dict()
    dict_db.pop('id', None)
    num_field = max((int(key.split('_')[0]) for key in dict_db.keys()), default=0)
    doc_ref.update({str(num_field+1) + "_text_" + 'u': text_user, str(num_field+2) + "_text_" + 'b': text_bot})


def get_inf(id_user):
    history = db.collection(collection_name).document(str(id_user)).get().to_dict()
    history.pop('id', None)
    messages = ''
    if history:
        num_field = max((int(key.split('_')[0]) for key in history.keys()), default=0)
        messages = history[f'{num_field}_text_b']
    return messages, len(history)


def get_last_10_entries(id_user):
    history = db.collection(collection_name).document(str(id_user)).get().to_dict()
    history.pop('id', None)

    sorted_keys = sorted(history.keys(), key=lambda x: int(x.split('_')[0]))
    last_10_keys = sorted_keys[-10:]
    last_10_entries = [history[key] for key in last_10_keys]
    return last_10_entries


def count_users():
    collection_ref = db.collection(collection_name)
    doc_refs = collection_ref.list_documents()
    users = ''
    for doc in doc_refs:
        users += doc.id + '\n'
    print(users)
    return len(list(collection_ref.stream())), users
