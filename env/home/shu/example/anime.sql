

CREATE TABLE anime (
    mal_id int,
    title text,
    type text,
    source text,
    genre_action boolean,
    genre_adventure boolean,
    genre_comedy boolean,
    genre_dementia boolean,
    genre_demons boolean,
    genre_drama boolean,
    genre_ecchi boolean,
    genre_fantasy boolean,
    genre_game boolean,
    genre_harem boolean,
    genre_historical boolean,
    genre_horror boolean,
    genre_josei boolean,
    genre_magic boolean,
    genre_martial_arts boolean,
    genre_mecha boolean,
    genre_military boolean,
    genre_music boolean,
    genre_mystery boolean,
    genre_parody boolean,
    genre_police boolean,
    genre_psychological boolean,
    genre_romance boolean,
    genre_samurai boolean,
    genre_school boolean,
    genre_sci_fi boolean,
    genre_seinen boolean,
    genre_shoujo boolean,
    genre_shoujo_ai boolean,
    genre_shounen boolean,
    genre_slice_of_life boolean,
    genre_space boolean,
    genre_sports boolean,
    genre_super_power boolean,
    genre_supernatural boolean,
    genre_thriller boolean,
    genre_vampire boolean,
    age_rating text,

    year int,
    season text,
    air_start timestamp,
    air_end timestamp,

    episode_duration int,
    episodes int,

    score float,
    score_rank int,
    members int,
    favorites int,
    popularity_rank int,

    studio text,
    producer text,
    licensor text,

    url text,
    url_image text
);

COPY anime FROM '/home/data/anime.tsv' DELIMITER E'\t' CSV HEADER;


