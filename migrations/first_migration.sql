--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

-- Started on 2024-08-03 12:28:48 -04

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

--
-- TOC entry 215 (class 1259 OID 16634)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16704)
-- Name: location; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- TOC entry 218 (class 1259 OID 16703)
-- Name: location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.location_id_seq OWNER TO postgres;

--
-- TOC entry 3642 (class 0 OID 0)
-- Dependencies: 218
-- Name: location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.location_id_seq OWNED BY public.location.id;


--
-- TOC entry 223 (class 1259 OID 16788)
-- Name: owner_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.owner_info (
    id integer NOT NULL,
    user_id integer NOT NULL,
    location_id integer NOT NULL,
    website character varying(200),
    owner_info text NOT NULL
);


ALTER TABLE public.owner_info OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16787)
-- Name: owner_info_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.owner_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.owner_info_id_seq OWNER TO postgres;

--
-- TOC entry 3643 (class 0 OID 0)
-- Dependencies: 222
-- Name: owner_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.owner_info_id_seq OWNED BY public.owner_info.id;


--
-- TOC entry 221 (class 1259 OID 16718)
-- Name: review; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.review (
    id integer NOT NULL,
    user_id integer NOT NULL,
    location_id integer NOT NULL,
    rating integer NOT NULL,
    comment text NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.review OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16717)
-- Name: review_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.review_id_seq OWNER TO postgres;

--
-- TOC entry 3644 (class 0 OID 0)
-- Dependencies: 220
-- Name: review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.review_id_seq OWNED BY public.review.id;


--
-- TOC entry 217 (class 1259 OID 16691)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

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

--
-- TOC entry 216 (class 1259 OID 16690)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO postgres;

--
-- TOC entry 3645 (class 0 OID 0)
-- Dependencies: 216
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- TOC entry 3463 (class 2604 OID 16707)
-- Name: location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location ALTER COLUMN id SET DEFAULT nextval('public.location_id_seq'::regclass);


--
-- TOC entry 3465 (class 2604 OID 16791)
-- Name: owner_info id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.owner_info ALTER COLUMN id SET DEFAULT nextval('public.owner_info_id_seq'::regclass);


--
-- TOC entry 3464 (class 2604 OID 16721)
-- Name: review id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review ALTER COLUMN id SET DEFAULT nextval('public.review_id_seq'::regclass);


--
-- TOC entry 3462 (class 2604 OID 16694)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 3628 (class 0 OID 16634)
-- Dependencies: 215
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
93c2e0ac29df
\.


--
-- TOC entry 3632 (class 0 OID 16704)
-- Dependencies: 219
-- Data for Name: location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location (id, name, description, latitude, longitude, average_rating, rating_count, created_by, created_at, address, working_hours, average_check) FROM stdin;
1	тест	вкусно	55.71738763912856	37.6248937988281	0	0	3	2024-07-23 06:30:32.118531	городская 2	сегодня2	222
2	Названи	вуукцкцук	55.68171231913251	37.60704101562498	0	0	8	2024-07-23 08:56:40.890115	цваы343	121	1211
3	йцуцук	йкйцукцук	55.72126342103643	37.60704101562498	0	0	8	2024-07-23 10:32:28.423259	йцукцук	1231	123123
4	йцуцук	йкйцукцук	55.72126342103643	37.60704101562498	0	0	8	2024-07-23 10:32:28.509473	йцукцук	1231	123123
5	qwerq	rqwrqwr	55.709634916485385	37.615280761718736	0	0	8	2024-07-24 17:21:11.2358	qwerqwer	123	1233
7	qerqwr11	qwreqwr	55.63971064948229	37.546188867187496	0	0	8	2024-08-02 16:39:59.991655	qwerqwr	12412	1242144
6	qwersdfa	asdfa	55.649886444205436	37.73247867683172	3.3333333333333335	3	8	2024-07-28 11:55:36.991391	qwer	12	213
\.


--
-- TOC entry 3636 (class 0 OID 16788)
-- Dependencies: 223
-- Data for Name: owner_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.owner_info (id, user_id, location_id, website, owner_info) FROM stdin;
\.


--
-- TOC entry 3634 (class 0 OID 16718)
-- Dependencies: 221
-- Data for Name: review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.review (id, user_id, location_id, rating, comment, created_at) FROM stdin;
1	8	6	5	супер	2024-07-28 19:48:53.463326
2	8	6	1	й3йцуУ	2024-07-28 20:08:36.533234
3	8	6	4	werwrwrwr	2024-08-03 09:38:54.411799
\.


--
-- TOC entry 3630 (class 0 OID 16691)
-- Dependencies: 217
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, email, password_hash, first_name, second_name, phone_hash) FROM stdin;
1	 Никитос	Stanchenkovn@yandex.ru	scrypt:32768:8:1$37LgSfA3R4vT9FEP$d6b09eb4483436ed22fd9074f960b91d07ff526e03fcb3f90b235b14fa81b658dcf626f11e8864218573de1c45fb82cc59d0a38307b1eb3914b0bd36b3695075	Никита	Иванов	15fcdf6dcf96c9584f2f1a0dae32f3282565b02e9483ed08723cd2c096ee6bf6
3	Тест	Stanchenkovnd@yandex.ru	scrypt:32768:8:1$tKfdOgJ5KiDUcIcL$07437c9ddae4b00d48b09378ace066eed27c8d005c2e3c65673a8af0a28969007ae220d1c0747f3a204ad02c7e115d73a9231bdd8f3560ace906f93bb28e982a	Никита	Иванов	0d0f120d6e7ae16336f1d079d8c33a3de755c5a04e3f9edf2ea35e4531dc3139
4	Тестовый	mafnuty@yandex.ru	scrypt:32768:8:1$fNN3q3qokHabxi40$796ce8a70f8df5c98003fb5aaf7edeeceea08df62cd2405c221ea54431baa92b30ffd728a1bc93b1d534e2df2ad6c4d35868ebe64fe37c528e7ac813b2a9f4a7	имя	имя22	scrypt:32768:8:1$uhzYU55Bu9FcfrVf$14b5a766798c52a110b442953f6c513ddfeef2a7b67834216e7bce44fe3426546e1061db0c80dfb25617ac4fb4fb9a123bb8590baaabb87f3d476b306221a2f0
6	123123	Mafnutyyy@yandex.ru	scrypt:32768:8:1$ShGezHp9YBzB6xdo$6458918cb2201a865478d7719e5d581f69c86bd083a1e07a0f83894d1df752b28bd2ef37c7e20fb5e95035ed37163e1dbfc789f6dbd8ee09ec8dc2af9f5ff486	никита	вававаа	scrypt:32768:8:1$5q9HufzjXrXLEVDN$7d7615ed61f69b3819275db42610b6d484d6b1d6cea08fa555bf26af56087e2607d6c5e3207db84381d3b1adcc9d710bf4a36ec69e6821b74976a33cb61c6daa
7	123		scrypt:32768:8:1$mDpp65AbSt6OXe4m$4174d193688d9a6e8e4b769c9238e74ca3d7c9a5a586fe42c66f1c309938417091acbf02d964a0401c29619aab01e1411050264354c65c4be61ff9ec95bbda33	qweqe	qweqwe	scrypt:32768:8:1$l0GjbR7vGyNVeB4c$44dc80ac2b8a3a23cd2ebf735f0d4e8ea5caea87539469107c9f3c66fe1085c5c9892540558038f5de31dc77a4938f93ce8637f46cf71e80133fbcd846dc3f90
8	qwerty		scrypt:32768:8:1$pmuJFnl61o7EPDsm$34de92902d01a362b88ba6aba69348e64f69a391da265f9226848be062cbb67ac95fad045ba61bd473ae356772521115adad535166b18b11af09fde5dddc85d8	qwerty	qwerty	scrypt:32768:8:1$vCXgUc7VMh9UKxp1$3084560fb0a22612584a2ec15ab579d6a93eeba72e026e4b6081a6bf8184e6922b6765832697d73866613239f421d3e912c5722ab54878596af04059a29cf7f7
9	asddad		scrypt:32768:8:1$C1NF84xwprI4TJ6z$25eaf2acb0b754a82f18233e0826ea3e1d914d28f9836f0720b4e3cc7538455a88452abfb68e47e5176d61652166259db553aac5a98446c639b8a6fc425bace3	adsasdad	asdasdd	scrypt:32768:8:1$5MX7GjY7QKKK4qcD$f07b7a3a834210bb9c2b6308b5095da448afae66819cfd507909cce7a6ab13b6a26bdb55f134e6db73201f28b1086dc3e1969ebc8aca70b72ee7efa72cab52e2
10	asddadwww		scrypt:32768:8:1$DrAGoT3JKmW0XTRg$279c03475f93d0b9e4f5db482868f13c943fb68e81dc53acfd0ac168e3544892783791db44d97dba3c37685bada31f00025b43894262c192c8a963b086963dcc	adsasdadww	asdasddqq	scrypt:32768:8:1$R7XJoFOrEK1kaFHX$3a29d5b33830e685d833aa830bda72f22c5672dc7bb2f5f51946cba8d631380e5fc394362f377ee6b41932384695f038a00e4a801de31bf1b6c9c42c511dd9fb
11	asddadwwwssa		scrypt:32768:8:1$CeCwjoiZM6StGckW$9eb7b6f6fcc50642dac3e4b771d241fc6b81540c231c65730393d69488d23e714c20da4c93fa19eccc3469d50004a124207d84d390886956271554ffbf1aa4ba	adsasdadwwsas	asdasddqqasa	scrypt:32768:8:1$IwjXQarRPe45SYBv$7e570fbad9a21679dc9de9e30a87d6d31ec66dc7ff1c29a37f300e000657a1792239f081ab2c05efdb1304b91153ba4052cb0c25558900eb351929c0d65dc038
12	qweqweqe		scrypt:32768:8:1$LY9GsHHpXMLotG5T$648ae72d59e9d9fd7ffa96022a0fa0815593686197afab8ad82c7de13c79771225f5c5a4beef9ba2b87698acf83ae87d947d48af30a17be7b176c23a43279323	qweqwe	qweqweqe	scrypt:32768:8:1$QBV4qx6Y3zeQOBUL$391919a23fa63b5cf4eca5edb3a6c6dad643b3e1ada8229d0939cb4fa3829d1e0a8a33b17c32f219d23f61672001a004d6def10809df153a05007f4027d7991e
13	qwerrt		scrypt:32768:8:1$iM38esZfyOEuVaDo$f891b414b30af4586072303672ec7400e23991b1b13b04e1ac7590a83b597c65de96619ed2cfb1cb9a386a90b1ab75ce50da7fae95928632a6f9f75d745bda13	qwrrfsdfas	sffdsdfds	scrypt:32768:8:1$4lTuPs1GchHcvEDb$b36561159080dc1e71435a1104e38c08461ccb235c3032614d9cd2af76dd00271cddfb6abc6e6d785dbe35c94f35e469e4d8fbad3ff05a80ab186192f6aa18d8
14	qwewerq		scrypt:32768:8:1$N1QNn2Y0ZqF1NFaE$c338b0a10955d8a374bf959499e99912b7f077e695b6189de4d2768216887e2509f595505b4500717404181146924df883f07fcdc136b238b227fc2dbbe4324d	qwerqwer	qwerqwr	scrypt:32768:8:1$3HZPu37IS1n26ymR$34daf5345306bc00443bb0fd453fd46e9bc80cb659a039267b5f00e6f2d9229a1807b265d48762531c0c59c25fd5654ab962a6d36809f37513f0b8b2b508931a
15	qwerrtqwt		scrypt:32768:8:1$4H1iAPXUPevvBcJe$7db9a2363701a9585430c64a7f792208e8a6ddae0bddeda0a08c4dd191f6fcb23f80ecb933a44396f8f8bf3b77095691ad149f0a52ff2cdc06063093a2035d82	wqerwreq	wqrqwrqw	scrypt:32768:8:1$FDGMu3SHAiaShLKF$bff62038a5f049c08beadcb73992a88d2aab6ba226da7641bf7141d62a1104ddb11bb4c9aa8b10d1630ffb42fa7f72660cbbf597831deefae9bda0f390e713b5
16	jqnkefwqk	ndfdf@yandex.ru	scrypt:32768:8:1$zeguWv7uUgrQBvtC$bd6b252fbbbc549f777b999126ecbdab517481e4902758d9ba0595512c7e8fedcd7b1bce5346a1c5bda6aaf4627d999bc49b9e14540b26941d64de6a40d67532	wfnwjfn	fwfdwfw	scrypt:32768:8:1$PzIysMxVzphSDAbs$3bdcda786e84716491e0c8efe159b66c28128d41fcc6adecc46ab1ec38a80f921ac8f1738b00694ec9de4a78fc24d5c16ff3317393353972bde7647740916b51
17	qwerqwerqwr	qwer@qwe.tu	scrypt:32768:8:1$2dOa4p4mkXt34BRo$9235895aab01acdc90a2eb33170462ad967ba9bd0ff5f73d5e12f564cdb7facb79a95eec9a3cc45a11ddc8512b2e7c9fede155c93d87c4541ef08b5a79e8c313	qwrwr	qwrqwre	scrypt:32768:8:1$ewbynbkiFsYIgtyo$22b462ddb3013f57731e9ecf8eb1eeb328ebbf2fb1e24bab5f3a04d75f140969eff892522e81b21eae06c668e39f6ab395dd4b5b00f00eed8f4aeb6589424c74
18	dqwkwer	qwerwqr@yandex.eer	scrypt:32768:8:1$xCL3eHadCzXUKIOV$a40e6c72d98dbcd4eb3a9b5765d1d2d4786b4d0891afe7b7b6f9ba476a5fe5f15e4302faf61bd083142f00a12be773e98752ef38085052bf31766e43236532a3	qwerqw	wqer	scrypt:32768:8:1$FafVvBP65yjNSzm4$42184e6abb7fb5a57ba9dc4bb953f0f7a118923037167b92a05224a36beae092010550922542612b8f54d52450f515c75068e6233a971e3b13e95a7e472dc8b9
19	qwertwqetqtw	qqrewq@yandex.ru	scrypt:32768:8:1$MZ2GrdLNQ7NmzZXz$0e55e44ff8c231ba41f1422866756eeb98e8692c292d7fd47f82d0ae2cf971dbac13d3dcbd0114299f42f5e4082bbc15d761d69c0abf5dcfa8e71e0f86bc03aa	qwertqwet	wer	scrypt:32768:8:1$mgEEbS9RqfiK9gm3$fd4ed69297159760c629b3f1eb8c534ce0c2d0ff6db979d6bd0866399cebc4321295bfbef58d8968b6cc76c442d93a9ac11b62cea4770d1e3ad8627afdcb47bd
20	safsdfas	fasdf@asd.ru	scrypt:32768:8:1$EDPSKJaPxKWWnrRc$a20d50e484cc8a88f6e99d838d6f57d91bb3e0278b3762317f73ed3b7fb4c6a08c465ac05e8bf428c9fc4dcc25b9c369b53b9378b6c80e7dee72e1e5496bcd07	asdfafa	afdadfaasd	scrypt:32768:8:1$HcwIkrf8FL9YI4T6$faa5a5ef027a50007b4a544a1fdf2b867865ce032afa9501f1111c3afa36d7cb56eefea8f5753d0500f1867e55c2614fb702f567c58f8b4bd60848066bc51788
21	sdf	wff@AD.RU	scrypt:32768:8:1$6xcRHlUAJPUH7FWG$f64baef16cedc523353b3e3a5e77d37e45d37dc32a31c464f293e2f9c1c114c2abd45aeca65a22b36d0429e0e3cbce6f16991cdff527f63b5b5c4d168d958a3d	afads	asfd	scrypt:32768:8:1$2LGsc74eWUPK7MsP$9934a743176c19f79e7d9a8667f6015ae162de4d91834553a2b18690f53d67b92e54989cfa5822b5cf70166df42518f0c882e32c62d5c1e5e0fe211ee895e50a
22	qwerqwrqwrqwrqr	qwewer@yandex.ru	scrypt:32768:8:1$tNjjpoRhCSptZQo2$dd342773d0782c62010ec79a05bbb678b4fed35a707e6d9ca32900ca2a73e23d2e335686c453d522934d2c5db3806be5c4c5de035036001e0f2959840b9cd228	qwrqrqrqwrwr	qqwerafsdc	scrypt:32768:8:1$UBGBD1oFJ7mckkjW$a20dbe4675edfb601ca55d65354d1a0a8312f6cb03c4a7df6fa6f5dfc0d3b1ebc16992e58601452c071d0757df17a61220aa9b0ffc5b3c087a0b1718525e0876
\.


--
-- TOC entry 3646 (class 0 OID 0)
-- Dependencies: 218
-- Name: location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.location_id_seq', 7, true);


--
-- TOC entry 3647 (class 0 OID 0)
-- Dependencies: 222
-- Name: owner_info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.owner_info_id_seq', 1, false);


--
-- TOC entry 3648 (class 0 OID 0)
-- Dependencies: 220
-- Name: review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.review_id_seq', 3, true);


--
-- TOC entry 3649 (class 0 OID 0)
-- Dependencies: 216
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 22, true);


--
-- TOC entry 3467 (class 2606 OID 16638)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3475 (class 2606 OID 16711)
-- Name: location location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_pkey PRIMARY KEY (id);


--
-- TOC entry 3479 (class 2606 OID 16795)
-- Name: owner_info owner_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.owner_info
    ADD CONSTRAINT owner_info_pkey PRIMARY KEY (id);


--
-- TOC entry 3477 (class 2606 OID 16725)
-- Name: review review_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_pkey PRIMARY KEY (id);


--
-- TOC entry 3469 (class 2606 OID 16762)
-- Name: user user_phone_hash_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_phone_hash_key UNIQUE (phone_hash);


--
-- TOC entry 3471 (class 2606 OID 16698)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3473 (class 2606 OID 16702)
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- TOC entry 3480 (class 2606 OID 16712)
-- Name: location location_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_created_by_fkey FOREIGN KEY (created_by) REFERENCES public."user"(id);


--
-- TOC entry 3483 (class 2606 OID 16801)
-- Name: owner_info owner_info_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.owner_info
    ADD CONSTRAINT owner_info_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.location(id) ON DELETE CASCADE;


--
-- TOC entry 3484 (class 2606 OID 16796)
-- Name: owner_info owner_info_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.owner_info
    ADD CONSTRAINT owner_info_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- TOC entry 3481 (class 2606 OID 16726)
-- Name: review review_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.location(id);


--
-- TOC entry 3482 (class 2606 OID 16731)
-- Name: review review_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


-- Completed on 2024-08-03 12:28:49 -04

--
-- PostgreSQL database dump complete
--

