from db import SQLite

db = SQLite('test_data.sqlite3')

print(db.run_query("CREATE TABLE contacts (\
    id INT AUTO_INCREMENT PRIMARY KEY,\
    phoneNumber VARCHAR(255),\
    email VARCHAR(255),\
    linkedId INT,\
    linkPrecedence VARCHAR(255),\
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,\
    updatedAt DATETIME,\
    deletedAt DATETIME);\
    "))

insert_queries = [
    "INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence) VALUES\
          ('123456', 'lorraine@hillvalley.edu', NULL, 'primary');",
    "INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence) VALUES \
        ('123456', 'mcfly@hillvalley.edu', 1, 'secondary');",
    "INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence) VALUES \
        ('919191', 'george@hillvalley.edu', NULL, 'primary');",
    "INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence) VALUES \
        ('717171', 'biffsucks@hillvalley.edu', NULL, 'primary');"
]
for query in insert_queries:
    db.run_query(query)

print(db.run_query("SELECT * FROM contacts;"))

db.close_connection()