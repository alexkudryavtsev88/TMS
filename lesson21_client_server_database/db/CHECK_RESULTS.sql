SELECT DISTINCT u.name, u.age, p.id, p.title, p.description, com.title, count(l.id) as likes_count
FROM posts p
LEFT JOIN comments com ON p.id = com.post_id
LEFT JOIN likes l ON p.id = l.post_id
JOIN users u ON u.id = p.user_id
GROUP BY u.id, p.id, com.id
ORDER BY p.id, likes_count DESC;
