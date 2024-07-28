SELECT
  people.name
FROM
  people
  INNER JOIN stars ON stars.person_id = people.id
  INNER JOIN movies ON stars.movie_id = movies.id
WHERE
  movies.title = 'Toy Story';