import re
import sqlite3
import subprocess

tag_re = re.compile(r'^(\S+)\s*(\S+).txt', re.MULTILINE)
def add_tags(software):
        with open('third_party/' + software + '/runtime/doc/tags') as f:
                text = f.read()

                matches = tag_re.findall(text)

                for m in matches:
                    # db entry: (doc, tag, software)
                    entry = (m[1], m[0], software)

                    c.execute('INSERT OR REPLACE INTO tags VALUES (?,?,?)', entry)
                    print('{}/{} => {}'.format(software, m[1], m[0]))

conn = sqlite3.connect('tags.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS tags(filename text, tag text, software text)")

# list of supported softwares
softwares = ['vim', 'neovim']

for software in softwares:
        add_tags(software)

conn.commit()
conn.close()
