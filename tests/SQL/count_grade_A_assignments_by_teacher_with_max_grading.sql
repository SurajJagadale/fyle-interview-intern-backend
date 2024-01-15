-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH GradedAssignments AS (
    SELECT teacher_id, COUNT(*) AS graded_count
    FROM assignments
    WHERE state = 'GRADED' AND grade = 'A'
    GROUP BY teacher_id
)

SELECT teacher_id, graded_count
FROM GradedAssignments
ORDER BY graded_count DESC
LIMIT 1;