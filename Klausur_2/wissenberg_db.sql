CREATE TABLE motor(
	motor_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255),
	position VARCHAR(255)
);

CREATE TABLE command (
	command_id INTEGER PRIMARY KEY AUTOINCREMENT,
	motor_id INTEGER,
	vorwaerts INTEGER,
	rueckwaerts INTEGER,
	timestamp VARCHAR(255)
);

INSERT INTO motor (name, position) VALUES
	("Motor 1", "Linke Seite vom Robo"),
	("Motor 2", "Rechte Seite vom Robo")
;



sqlite> .headers on
sqlite> .mode csv
sqlite> .output data.csv
sqlite> SELECT * FROM command WHERE motor_id = 1 ORDER BY timestamp;
sqlite> .quit