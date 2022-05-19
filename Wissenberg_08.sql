SELECT * FROM robo LEFT JOIN kommando USING (robo_id) ORDER BY received_at;
