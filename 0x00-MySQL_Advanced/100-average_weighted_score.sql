-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE average_weighted_score INT DEFAULT 0;

    SELECT COALESCE(SUM(corrections.score * projects.weight) / NULLIF(SUM(projects.weight), 0), 0)
        INTO average_weighted_score
        FROM corrections
            INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    UPDATE users
        SET users.average_score = average_weighted_score
        WHERE users.id = user_id;
END $$
DELIMITER ;