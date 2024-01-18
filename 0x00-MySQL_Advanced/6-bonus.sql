--  script that creates a stored procedure AddBonus that adds a new correction for a student.
DELIMITER $$
CREATE PROCEDURE AddBonus (user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE project_id INT DEFAULT 0;
    DECLARE project_here BOOLEAN;

    SELECT COUNT(id) INTO project_here FROM projects WHERE name = project_name;
    IF NOT project_here THEN
        INSERT INTO projects(name) VALUES(project_name);
    END IF;
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    INSERT INTO corrections(user_id, project_id, score) VALUES (user_id, project_id, score);
END $$
DELIMITER ;