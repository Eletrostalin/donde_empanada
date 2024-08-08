-- Создание таблицы пользователя
CREATE TABLE public."user" (
    id SERIAL PRIMARY KEY,
    username character varying(150) NOT NULL,
    email character varying(150),
    password_hash character varying(256) NOT NULL,
    first_name character varying(150) NOT NULL,
    second_name character varying(150) NOT NULL,
    phone_hash character varying(256) UNIQUE NOT NULL
);

-- Создание таблицы локации
CREATE TABLE public.location (
    id SERIAL PRIMARY KEY,
    name character varying(150) NOT NULL,
    description text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    average_rating double precision NOT NULL,
    rating_count integer,
    created_by integer NOT NULL REFERENCES public."user"(id),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    address character varying(255),
    working_hours character varying(255),
    average_check integer
);

-- Создание таблицы информации владельца
CREATE TABLE public.owner_info (
    id SERIAL PRIMARY KEY,
    user_id integer NOT NULL REFERENCES public."user"(id) ON DELETE CASCADE,
    location_id integer NOT NULL REFERENCES public.location(id) ON DELETE CASCADE,
    website character varying(200),
    owner_info text NOT NULL
);

-- Создание таблицы отзывов
CREATE TABLE public.review (
    id SERIAL PRIMARY KEY,
    user_id integer NOT NULL REFERENCES public."user"(id),
    location_id integer NOT NULL REFERENCES public.location(id),
    rating integer NOT NULL,
    comment text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы миграций
CREATE TABLE public.migrations (
    id SERIAL PRIMARY KEY,
    migration_name character varying(255) NOT NULL UNIQUE,
    applied_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
