import re
import glob
import sqlite3

def add_tag(doc, software):
    with open(doc) as f:
        text = f.read()
        
        match_re = re.compile(r'(?:^|\s)\*(\S*?)\*(?=\s)')
        matches = match_re.findall(text)
        for m in matches:
            doc = doc.split("/")[-1].split(".")[0]
            t = (doc, m, software)
            c.execute("INSERT INTO tags VALUES (?,?,?)", t)
            print("{}/{} => {}".format(software,doc, m))

conn = sqlite3.connect('tags1.db')
c = conn.cursor()
files = glob.glob("/home/aniket/vim/runtime/doc/*.txt")
for doc in files:
    add_tag(doc, "vim")

files = glob.glob("/home/aniket/neovim/runtime/doc/*.txt")
for doc in files:
    add_tag(doc, "neovim")
conn.commit()
conn.close()
