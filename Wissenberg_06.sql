CREATE TABLE robo (
	robo_id INTEGER,
	name VARCHAR(255),
	PRIMARY KEY(robo_id AUTOINCREMENT)
);


CREATE TABLE kommando (
	kommando_id INTEGER,
	direction FLOAT,
	turn INTEGER,
	robo_id INTEGER,
	received_at TIMESTAMP,
	PRIMARY KEY (kommando_id AUTOINCREMENT),
	FOREIGN KEY (robo_id) REFERENCES robo(robo_id)
);


INSERT INTO robo(name) VALUES
("car_Wissenberg")
;