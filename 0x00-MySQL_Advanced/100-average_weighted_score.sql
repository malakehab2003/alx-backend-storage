-- creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE weight_score INT DEFAULT 0;
    DECLARE wght INT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight)
    INTO weight_score
    FROM corrections
    JOIN projects
    ON projects.id = corrections.project_id
    WHERE corrections.user_id = user_id;

    SELECT SUM(projects.weight)
    INTO wght
    FROM projects
    JOIN corrections
    ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    IF wght = 0 THEN
	UPDATE users
        SET users.average_score = 0
        WHERE user_id = users.id;
    ELSE
        UPDATE users
        SET users.average_score = weight_score / wght
        WHERE user_id = users.id;
    END IF;
END $$
DELIMITER ;
