CREATE TABLE users (
    username text unique,
    password text,
    email text
);

CREATE INDEX usernameI on users (username);