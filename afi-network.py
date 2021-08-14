import networkx as nx
import nltk
import os, re
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

afi_files = [f for f in os.listdir(os.getcwd()) if f[:2]=="af" and f.endswith(".txt")] #find all the AFI text files
print(afi_files)
#afi = open(afi_files[0], encoding='latin')
#f1 = afi.read()
#print(f1[:2000])

afi_expand_pattern = re.compile(r'AIR FORCE INSTRUCTION ?[0-9]+-? ?[0-9]+', flags=re.IGNORECASE)
afi_pattern = re.compile(r'\afi-? ?[0-9]+-? ?[0-9]+', flags=re.IGNORECASE)

afi_ref = re.compile(r'afi-? ?[0-9]+-? ?[0-9]+', flags=re.IGNORECASE)
form_ref = re.compile(r'af form ?[0-9]+', flags=re.IGNORECASE)
afman_ref = re.compile(r'afman ?[0-9]+-? ?[0-9]+', flags=re.IGNORECASE)

for f in afi_files:
    afi_file = open(f,encoding='latin').read()
    print(f)
    #print(afi_expand_pattern.search(afi_file).group())
    afi_count = Counter(afi_ref.findall(afi_file))
    for k in afi_count:
        print(k,": ",afi_count[k])
    print(form_ref.findall(afi_file))
#pandatext = pd.read_table(afi)
#print(pandatext.head())
#afi63101 = open('afi61-102.txt', encoding='latin').read()
#print(afi63101)

G = nx.Graph()
for f in afi_files:
    afi_title = os.path.splitext(f)[0].upper()
    afi_file = open(f, encoding='latin').read()
    G.add_node(afi_title)
    #G[afi_title]['Length'] = len(afi_file)
    afi_ref_count = Counter(afi_ref.findall(afi_file))
    for match in afi_ref_count:
        G.add_node(match)


for f in afi_files:
    afi_title = os.path.splitext(f)[0].upper()
    afi_file = open(f, encoding='latin').read()
    afi_ref_count = Counter(afi_ref.findall(afi_file))
    for match in afi_ref_count:
        G.add_edge(afi_title,match,{'weight':afi_ref_count[match]})

print("G nodes: ",G.nodes())
print(sorted(nx.degree(G).values(),reverse=True))