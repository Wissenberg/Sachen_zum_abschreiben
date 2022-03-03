CREATE TABLE Robo (
	robo_id INTEGER PRIMARY KEY AUTOINCREMENT,
	robo_name VARCHAR(255),
	topic VARCHAR(255)
);

CREATE TABLE Makro(
	makro_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(255)
);

CREATE TABLE Kommandos (
	kommando_id INTEGER PRIMARY KEY AUTOINCREMENT,
	robo_id INT,
	send_at DATETIME,
	makro_id INT,
	move INT,
	turn INT,
	FOREIGN KEY (robo_id) REFERENCES Robo (robo_id),
	FOREIGN KEY (makro_id) REFERENCES Makro (makro_id)
);