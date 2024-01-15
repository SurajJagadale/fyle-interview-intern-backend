-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grades AS (
    SELECT teacher_id, COUNT(*) as total_grades
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
max_grades_teacher AS (
    SELECT teacher_id
    FROM teacher_grades
    ORDER BY total_grades DESC
    LIMIT 1
)
SELECT teacher_id, COUNT(*)
FROM assignments
WHERE teacher_id = (SELECT teacher_id FROM max_grades_teacher)
AND grade = 'A';
