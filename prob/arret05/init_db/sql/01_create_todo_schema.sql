/*==============================================================*/
/* db for todo list                                             */
/* created on:     2022-05-15                                   */
/*==============================================================*/


create schema todo;
--set search_path to tododb,public;
--alter database postgres set search_path to tododb,public;


/*==============================================================*/
/* table: todo_element                                          */
/*==============================================================*/
create table todo.element (
   id                 serial               not null primary key,
   init_time          timestamptz          not null default now(),
   last_update_time   timestamptz          not null default now(),
   done_time          timestamptz,
   task               text                 null,
   td_user            text                 null
);

create or replace function trigger_set_timestamp()
returns trigger as $$
begin
   new.last_update_time = now();
   return new;
end
$$
language plpgsql;


create trigger trigger_set_timestamp
after update on todo.element
for each row
execute procedure trigger_set_timestamp();


set timezone = 'America/Montreal';

create view todo.extern_element as 
   select 
   id, 
   init_time, 
   last_update_time, 
   done_time, 
   task, 
   td_user, 
   done_time is null as is_active 
   from todo.element;

-- create function todo.user_element 
--    ($1 text)
--    returns table todo.extern_element

create view todo.v_oldest_user_task as
select * from todo.extern_element
where (init_time, td_user) in
(select min(init_time), td_user
    from todo.extern_element
    where is_active
    group by td_user);

create or replace function todo.fn_oldest_user_task
      (fn_user text)
      returns table (
          id  integer,
          init_time          timestamptz,
          last_update_time   timestamptz,
          done_time          timestamptz,
          task               text,
          td_user            text)
    as $$
    select id, init_time, last_update_time, done_time, task, td_user from todo.v_oldest_user_task where td_user=fn_user
    $$
    language sql;

create or replace function todo.fn_user_active_elements
      (fn_user text)
      returns table (
          id  integer,
          init_time          timestamptz,
          last_update_time   timestamptz,
          done_time          timestamptz,
          task               text,
          td_user            text,
          is_active          boolean)
    as $$
    select * from todo.extern_element where td_user=fn_user and is_active
    $$
    language sql;

create or replace function todo.fn_id_task
      (id_task text)
      returns table (
          id  integer,
          init_time          timestamptz,
          last_update_time   timestamptz,
          done_time          timestamptz,
          task               text,
          td_user            text,
          is_active          boolean)
    as $$
select * from todo.extern_element where td_user=id_task
    $$
    language sql;

create or replace function todo.fn_user_all_elements
      (fn_user text)
      returns table (
          id  integer,
          init_time          timestamptz,
          last_update_time   timestamptz,
          done_time          timestamptz,
          task               text,
          td_user            text,
          is_active          boolean)
    as $$
    select * from todo.extern_element where td_user=fn_user
    $$
    language sql;
