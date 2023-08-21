CREATE TABLE users (
    counter SERIAL ,
    uuid VARCHAR(255) PRIMARY KEY ,
    chat_id INT ,
    fullname VARCHAR (255),
    username VARCHAR (50) UNIQUE,
    password VARCHAR (255),
    is_manager VARCHAR (50),
    is_user VARCHAR(50) ,
    active VARCHAR(50) ,
    step VARCHAR (255) ,
    first_msg VARCHAR(255) ,
    second_msg VARCHAR(255)
);


CREATE TABLE karavan (
    counter SERIAL ,
    uuid VARCHAR(255) PRIMARY KEY ,
    name VARCHAR(255) ,
    manager_uuid VARCHAR(255) ,
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
