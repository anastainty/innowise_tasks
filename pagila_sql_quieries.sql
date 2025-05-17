-- Вывести количество фильмов в каждой категории, отсортировать по убыванию
SELECT
    category.name AS category,
    COUNT(film_category.film_id) AS film_count
FROM
    category
JOIN film_category ON category.category_id = film_category.category_id
GROUP BY category.name
ORDER BY film_count DESC;

-- Вывести 10 актеров, чьи фильмы большего всего арендовали, отсортировать по убыванию
SELECT
    actor.actor_id,
    actor.first_name,
    actor.last_name
FROM
    actor
JOIN film_actor ON actor.actor_id = film_actor.actor_id
JOIN inventory ON film_actor.film_id = inventory.film_id
JOIN rental ON inventory.inventory_id = rental.inventory_id
GROUP BY actor.actor_id, actor.first_name, actor.last_name
ORDER BY COUNT(rental_id) DESC
LIMIT 10;

-- Вывести категорию фильмов, на которую потратили больше всего денег
SELECT
    category.name
FROM
    category
JOIN film_category ON category.category_id = film_category.category_id
JOIN film ON film_category.film_id = film.film_id
JOIN inventory ON film.film_id = inventory.film_id
JOIN rental ON inventory.inventory_id = rental.inventory_id
JOIN payment ON  rental.rental_id = payment.rental_id
GROUP BY category.name
ORDER BY SUM(payment.amount) DESC
LIMIT 1;

-- Вывести названия фильмов, которых нет в inventory. Написать запрос без использования оператора IN
SELECT
    film.title
FROM
    film
LEFT JOIN inventory ON film.film_id = inventory.film_id
WHERE inventory.inventory_id IS NULL;

-- Вывести топ 3 актеров, которые больше всего появлялись в фильмах в категории “Children”. Если у нескольких актеров одинаковое кол-во фильмов, вывести всех
WITH actor_film_counts AS (
    SELECT
        actor.actor_id,
        actor.first_name,
        actor.last_name,
        COUNT(DISTINCT film.film_id) AS film_count,
        DENSE_RANK() OVER (ORDER BY COUNT(DISTINCT film.film_id) DESC) AS rank
    FROM
        actor
    JOIN film_actor ON actor.actor_id = film_actor.actor_id
    JOIN film ON film_actor.film_id = film.film_id
    JOIN film_category ON film.film_id = film_category.film_id
    JOIN category ON film_category.category_id = category.category_id
    WHERE category.name = 'Children'
    GROUP BY actor.actor_id, actor.first_name, actor.last_name
)
SELECT
    actor_id,
    first_name,
    last_name
FROM
    actor_film_counts
WHERE rank <= 3
ORDER BY film_count DESC;

-- Вывести города с количеством активных и неактивных клиентов (активный — customer.active = 1). Отсортировать по количеству неактивных клиентов по убыванию

-- Вывести категорию фильмов, у которой самое большое кол-во часов суммарной аренды в городах (customer.address_id в этом city), и которые начинаются на букву “a”. То же самое сделать для городов в которых есть символ “-”. Написать все в одном запросе