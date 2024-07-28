SELECT
  title,
  rating
FROM
  movies,
  ratings
WHERE
  id = movie_id
  AND YEAR = 2010
ORDER BY
  rating DESC,
  title ASC;