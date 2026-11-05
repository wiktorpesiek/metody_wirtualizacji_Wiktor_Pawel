CREATE TABLE IF NOT EXISTS categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS listings (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(200)  NOT NULL,
    description TEXT          NOT NULL DEFAULT '',
    price       NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    city        VARCHAR(100),
    category_id INT REFERENCES categories(id),
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT now()
);

INSERT INTO categories (name) VALUES ('Elektronika'), ('Książki'), ('Rowery');

INSERT INTO listings (title, description, price, city, category_id) VALUES
    ('iPhone 12 128GB', 'Stan dobry, bateria 85%', 1500, 'Poznań', 1),
    ('Wiedźmin - Ostatnie życzenie', 'Wydanie z 2014', 25, 'Gniezno', 2),
    ('Rower górski Kross', 'Rama M, 21 biegów', 900, 'Poznań', 3);