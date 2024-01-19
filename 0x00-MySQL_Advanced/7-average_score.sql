-- SQL script that creates a stored procedure ComputeAverageScoreForUser that
-- computes and store the average score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
    DECLARE total INT DEFAULT 0;
    DECLARE num_projects INT DEFAULT 0;

    SELECT COUNT(*) INTO num_projects FROM corrections WHERE corrections.user_id = user_id;
    SELECT SUM(score) INTO total FROM corrections WHERE corrections.user_id = user_id;

    UPDATE users
        SET users.average_score = IF(num_projects = 0, 0, total / num_projects)
        WHERE users.id = user_id;
END $$
DELIMITER ;