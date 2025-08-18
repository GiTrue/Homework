CREATE TABLE Employee (
    id SERIAL PRIMARY KEY,                            -- Уникальный идентификатор сотрудника
    name VARCHAR(100) NOT NULL,                       -- Имя сотрудника
    department VARCHAR(100) NOT NULL,                 -- Отдел
    manager_id INT,                                   -- Ссылка на начальника (ID сотрудника)
    FOREIGN KEY (manager_id) REFERENCES Employee(id)  -- Самоссылка
);
