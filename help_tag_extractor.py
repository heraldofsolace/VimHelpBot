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
            c.execute("INSERT OR REPLACE INTO tags VALUES (?,?,?)", t)
            print("{}/{} => {}".format(software,doc, m))

conn = sqlite3.connect('../tags.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS tags(filename text, tag text, software text)")
files = glob.glob("../vim/runtime/doc/*.txt")
for doc in files:
    add_tag(doc, "vim")

files = glob.glob("../neovim/runtime/doc/*.txt")
for doc in files:
    add_tag(doc, "neovim")
conn.commit()
conn.close()
