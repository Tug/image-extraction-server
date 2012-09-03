import random, string
import pickle, base64

def genRandomString(len):
    return "".join(random.choice(string.letters) for x in range(len))

def serialize(obj):
    return base64.b64encode(pickle.dumps(obj))

def deserialize(obj):
    return pickle.loads(base64.b64decode(obj))