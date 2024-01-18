-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE total_score INT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    SELECT SUM(projects.weight) INTO total_weight FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
            WHERE corrections.user_id = user_id;
    SELECT SUM(corrections.score * projects.weight) INTO total_score FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
            WHERE corrections.user_id = user_id;
    UPDATE users
    SET users.average_score = CASE
        WHEN total_weight = 0 THEN 0
        ELSE total_score / total_weight
END
WHERE users.id = user_id;

END $$
DELIMITER ;