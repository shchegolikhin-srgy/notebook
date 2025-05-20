
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    hashed_password TEXT NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,          
    text VARCHAR(255) NOT NULL,    
    user_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    completed BOOLEAN
);

INSERT INTO users (username, hashed_password) VALUES('1', '1');
INSERT INTO users (username, hashed_password, role) VALUES('1', '1', 'admin');
INSERT INTO tasks (text, completed, user_id) SELECT $1, $2, users.id FROM users WHERE users.username = $3;

INSERT INTO tasks (text, completed, user_id) SELECT $1, $2, users.id FROM users WHERE users.username = $2;

SELECT tasks.text, tasks.completed FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.username =$1; 
SELECT id FROM users WHERE username =$1 AND hashed_password = $2;

UPDATE tasks SET text = $1 FROM users WHERE tasks.text =$2 AND tasks.user_id = users.id AND users.username = $3;
UPDATE tasks SET completed = $1 FROM users WHERE tasks.text =$2 AND tasks.user_id = users.id AND users.username = $3;

DELETE FROM users WHERE username ='1' AND hashed_password = '1';
DELETE FROM tasks  USING users WHERE tasks.text =$1 AND tasks.user_id = users.id AND users.username = $2;