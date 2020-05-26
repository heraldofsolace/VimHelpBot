import re
import glob
import sqlite3

conn = sqlite3.connect('tags.db')
c = conn.cursor()
files = glob.glob("/home/aniket/vim/runtime/doc/*.txt")
for doc in files:
    with open(doc) as f:
        text = f.read()
        
        match_re = re.compile(r'(?:^|\s)\*(\S*?)\*(?=\s)')
        matches = match_re.findall(text)
        for m in matches:
            doc = doc.split("/")[-1].split(".")[0]
            t = (doc, m)
            c.execute("INSERT INTO tags VALUES (?,?)", t)
            print("{} => {}".format(doc, m))
conn.commit()
conn.close()
