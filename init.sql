CREATE TABLE teams (
    id UUID NOT NULL,
    name VARCHAR NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id UUID NOT NULL,
    username VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    status INTEGER,
    birthday TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    team UUID,
    PRIMARY KEY (id),
    UNIQUE (username),
    FOREIGN KEY (team) REFERENCES teams (id)
);

CREATE TABLE team_members (
    team_id UUID NOT NULL,
    user_id UUID NOT NULL,
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES teams (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
