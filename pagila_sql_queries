-- Вывести количество фильмов в каждой категории, отсортировать по убыванию
SELECT
    category.name AS category,
    COUNT(film_category.film_id) AS film_count
FROM
    category
JOIN
    film_category ON category.category_id = film_category.category_id
GROUP BY
    category.name
ORDER BY
    film_count DESC;

-- Вывести 10 актеров, чьи фильмы большего всего арендовали, отсортировать по убыванию
