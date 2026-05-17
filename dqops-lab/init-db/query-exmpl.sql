-- 
CREATE TABLE public.movie_events (
    event_id      INTEGER PRIMARY KEY,
    user_id       INTEGER NOT NULL,
    movie_id      INTEGER NOT NULL,
    event_type    VARCHAR(30) NOT NULL,
    event_ts      TIMESTAMP NOT NULL,
    watch_seconds INTEGER
);

INSERT INTO public.movie_events
(event_id, user_id, movie_id, event_type, event_ts, watch_seconds)
VALUES
(1, 101, 501, 'click', '2026-05-01 10:00:00', NULL),
(2, 101, 501, 'play',  '2026-05-01 10:01:00', 120),
(3, 102, 502, 'click', '2026-05-01 10:05:00', NULL),
(4, 103, 503, 'play',  '2026-05-01 10:10:00', 300),
(5, 104, 504, 'play',  '2026-05-01 10:20:00', 60);