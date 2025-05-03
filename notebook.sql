CREATE TABLE tasks(
	id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES Users(id) ON DELETE CASCADE,
        text VARCHAR(100) NOT NULL,
        is_completed BOOLEAN
);

INSERT INTO tasks(user_id, text, is_completed) VALUES(1, ' Task number i', false);

