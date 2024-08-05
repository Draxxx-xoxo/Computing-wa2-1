import sqlite3

con = sqlite3.connect('computing_students.db')

cur = con.cursor()

res = cur.execute("SELECT name, gender FROM student")

print(res.fetchall())

#res = cur.execute("INSERT INTO offence (stu_id, description, offence_date) VALUES(1, 'Plagiarism', '2019-01-01')")
#con.commit() 

data = [(35, 'Plagiarism', '2019-01-01'), (16, 'Plagiarism', '2019-01-01')]
res = cur.executemany("INSERT INTO offence (stu_id, description, offence_date) VALUES(?, ?, ?)", data)
con.commit() 

con.close()
