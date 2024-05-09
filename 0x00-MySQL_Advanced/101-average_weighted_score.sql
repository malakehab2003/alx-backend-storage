-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    ALTER TABLE users ADD weight_score INT NOT NULL;
    ALTER TABLE users ADD wght INT NOT NULL;

    UPDATE users
        SET weight_score = (
            SELECT SUM(corrections.score * projects.weight)
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
            );

    UPDATE users
        SET wght = (
            SELECT SUM(projects.weight)
                FROM corrections
                    INNER JOIN projects
                        ON corrections.project_id = projects.id
                WHERE corrections.user_id = users.id
            );

    UPDATE users
        SET users.average_score = IF(users.wght = 0, 0, users.weight_score / users.wght);
    ALTER TABLE users
        DROP COLUMN weight_score;
    ALTER TABLE users
        DROP COLUMN wght;
END $$
DELIMITER ;
