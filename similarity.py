import re
import math
from collections import Counter
import os

def readText(f):
    fin = open(f,'r')
    content = fin.read()
    fin.close()
    return content

def cosine(v1,v2):
    common = set(v1.keys()) & set(v2.keys())
    n = sum([v1[x]*v2[x] for x in common])
    s1 = sum([v1[x]**2 for x in v1.keys()])
    s2 = sum([v2[x]**2 for x in v2.keys()])
    d = math.sqrt(s1)*math.sqrt(s2)
    try:
        return float(n)/d
    except Exception:
        return 0.0

def t2v(text):
    w = re.compile(r'\w+')
    ws = w.findall(text)
    return Counter(ws)

def compute(fileA,fileB):
    return cosine(t2v(readText(fileA)),t2v(readText(fileB)))

print(compute('ocr.txt','clearText.txt'))