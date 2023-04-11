--DROP DATABASE IF EXISTS visitorsbook;
--CREATE DATABASE if not exists visitorsbook;
DROP table if exists users;
create table if not exists users
(
    id serial PRIMARY KEY,
    name text,
    email text NOT NULL UNIQUE,
    password text NOT NULL,
    contact_num text,
    active boolean NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT current_timestamp,
    activated_at TIMESTAMP NULL

);
DROP table if exists tokens;
create table if not exists tokens
(
    id serial PRIMARY KEY,
    token text NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);




create table if not exists visitorbook
(
    id         serial PRIMARY KEY,
    message    text     NOT NULL,
    user_id    integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    private     boolean NOT NULL DEFAULT false,
    created_at  timestamp NOT NULL DEFAULT current_timestamp,
    updated_at timestamp
);


create table if not exists upvotes(
    id serial PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_id integer NOT NULL REFERENCES visitorbook(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp

)

create or replace view top_messages as
select t1.id, t1.message, count(t2.id) as upvotes
from visitorbook as t1
            left join upvotes t2 on t1.id = t2.message_id
where private = false
group by t1.id
order by upvotes desc
limit 5;













