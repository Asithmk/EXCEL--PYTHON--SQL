
USE student_analytics;

-- 1. View all students
SELECT *
FROM students;

-- 2. Average student grade
SELECT ROUND(AVG(average_grade), 2) AS average_grade
FROM students;

-- 3. Average living cost
SELECT ROUND(AVG(total_living_cost), 2) AS average_living_cost
FROM students;

-- 4. Living costs by nationality
SELECT
    nationality,
    COUNT(*) AS student_count,
    ROUND(AVG(total_living_cost), 2) AS average_living_cost
FROM students
GROUP BY nationality
ORDER BY average_living_cost DESC;

-- 5. Student with the highest living cost
SELECT
    name,
    nationality,
    total_living_cost
FROM students
ORDER BY total_living_cost DESC
LIMIT 1;

-- 6. Ambition distribution
SELECT
    ambition,
    ambition_score,
    COUNT(*) AS student_count
FROM students
GROUP BY ambition, ambition_score
ORDER BY ambition_score DESC;

-- 7. Students with above-average living costs
SELECT
    name,
    total_living_cost
FROM students
WHERE total_living_cost > (
    SELECT AVG(total_living_cost)
    FROM students
);
