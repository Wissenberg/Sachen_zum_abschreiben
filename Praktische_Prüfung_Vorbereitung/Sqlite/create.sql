CREATE TABLE robo (
	robo_id INTEGER,
	name VARCHAR(255),
	topic VARCHAR(255),
	PRIMARY KEY(robo_id AUTOINCREMENT)
);


CREATE TABLE kommando (
	kommando_id INTEGER,
	move FLOAT,
	turn INTEGER,
	robo_id INTEGER,
	received_at TIMESTAMP,
	PRIMARY KEY (kommando_id AUTOINCREMENT),
	FOREIGN KEY (robo_id) REFERENCES robo(robo_id)
);


INSERT INTO robo(name, topic) VALUES
("Robo_Cedric","Wissenberg/Robo")
;