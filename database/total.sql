
SELECT
    (SELECT COUNT(`identifier`) FROM `classes`) AS `classes`,
    (SELECT COUNT(`identifier`) FROM `students_in_classes`) AS `students`,
    (SELECT COUNT(`identifier`) FROM `student_connection_history`) AS `history`,

    (SELECT COUNT(`identifier`) FROM `questions`) AS `questions`,
    (SELECT COUNT(`identifier`) FROM `question_options`) AS `options`,
    (SELECT COUNT(`identifier`) FROM `student_answers`) AS `answers`;
