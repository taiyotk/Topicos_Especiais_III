create table aluno(
    id SERIAL primary key,
    nome TEXT not null,
    idade INTEGER not null
);

INSERT INTO aluno (nome, idade) VALUES
('Ana', 20),
('Bruno', 22),
('Carla', 19),
('Daniel', 21),
('Eva', 23);

insert into aluno (nome, idade) values ('Fabio', 25);

select * from aluno;

select nome from aluno
where idade > 20;