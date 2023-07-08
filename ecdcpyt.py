from pyDes import *
from utils import load_json
from assets import jsonfile as jsonfiles
loader = load_json(jsonfiles)
eck = loader['key']

def ecpyt(message:str):
    """Encrypts data using `triple_des()`"""
    tte = triple_des(eck).encrypt(message, padmode=2)
    return tte

def dcypt(message:str):
    """Decrypts data using `triple_des()`"""
    ttd = triple_des(eck).decrypt(message, padmode=2)
    return ttd

