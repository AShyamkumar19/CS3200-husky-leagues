DROP DATABASE IF EXISTS newHuskyLeagues;

CREATE DATABASE newHuskyLeagues;

USE newHuskyLeagues;

CREATE TABLE IF NOT EXISTS team_members (
    memberID int,
    firstName varchar(50),
    lastName varchar(50),
    email varchar(50),
    PRIMARY KEY (memberID)
);

CREATE TABLE IF NOT EXISTS sports (
    sportID int,
    name varchar(50),
    rules text,
    PRIMARY KEY (sportID)
);

CREATE TABLE IF NOT EXISTS teams (
    sportID int,
    teamID int,
    name varchar(50),
    PRIMARY KEY (sportID, teamID),
    FOREIGN KEY (sportID) REFERENCES sports (sportID)
                                 ON UPDATE CASCADE,
    INDEX team_sport_index (teamID, sportID)
);

CREATE TABLE IF NOT EXISTS roles (
    roleID int,
    name varchar(50),
    description text,
    PRIMARY KEY (roleID)
);

CREATE TABLE IF NOT EXISTS part_of (
    memberID int,
    sportID int,
    teamID int,
    jerseyNum int,
    roleID int,
    PRIMARY KEY (memberID, sportID, teamID),
    FOREIGN KEY (memberID) REFERENCES team_members (memberID)
                                 ON UPDATE CASCADE,
    FOREIGN KEY (sportID, teamID) REFERENCES teams (sportID, teamID)
                                 ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS admins (
    adminID int,
    firstName varchar(50),
    lastName varchar(50),
    email varchar(50),
    sportID int,
    PRIMARY KEY (adminID),
    FOREIGN KEY (sportID) REFERENCES sports (sportID)
                                 ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS sponsors (
    sponsorID int,
    name varchar(50),
    email varchar(50),
    PRIMARY KEY (sponsorID)
);

CREATE TABLE IF NOT EXISTS events (
    eventID int,
    description text,
    dateTime datetime,
    location varchar(50),
    sponsorID int,
    PRIMARY KEY (eventID),
    FOREIGN KEY (sponsorID) REFERENCES sponsors (sponsorID)
                                 ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS sponsorships (
    sponsorID int,
    teamID int,
    sportID int,
    money FLOAT,
    PRIMARY KEY (sponsorID, teamID, sportID),
    FOREIGN KEY (sponsorID) REFERENCES sponsors (sponsorID)
                                 ON UPDATE CASCADE,
    FOREIGN KEY (sportID, teamID) REFERENCES teams (sportID, teamID)
                                 ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS games (
    gameID int,
    dateTime datetime,
    location varchar(50),
    team1_ID int,
    team2_ID int,
    team1_score int,
    team2_score int,
    team1_sportID int,
    team2_sportID int,
    PRIMARY KEY (gameID),
    FOREIGN KEY(team1_ID, team1_sportID) REFERENCES teams (teamID, sportID)
                                 ON UPDATE CASCADE,
    FOREIGN KEY (team2_ID, team2_sportID) REFERENCES teams(teamID, sportID)
                                ON UPDATE CASCADE,
    INDEX (team1_ID, team1_sportID),
    INDEX (team2_ID, team2_sportID)
);

CREATE TABLE IF NOT EXISTS referees (
    refID int,
    firstName varchar(50),
    lastName varchar(50),
    email varchar(50),
    PRIMARY KEY (refID)
);

CREATE TABLE IF NOT EXISTS officiates (
    refID int,
    gameID int,
    PRIMARY KEY (refID, gameID),
    FOREIGN KEY (refID) REFERENCES referees (refID)
                                      ON UPDATE CASCADE,
    FOREIGN KEY (gameID) REFERENCES games (gameID)
                                      ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS chooses (
    refID int,
    sportID int,
    PRIMARY KEY (refID, sportID),
    FOREIGN KEY (refID) REFERENCES referees (refID)
                                   ON UPDATE CASCADE,
    FOREIGN KEY (sportID) REFERENCES sports (sportID)
                                   ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS fans (
    fanID int,
    firstName varchar(50),
    lastName varchar(50),
    email varchar(50),
    PRIMARY KEY (fanID)
);

CREATE TABLE IF NOT EXISTS follows_team_members (
    fanID int,
    memberID int,
    PRIMARY KEY (fanID, memberID),
    FOREIGN KEY (fanID) REFERENCES fans (fanID)
                                                ON UPDATE CASCADE,
    FOREIGN KEY (memberID) REFERENCES team_members (memberID)
                                                ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS follows_teams (
    fanID int,
    teamID int,
    sportID int,
    PRIMARY KEY (fanID, teamID, sportID),
    FOREIGN KEY (fanID) REFERENCES fans (fanID)
                                            ON UPDATE CASCADE,
    FOREIGN KEY (sportID, teamID) REFERENCES teams (sportID, teamID)
                                            ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS follows_sports (
    fanID int,
    sportID int,
    PRIMARY KEY (fanID, sportID),
    FOREIGN KEY (fanID) REFERENCES fans (fanID)
                                            ON UPDATE CASCADE,
    FOREIGN KEY (sportID) REFERENCES sports (sportID)
                                            ON UPDATE CASCADE
);