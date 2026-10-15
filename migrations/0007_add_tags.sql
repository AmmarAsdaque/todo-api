CREATE TABLE tags (
    task_id INTEGER NOT NULL REFERENCES tasks (id),
    name TEXT NOT NULL,
    PRIMARY KEY (task_id, name)
);
