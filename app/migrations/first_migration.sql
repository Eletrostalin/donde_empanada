-- Установка настроек базы данных
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';
SET default_table_access_method = heap;

-- Создание таблицы alembic_version
CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
ALTER TABLE public.alembic_version OWNER TO postgres;

-- Создание таблицы location
CREATE TABLE public.location (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    description text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    average_rating double precision NOT NULL,
    rating_count integer,
    created_by integer NOT NULL,
    created_at timestamp without time zone,
    address character varying(255),
    working_hours character varying(255),
    average_check integer
);
ALTER TABLE public.location OWNER TO postgres;

CREATE SEQUENCE public.location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.location_id_seq OWNER TO postgres;
ALTER SEQUENCE public.location_id_seq OWNED BY public.location.id;

-- Создание таблицы owner_info
CREATE TABLE public.owner_info (
    id integer NOT NULL,
    user_id integer NOT NULL,
    location_id integer NOT NULL,
    website character varying(200),
    owner_info text NOT NULL
);
ALTER TABLE public.owner_info OWNER TO postgres;

CREATE SEQUENCE public.owner_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.owner_info_id_seq OWNER TO postgres;
ALTER SEQUENCE public.owner_info_id_seq OWNED BY public.owner_info.id;

-- Создание таблицы review
CREATE TABLE public.review (
    id integer NOT NULL,
    user_id integer NOT NULL,
    location_id integer NOT NULL,
    rating integer NOT NULL,
    comment text NOT NULL,
    created_at timestamp without time zone
);
ALTER TABLE public.review OWNER TO postgres;

CREATE SEQUENCE public.review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.review_id_seq OWNER TO postgres;
ALTER SEQUENCE public.review_id_seq OWNED BY public.review.id;

-- Создание таблицы user
CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(150) NOT NULL,
    email character varying(150),
    password_hash character varying(256) NOT NULL,
    first_name character varying(150) NOT NULL,
    second_name character varying(150) NOT NULL,
    phone_hash character varying(256) NOT NULL
);
ALTER TABLE public."user" OWNER TO postgres;

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.user_id_seq OWNER TO postgres;
ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;

-- Установка значений по умолчанию для ID
ALTER TABLE ONLY public.location ALTER COLUMN id SET DEFAULT nextval('public.location_id_seq'::regclass);
ALTER TABLE ONLY public.owner_info ALTER COLUMN id SET DEFAULT nextval('public.owner_info_id_seq'::regclass);
ALTER TABLE ONLY public.review ALTER COLUMN id SET DEFAULT nextval('public.review_id_seq'::regclass);
ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);

-- Установка последовательностей
SELECT pg_catalog.setval('public.location_id_seq', 7, true);
SELECT pg_catalog.setval('public.owner_info_id_seq', 1, false);
SELECT pg_catalog.setval('public.review_id_seq', 3, true);
SELECT pg_catalog.setval('public.user_id_seq', 22, true);

-- Создание первичных и уникальных ключей
ALTER TABLE ONLY public.alembic_version ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
ALTER TABLE ONLY public.location ADD CONSTRAINT location_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.owner_info ADD CONSTRAINT owner_info_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.review ADD CONSTRAINT review_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public."user" ADD CONSTRAINT user_phone_hash_key UNIQUE (phone_hash);
ALTER TABLE ONLY public."user" ADD CONSTRAINT user_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public."user" ADD CONSTRAINT user_username_key UNIQUE (username);

-- Установка внешних ключей
ALTER TABLE ONLY public.location ADD CONSTRAINT location_created_by_fkey FOREIGN KEY (created_by) REFERENCES public."user"(id);
ALTER TABLE ONLY public.owner_info ADD CONSTRAINT owner_info_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.location(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.owner_info ADD CONSTRAINT owner_info_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;
ALTER TABLE ONLY public.review ADD CONSTRAINT review_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.location(id);
ALTER TABLE ONLY public.review ADD CONSTRAINT review_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);
