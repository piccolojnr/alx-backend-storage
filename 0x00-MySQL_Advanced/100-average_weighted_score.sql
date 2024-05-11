-- script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

-- Requirements:

-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE average_score FLOAT;
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;
    
	-- Calculate the total score for the user
    SELECT SUM(c.score * p.weight)
        INTO total_score
        FROM corrections as c
            INNER JOIN projects as p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    
    SELECT SUM(projects.weight)
        INTO total_weight
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    IF total_weight > 0 THEN
        SET average_score = total_score / total_weight;
    ELSE
        SET average_score = 0;
    END IF;
    
    
    -- Update the users table with the computed average_score
    UPDATE users
    SET average_score = average_score
    WHERE id = p_user_id;

END //

DELIMITER ;