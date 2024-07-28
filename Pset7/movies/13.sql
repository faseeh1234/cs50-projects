SELECT
  name
FROM
  people,
  stars
WHERE
  movie_id IN (
    SELECT
      movie_id
    FROM
      people,
      stars
    WHERE
      name = 'Kevin Bacon'
      AND birth = 1958
      AND id = person_id
  )
  AND id = person_id
  AND NOT (
    name = 'Kevin Bacon'
    AND birth = 1958
  );