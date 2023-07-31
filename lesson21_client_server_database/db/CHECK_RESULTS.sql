SELECT
    u.id AS USER_ID,
    u.name AS USER_NAME,
    u.age AS USER_AGE,
    p.id AS POST_ID,
    p.title AS POST_TITLE,
    p.description AS POST_DESCRIPTION,
    com.id AS COMMENT_ID,
    com.title AS COMMENT_TITLE,
    count(l.id) as LIKES_COUNT
FROM posts p
LEFT JOIN comments com ON p.id = com.post_id
LEFT JOIN likes l ON p.id = l.post_id
JOIN users u ON u.id = p.user_id
GROUP BY u.id, p.id, com.id
ORDER BY p.id, likes_count DESC;
