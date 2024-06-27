-- Get all tasks of a specific user
SELECT * FROM tasks WHERE user_id = 1;

-- Get tasks by status
SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- Update task status
UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 1;

-- Get users with no tasks
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);

-- Add a new task for a user
INSERT INTO tasks (title, description, status_id, user_id) VALUES ('New Task', 'Task description', 1, 1);

-- Get all unfinished tasks
SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');

-- Delete a specific task
DELETE FROM tasks WHERE id = 1;

-- Find users by email
SELECT * FROM users WHERE email LIKE '%example.com';

-- Update user name
UPDATE users SET fullname = 'New Name' WHERE id = 1;

-- Get task count by status
SELECT status.name, COUNT(tasks.id) FROM tasks JOIN status ON tasks.status_id = status.id GROUP BY status.name;

-- Get tasks by user email domain
SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE '%example.com';

-- Get tasks with no description
SELECT * FROM tasks WHERE description IS NULL;

-- Get users and their tasks with status 'in progress'
SELECT users.fullname, tasks.* FROM users JOIN tasks ON users.id = tasks.user_id WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress');

-- Get users and their task counts
SELECT users.fullname, COUNT(tasks.id) FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.fullname;
