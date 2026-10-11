CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    age INTEGER
);

INSERT INTO customers (customer_id, name, city, age)
VALUES
    (1, 'Ada', 'Lagos', 24),
    (2, 'Tunde', 'Abuja', 31),
    (3, 'Chidi', 'Lagos', 27),
    (4, 'Amina', 'Kano', 22),
    (5, 'David', 'Ibadan', 29),
    (6, 'Zainab', 'Lagos', 35),
    (7, 'Femi', 'Abuja', 26),
    (8, 'Grace', 'Port Harcourt', 30);

-- View all customers
SELECT *
FROM customers;
-- Select specific columns
SELECT name, city
FROM customers;

-- Customers who live in Lagos
SELECT *
FROM customers
WHERE city = 'Lagos';

-- Customers who live in Lagos
SELECT *
FROM customers
WHERE city = 'Lagos';

-- Sort customers from oldest to youngest
SELECT *
FROM customers
ORDER BY age DESC;

-- Customers older than 25
SELECT *
FROM customers
WHERE age > 25;

-- Customers aged 30 or older
SELECT *
FROM customers
WHERE age >= 30;

-- Lagos customers older than 25
SELECT *
FROM customers
WHERE city = 'Lagos'
  AND age > 25;

-- Customers from Lagos or Abuja
SELECT *
FROM customers
WHERE city = 'Lagos'
   OR city = 'Abuja';

-- Customers who are not from Lagos
SELECT *
FROM customers
WHERE NOT city = 'Lagos';

-- Show each city only once
SELECT DISTINCT city
FROM customers;

-- Return only three customers
SELECT *
FROM customers
LIMIT 3;

-- Top two oldest Lagos customers aged 25+
SELECT name, age
FROM customers
WHERE city = 'Lagos'
  AND age >= 25
ORDER BY age DESC
LIMIT 2;

--Exercise
SELECT name, city, age
FROM customers
WHERE age > 25
ORDER BY age DESC
LIMIT 3;

-- customers from Lagos, Abuja and Kano
SELECT *
FROM customers
WHERE city IN ('Lagos', 'Abuja', 'Kano');

-- customers neither in Lagos or Abuja
SELECT *
FROM customers
WHERE city NOT IN ('Lagos', 'Abuja');

-- Customers aged between 25 and 30
SELECT *
FROM customers
WHERE age BETWEEN 25 AND 30;

-- cusstomer outside the 25 to 30 range
SELECT *
FROM customers
WHERE age NOT BETWEEN 25 AND 30;

-- Names starting with A
SELECT *
FROM customers
WHERE name LIKE 'A%'; --% means any number of character can appear next.

-- Names enidng with a
SELECT *
FROM customers
WHERE name LIKE '%a';

-- One underscore (_) means exactly one character. 

-- Add a  Customer with unknown age
INSERT INTO customers (customer_id, name, city, age)
VALUES (9, 'Musa', 'Kaduna', NULL);

-- Customers with missing age
SELECT *
FROM customers
WHERE age IS NULL;

-- Customers without missing age
SELECT *
FROM customers
WHERE age IS NOT NULL;

-- Customers from selected cities aged 25 to 35
SELECT *
FROM customers
WHERE city IN ('Lagos', 'Abuja', 'Kano')
  AND age BETWEEN 25 AND 35;

-- Count all customers
SELECT COUNT(*) AS total_customers -- AS is used to create an alias
FROM customers;

-- Count every row
SELECT COUNT(*) AS total_customers
FROM customers;

-- Count customers with a known age
SELECT COUNT(age) AS customers_with_age
FROM customers;

-- Average customer age
SELECT AVG(age) AS average_age
FROM customers;

-- Youngest customer age
SELECT MIN(age) AS youngest_age
FROM customers;

-- Oldest customer age
SELECT MAX(age) AS oldest_age
FROM customers;

-- combining the above two queries into one
SELECT
    MIN(age) AS youngest_age,
    MAX(age) AS oldest_age
FROM customers;

-- Using the SUM() function
SELECT SUM(age) AS total_age
FROM customers;

-- Count customers in each city
SELECT
    city,
    COUNT(*) AS total_customers
FROM customers
GROUP BY city;

-- Average customer age in each city
SELECT
    city,
    AVG(age) AS average_age
FROM customers
GROUP BY city;

-- Cities ranked by number of customers
SELECT
    city,
    COUNT(*) AS total_customers
FROM customers
GROUP BY city
ORDER BY total_customers DESC;

-- Cities with at least two customers
SELECT
    city,
    COUNT(*) AS total_customers
FROM customers
GROUP BY city
HAVING COUNT(*) >= 2;

--EXERCISES
-- count total number of customers and call the column total_customers 
SELECT COUNT(*) AS customer_count
FROM customers;
-- Average age of customers and call the column average_age
SELECT AVG(age) AS average_age
FROM customers;
-- return the youngest and oldest ages in one query and call the columns youngest_age and oldest_age
SELECT MIN(age) AS youngest_age, MAX(age) AS oldest_age
FROM customers;
-- show each city and the number of customers in that city  
SELECT city, 
  COUNT(*) AS total_customers
FROM customers
GROUP BY city;
-- show each city and the average age of customers in that city sorted from highest average age to lowest 
SELECT city, 
  AVG(age) AS average_age
FROM customers
GROUP BY city
ORDER BY average_age DESC;
-- show cities having 2 or more customers, sorted from highest to lowest number of customers
SELECT city, 
  COUNT(*) AS total_customers
FROM customers
GROUP BY city
HAVING COUNT(*) >= 2
ORDER BY total_customers DESC;

-- Create orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Insert sample orders
INSERT INTO orders (order_id, customer_id, amount, order_date)
VALUES
    (101, 1, 25000, '2026-09-01'),
    (102, 1, 12000, '2026-09-03'),
    (103, 2, 40000, '2026-09-04'),
    (104, 3, 18500, '2026-09-05'),
    (105, 5, 32000, '2026-09-07'),
    (106, 6, 15000, '2026-09-08'),
    (107, 6, 22000, '2026-09-10'),
    (108, 2, 10000, '2026-09-12');

-- Show orders with customer names
SELECT
    customers.name,
    orders.order_id,
    orders.amount,
    orders.order_date
FROM customers
INNER JOIN orders
    ON customers.customer_id = orders.customer_id;

-- Show all customers and any orders they have
SELECT
    c.name,
    o.order_id,
    o.amount
FROM customers AS c -- the left table
LEFT JOIN orders AS o -- the right table
    ON c.customer_id = o.customer_id;

-- Total amount spent by each customer who has placed an order
SELECT
    c.name,
    SUM(o.amount) AS total_spent
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;

-- show customer name, order id and amount using INNER JOIN
SELECT
    c.name,
    o.order_id,
    o.amount
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id;

-- show customer name, order id and city using LEFT JOIN
SELECT
    c.name,
    o.order_id,
    c.city
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id;

-- show customer name and total amount spent using INNER JOIN
SELECT
    c.name,
    SUM(o.amount) AS total_spent
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;

--show customers who have never placed an order
SELECT
    c.name
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL; 

-- Count the number of orders placed by each customer
SELECT
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY order_count DESC;

-- Total spending for all customers
SELECT
    c.name,
    SUM(o.amount) AS total_spent
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;

-- Total spending for every customer, including zero spenders
SELECT
    c.name,
    COALESCE(SUM(o.amount), 0) AS total_spent
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;

-- Customer order summary
SELECT
    c.name,
    c.city,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.amount), 0) AS total_spent
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name,
    c.city
ORDER BY total_spent DESC;

-- Average order value for each customer
SELECT
    c.name,
    COUNT(o.order_id) AS order_count,
    COALESCE(AVG(o.amount), 0) AS average_order_value
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY average_order_value DESC;

-- Customers who have placed at least two orders
SELECT
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) >= 2
ORDER BY order_count DESC;

--Exercises
-- show customer name, number of orders including customers with zero orders
SELECT
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id  
GROUP BY c.customer_id, c.name;

-- show customer name, total amount spent including customers with zero orders showing as zero
SELECT
    c.name,
    COALESCE(SUM(o.amount), 0) AS total_spent 
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- show customer name, city, number of orders and total amount spent for ALL customers, sorted from highest total spending to the lowest
SELECT
    c.name,
    c.city,
    COUNT(o.order_id) AS order_count,
    COALESCE(SUM(o.amount), 0) AS total_spent
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spent DESC;

-- show customer name, order count. customer who have placed 2 or more order
SELECT
    c.name,
    COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) >= 2;

-- find the number of unique customers who have placed an order 
SELECT
    COUNT(DISTINCT c.customer_id) AS customers_with_orders
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id;

-- return the name and total spent of customer whose total spending is greater than 30,000
SELECT
    c.name,
    COALESCE(SUM(o.amount), 0) AS total_spent
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING SUM(o.amount) > 30000
ORDER BY total_spent DESC;

-- SUBQUERIES AND CTEs 
--Subqueries are queries nested inside another query. They can be used in SELECT, FROM, and WHERE clauses.
SELECT customer_id
FROM orders
WHERE amount > 30000;

-- Customers who have placed an order above 30,000
SELECT
    name
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    WHERE amount > 30000
);

-- Orders above the average order amount
SELECT
    order_id,
    customer_id,
    amount
FROM orders -- orders with amount greater than the average order amount
WHERE amount > (
    SELECT AVG(amount)-- average order amount
    FROM orders
);

--CTEs (Common Table Expressions) are temporary result sets that can be referenced within a SELECT, INSERT, UPDATE, or DELETE statement. They are defined using the WITH clause.
-- Create a temporary customer spending result
WITH customer_spending AS (
    SELECT
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_spent
    FROM customers AS c
    INNER JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)

SELECT *
FROM customer_spending;

-- Customers whose total spending exceeds 30,000
WITH customer_spending AS (
    SELECT
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_spent
    FROM customers AS c
    INNER JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)

SELECT
    name,
    total_spent
FROM customer_spending
WHERE total_spent > 30000
ORDER BY total_spent DESC;

-- Exercises 
-- SUbquery: find all orders whose amount is greater than the average order amount: return order_id and amount
SELECT
    order_id,
    amount
FROM orders
WHERE amount > (
    SELECT AVG(amount)
    FROM orders
);
--SUbquery: names of cusoomers who have placed an order greater than 20000
SELECT
    name
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    WHERE amount > 20000
);

--CTE: calculates customers name and total amount spent
WITH customer_totals AS(
  SELECT
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_amount_spent
    FROM customers AS c
    INNER JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)

SELECT *
FROM customer_totals;

--CTE: customers whose total spending is at least 35,000(name and total_spent) an sort DESC
WITH customer_total AS(
  SELECT
          c.name,
        SUM(o.amount) AS total_spent
    FROM customers AS c
    INNER JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)

SELECT * 
FROM customer_total
WHERE total_spent >= 35000;

--CTE: contains customer name, orer count and total spent for EVERY customer
WITH order_summary AS(
  SELECT
        c.customer_id,
        c.name,
        COUNT(o.order_id) AS order_count,
        COALESCE(SUM(o.amount), 0) AS total_spent
    FROM customers AS c
    LEFT JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)

SELECT *
FROM order_summary
WHERE order_count >= 2
ORDER BY total_spent DESC;

-- FInal exercise: 
-- which customers have spent the most money? return the name and total spent
WITH customer_spending AS (
    SELECT
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_spent
    FROM customers AS c
    INNER JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)

SELECT
    name,
    total_spent
FROM customer_spending
WHERE total_spent = (
    SELECT MAX(total_spent)
    FROM customer_spending
);

--calculate the total revenue generated by customers from each city. return only cities whose combined revenue is greater than 30000
WITH city_revenue AS (
    SELECT
        c.city,
        SUM(o.amount) AS total_revenue
    FROM customers AS c
    INNER JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.city
)
SELECT
    city,
    total_revenue   
FROM city_revenue
WHERE total_revenue > 30000;

-- Find every customer who have never made a purchase. Return the name and city of these customers.
SELECT
    c.name,
    c.city
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL; 

-- find customers whose total spending is greater than the average total spending amon customers who have placed orders. Return the name and total spent of these customers.
WITH customer_spending AS (
    SELECT
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_spent
    FROM customers AS c
    INNER JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)

SELECT
    name,
    total_spent
FROM customer_spending
WHERE total_spent > (
    SELECT AVG(total_spent)
    FROM customer_spending
);