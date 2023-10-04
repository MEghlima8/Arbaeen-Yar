DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS karavan_users;
DROP TABLE IF EXISTS karavan;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    counter SERIAL ,
    uuid VARCHAR(255) PRIMARY KEY ,
    chat_id INT ,
    fullname VARCHAR (255),
    username VARCHAR (50) UNIQUE,
    password VARCHAR (255),
    is_manager VARCHAR (50),
    is_user VARCHAR(50) ,
    active JSONB ,
    step VARCHAR (255) ,
    first_msg VARCHAR(255) ,
    second_msg VARCHAR(255) ,
    last_activity JSONB
);
    

CREATE TABLE karavan (
    counter SERIAL ,
    uuid VARCHAR(255) PRIMARY KEY ,
    name VARCHAR(255) ,
    manager_uuid VARCHAR(255) ,
    managers JSONB ,
    events JSONB ,
    FOREIGN KEY(manager_uuid) REFERENCES users(uuid)
);


CREATE TABLE karavan_users (
    counter SERIAL ,
    uuid VARCHAR(255) PRIMARY KEY ,
    user_uuid VARCHAR(255) NOT NULL ,
    karavan_uuid VARCHAR(255) NOT NULL ,
    whois VARCHAR(50) ,
    FOREIGN KEY(user_uuid) REFERENCES users(uuid) ,
    FOREIGN KEY(karavan_uuid) REFERENCES karavan(uuid)
);


CREATE TABLE request (
    counter SERIAL PRIMARY KEY ,
    uuid VARCHAR (255) ,
    user_uuid VARCHAR (255) NOT NULL ,
    karavan_uuid VARCHAR(255) NOT NULL ,
    type VARCHAR (50) NOT NULL ,
    params JSONB NOT NULL ,
    time JSONB ,
    status VARCHAR (50) ,
    client_service VARCHAR(255) ,
    FOREIGN KEY(user_uuid) REFERENCES users(uuid) ,
    FOREIGN KEY(karavan_uuid) REFERENCES karavan(uuid)
);