import firebase_admin
from firebase_admin import credentials, firestore

path_to_key = "firebase_sdk/dexartbot-firebase-adminsdk-09uy5-b81f5fa8d1.json"

cred = credentials.Certificate(path_to_key)
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_name = 'users'


def create_user(id_user):
    doc_ref = db.collection(collection_name).document(str(id_user))
    doc_ref.set({"id": id_user})


def check_user(id_user):
    return db.collection(collection_name).document(str(id_user)).get().exists


def add_text(id_user, text_user, text_bot):
    doc_ref = db.collection(collection_name).document(str(id_user))
    doc = doc_ref.get().to_dict()
    num_field = max(len(doc) // 2 - 1, 0)
    doc_ref.update({f"text_{num_field}u": text_user, f"text_{num_field}b": text_bot})


def get_inf(id_user):
    history = db.collection(collection_name).document(str(id_user)).get().to_dict()
    history.pop('id', None)
    # Вернем список сообщений
    return list(history.values())


def count_users():
    collection_ref = db.collection(collection_name)
    doc_refs = collection_ref.list_documents()

    users_list = [int(doc.id) for doc in doc_refs]
    print(users_list, sep='\n')
    return len(list(collection_ref.stream())), users_list
