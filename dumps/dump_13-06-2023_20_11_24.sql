--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases (except postgres and template1)
--





--
-- Drop roles
--

DROP ROLE postgres;


--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:zS+Ar8lYVy7/qU363lCAbw==$fBzeAaqLVOLJ3f1QE1VsvbpVTQdB9KNLuOnysyx44M8=:8zN9p/9vWWmuGRzPs9KDqVzGua/+W5s13U+yr0qOCvs=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

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

UPDATE pg_catalog.pg_database SET datistemplate = false WHERE datname = 'template1';
DROP DATABASE template1;
--
-- Name: template1; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE template1 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE template1 OWNER TO postgres;

\connect template1

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

--
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: template1; Type: DATABASE PROPERTIES; Schema: -; Owner: postgres
--

ALTER DATABASE template1 IS_TEMPLATE = true;


\connect template1

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

--
-- Name: DATABASE template1; Type: ACL; Schema: -; Owner: postgres
--

REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

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

DROP DATABASE postgres;
--
-- Name: postgres; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE postgres OWNER TO postgres;

\connect postgres

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

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Animal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Animal" (
    animal_id character varying NOT NULL
);


ALTER TABLE public."Animal" OWNER TO postgres;

--
-- Name: Houses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Houses" (
    house_id integer NOT NULL,
    description character varying,
    start_date timestamp without time zone,
    end_date timestamp without time zone,
    available boolean,
    owner_id integer,
    rooms integer,
    city character varying,
    image1 character varying,
    image2 character varying,
    image3 character varying,
    image4 character varying,
    image5 character varying
);


ALTER TABLE public."Houses" OWNER TO postgres;

--
-- Name: Houses_house_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Houses_house_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Houses_house_id_seq" OWNER TO postgres;

--
-- Name: Houses_house_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Houses_house_id_seq" OWNED BY public."Houses".house_id;


--
-- Name: Pet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Pet" (
    pet_id integer NOT NULL,
    animal_id character varying,
    house_id integer,
    pet_cant integer
);


ALTER TABLE public."Pet" OWNER TO postgres;

--
-- Name: Pet_pet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Pet_pet_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Pet_pet_id_seq" OWNER TO postgres;

--
-- Name: Pet_pet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Pet_pet_id_seq" OWNED BY public."Pet".pet_id;


--
-- Name: Ratings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Ratings" (
    user_id character varying NOT NULL,
    house_id character varying NOT NULL,
    rating integer,
    comment character varying
);


ALTER TABLE public."Ratings" OWNER TO postgres;

--
-- Name: RatingsHouses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."RatingsHouses" (
    user_id character varying NOT NULL,
    house_id character varying NOT NULL,
    rating integer,
    comment character varying
);


ALTER TABLE public."RatingsHouses" OWNER TO postgres;

--
-- Name: User_applications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."User_applications" (
    user_application_id integer NOT NULL,
    user_id integer,
    house_id integer,
    accepted boolean
);


ALTER TABLE public."User_applications" OWNER TO postgres;

--
-- Name: User_applications_user_application_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."User_applications_user_application_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_applications_user_application_id_seq" OWNER TO postgres;

--
-- Name: User_applications_user_application_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."User_applications_user_application_id_seq" OWNED BY public."User_applications".user_application_id;


--
-- Name: Users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Users" (
    user_id integer NOT NULL,
    username character varying,
    password character varying,
    country character varying,
    age integer,
    description character varying,
    photo_url character varying
);


ALTER TABLE public."Users" OWNER TO postgres;

--
-- Name: Users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Users_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Users_user_id_seq" OWNER TO postgres;

--
-- Name: Users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Users_user_id_seq" OWNED BY public."Users".user_id;


--
-- Name: Houses house_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Houses" ALTER COLUMN house_id SET DEFAULT nextval('public."Houses_house_id_seq"'::regclass);


--
-- Name: Pet pet_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Pet" ALTER COLUMN pet_id SET DEFAULT nextval('public."Pet_pet_id_seq"'::regclass);


--
-- Name: User_applications user_application_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User_applications" ALTER COLUMN user_application_id SET DEFAULT nextval('public."User_applications_user_application_id_seq"'::regclass);


--
-- Name: Users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users" ALTER COLUMN user_id SET DEFAULT nextval('public."Users_user_id_seq"'::regclass);


--
-- Data for Name: Animal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Animal" (animal_id) FROM stdin;
Perro
Gato
Ave
Pez
Otro
\.


--
-- Data for Name: Houses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Houses" (house_id, description, start_date, end_date, available, owner_id, rooms, city, image1, image2, image3, image4, image5) FROM stdin;
2	Bungalow en el Tigre donde vive un perrito callejero que todos los dias se acerca a comer algo y jugar.	2023-04-05 00:00:00	2023-05-12 00:00:00	f	1	1	Tigre	https://media-cdn.tripadvisor.com/media/photo-s/11/5c/14/d1/bungalow.jpg	https://cdn.pixabay.com/photo/2017/10/10/15/38/sleeping-dog-2837631_1280.jpg	\N	\N	\N
3	Monoambiente en palermo con un perro caniche y un pececito dorado. Son amigos entre si.	2023-03-03 00:00:00	2023-03-30 00:00:00	f	2	1	buenos aires	https://previews.123rf.com/images/iridi/iridi2102/iridi210200229/163581813-un-perro-con-un-sombrero-de-paja-est%C3%A1-pescando-en-una-bola-de-acuario-atrap%C3%B3-un-pez-dorado-fondo.jpg	https://imgar.zonapropcdn.com/avisos/1/00/47/20/83/76/720x532/1751800804.jpg	\N	\N	\N
4	Hola mis parceros estoy buscando quien cuide mi casa en Medellin donde tengo mis panas mascotas: un perrito llamado Maluma, un gatito llamado J Balvin y un pajarito llamado James.	2023-07-01 00:00:00	2023-07-15 00:00:00	t	4	2	Medellin	https://www.revistaaxxis.com.co/wp-content/uploads/2021/07/imagen-21.png	https://res.cloudinary.com/postedin/image/upload/d_mascotas:no-image.jpg,w_340,c_thumb,f_auto,q_80/mascotas/c-4e0e1a5c0b.jpg	\N	\N	\N
5	Casa en rio de janeiro con dos perritos.	2023-08-01 00:00:00	2023-09-01 00:00:00	t	3	2	Rio de Janeiro	https://media.rightmove.co.uk/107k/106120/133402394/106120_41CA_IMG_00_0000.jpeg	https://media.rightmove.co.uk/107k/106120/133402394/106120_41CA_IMG_01_0000.jpeg	https://media.rightmove.co.uk/107k/106120/133402394/106120_41CA_IMG_02_0000.jpeg	\N	\N
1	Casa situada en el barrio de caballito, buenos aires. Viven dos gatitos, uno negro y el otro blanco, muy amigables aunque inicialmente desconfían de los extraños.	2023-08-01 00:00:00	2023-09-01 00:00:00	f	1	3	Buenos aires	https://elcorreoweb.es/binrepository/761x400/43c0/675d400/none/10703/BDIX/eca-gatos-negros_20980457_20221227101253.jpg	https://www.rionegro.com.ar/wp-content/uploads/2022/12/portada-2.jpg?w=1099	https://static.tokkobroker.com/pictures/7812695845489170082879630586200096639599879815801249528266590723955910382182.jpg	\N	\N
\.


--
-- Data for Name: Pet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Pet" (pet_id, animal_id, house_id, pet_cant) FROM stdin;
1	Gato	1	2
2	Perro	2	1
3	Perro	3	1
4	Pez	3	1
5	Perro	4	1
6	Gato	4	1
7	Ave	4	1
8	Perro	5	2
\.


--
-- Data for Name: Ratings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Ratings" (user_id, house_id, rating, comment) FROM stdin;
2	2	5	Muy amigable con los animales pero dejo un poco sucio.
1	3	3	muy bueno
\.


--
-- Data for Name: RatingsHouses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."RatingsHouses" (user_id, house_id, rating, comment) FROM stdin;
2	2	3	Muy agradable casa pero el perrito estaba un poco roñoso.
1	3	4	esta casa es muy agradable!
\.


--
-- Data for Name: User_applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."User_applications" (user_application_id, user_id, house_id, accepted) FROM stdin;
2	2	2	t
3	1	3	t
4	3	1	f
5	3	1	f
1	2	1	t
6	2	5	\N
\.


--
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Users" (user_id, username, password, country, age, description, photo_url) FROM stdin;
1	joaquin@gmail.com	123456789	Argentina	36	Hola soy Joaquin de Argentina. Me gustan mucho los gatitos y viajar por el mundo conociendo lugares y personas nuevas.	https://cloudfront-us-east-1.images.arcpublishing.com/infobae/CAVJTK7RYJCZDLUGUEFH4NTXDA.jpg
2	leonardo@gmail.com	123456789	Argentina	24	Soy Leonardo! Me gustan los perros y jugar al futbol y al padel. Me gusta viajar y cuidar mascotas, sabiendo que mis propias mascotas también están siendo cuidadas.	https://www.eldiariocba.com.ar/u/fotografias/fotosnoticias/2022/12/21/93486.jpg
4	francisco@gmail.com	123456789	Colombia	29	Hola mis panas soy Francisco de medellin, colombia. Me gustan todo tipo de animales y viajar bien chimba. 	https://www.elgrafico.com.ar/media/cache/pub_news_details_large/media/i/68/6d/686d1e80974eea2e71fc3760961d4d89db9f217e.JPG
3	neymar@gmail.com	123456789	Brasil	31	Meu nome é Neymar Jr, gosto de viajar o mundo e festejar. Se eu tiver tempo quando chegar de uma festa, posso cuidar de animais. 	https://www.elnacional.cat/enblau/uploads/s1/66/51/27/6/neymar-festa-gtres.jpeg
\.


--
-- Name: Houses_house_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Houses_house_id_seq"', 5, true);


--
-- Name: Pet_pet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Pet_pet_id_seq"', 8, true);


--
-- Name: User_applications_user_application_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."User_applications_user_application_id_seq"', 6, true);


--
-- Name: Users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Users_user_id_seq"', 4, true);


--
-- Name: Animal Animal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Animal"
    ADD CONSTRAINT "Animal_pkey" PRIMARY KEY (animal_id);


--
-- Name: Houses Houses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Houses"
    ADD CONSTRAINT "Houses_pkey" PRIMARY KEY (house_id);


--
-- Name: Pet Pet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Pet"
    ADD CONSTRAINT "Pet_pkey" PRIMARY KEY (pet_id);


--
-- Name: RatingsHouses RatingsHouses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."RatingsHouses"
    ADD CONSTRAINT "RatingsHouses_pkey" PRIMARY KEY (user_id, house_id);


--
-- Name: Ratings Ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Ratings"
    ADD CONSTRAINT "Ratings_pkey" PRIMARY KEY (user_id, house_id);


--
-- Name: User_applications User_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User_applications"
    ADD CONSTRAINT "User_applications_pkey" PRIMARY KEY (user_application_id);


--
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (user_id);


--
-- Name: Houses Houses_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Houses"
    ADD CONSTRAINT "Houses_owner_id_fkey" FOREIGN KEY (owner_id) REFERENCES public."Users"(user_id);


--
-- Name: Pet Pet_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Pet"
    ADD CONSTRAINT "Pet_animal_id_fkey" FOREIGN KEY (animal_id) REFERENCES public."Animal"(animal_id);


--
-- Name: Pet Pet_house_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Pet"
    ADD CONSTRAINT "Pet_house_id_fkey" FOREIGN KEY (house_id) REFERENCES public."Houses"(house_id);


--
-- Name: User_applications User_applications_house_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User_applications"
    ADD CONSTRAINT "User_applications_house_id_fkey" FOREIGN KEY (house_id) REFERENCES public."Houses"(house_id);


--
-- Name: User_applications User_applications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User_applications"
    ADD CONSTRAINT "User_applications_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."Users"(user_id);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

