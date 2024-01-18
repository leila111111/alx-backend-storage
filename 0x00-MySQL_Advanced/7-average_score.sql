-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.
DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    DECLARE new_score INT DEFAULT 0;

    SELECT AVG(score) INTO new_score FROM corrections WHERE user_id = user_id;
    UPDATE users SET average_score = new_score WHERE id = user_id;
END $$
DELIMITER ;
