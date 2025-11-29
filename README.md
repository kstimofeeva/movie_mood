# movie_mood
1. PostgreSQL схема
база данных состоит из двух таблиц (movies, reviews)
movies содержит атрибуты: id, title, genre, description, mood, created_at
reviews содержит атрибуты: id, movie_id, review_text, sentiment, sentiment_score, created_at
2. в models были добавлены две модели (для фильмов и отзывов соответственно)
3. в database добавлен класс для бд (создание таблиц, создание бд, создание сессий)
4. созданы классы для возврата пользователю информации о отзывах и фильмах (а также добавление отзывов и фильмов и изменения информации о фильмах)
5. 