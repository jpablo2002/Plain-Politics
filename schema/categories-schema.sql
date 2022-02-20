create table categories
(
    id         int          not null,
    categories varchar(255) not null,
    constraint categories_BILLCOMMITIES_id_fk
        foreign key (id) references BILLCOMMITIES (id)
            on update cascade on delete cascade
);

create unique index categories_id_uindex
    on categories (id);

