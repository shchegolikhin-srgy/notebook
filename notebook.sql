CREATE TABLE users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(20) NOT NULL,
        password VARCHAR(16) NOT NULL
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,          
    text VARCHAR(255) NOT NULL,    
    user_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    completed BOOLEAN
);

INSERT INTO users (username, password) VALUES('1', '1');
INSERT INTO tasks (text, completed, user_id) VALUES ('Task 1', false, 0);

SELECT text, completed FROM tasks  WHERE user_id = 1;
SELECT id FROM users WHERE username ='1' AND password = '1';

UPDATE tasks SET completed = true WHERE text ='text 1' AND user_id = 3;
UPDATE tasks SET text = 'text 2' WHERE text ='text 1'AND user_id = 3;

DELETE FROM users WHERE username ='1' AND password = '1';
DELETE FROM tasks WHERE text ='text 1' AND user_id = 1;
