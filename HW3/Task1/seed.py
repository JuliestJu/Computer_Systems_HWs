from faker import Faker
import psycopg2

fake = Faker()

conn = psycopg2.connect(
    dbname='hw3',
    user='user',
    password='password',
    host='db'
)
cursor = conn.cursor()

# Insert statuses
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (status,))

# Insert users and tasks
user_ids = []
for _ in range(20):
    fullname = fake.name()
    email = fake.email()
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id", (fullname, email))
    user_id = cursor.fetchone()[0]
    user_ids.append(user_id)

# Assign tasks to 15 users
for user_id in user_ids[:15]:
    for i in range(5):
        title = fake.sentence(nb_words=2)
        description = fake.text(nb_words=3)
        status_id = fake.random_int(min=1, max=3)
        cursor.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id)
        )

conn.commit()
cursor.close()
conn.close()
