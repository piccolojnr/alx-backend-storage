-- script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

-- Requirements:

-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)


DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE avg_score FLOAT;
    DECLARE total_score FLOAT;
    
	-- Calculate the total score for the user
    SELECT SUM(score) INTO total_score 
    FROM corrections
    WHERE user_id = user_id;
    
    -- Calculate the average weighted score for the user
    SELECT SUM(score / total_score * score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    SELECT avg_score;    
END //
DELIMITER ;

call ComputeAverageWeightedScoreForUser (1);
