-- SELECT ALL PRODUCTS AND PRODUCT GROUPS DATA
SELECT a.product_name, b.group_name, a.price
FROM products a JOIN product_groups b
ON a.group_id = b.id;

-- CREATE VIEW TO AVOID WRITING OF 'JOIN' IN EACH QUERY
CREATE VIEW products_with_groups_view AS (
    SELECT a.product_name, b.group_name, a.price
    FROM products a JOIN product_groups b
    ON a.group_id = b.id
);

-- WINDOW FUNCTIONS explanations:
-- 1. AGGREGATE Function itself collapses the Rows in the Query Result set
-- to the Single row with Single value:
-- 2. When we use GROUP BY clause, the Result set is broken to the pieces (Groups)
-- and Rows are collapsed the borders of the each Group
-- 3. When we use WINDOW FUNCTIONS together with AGGREGATE functions: the Query Result set
-- (Rows) is not collapsed and stays as is, but we get the separate column
-- with value of the AGGREGATE Function which is repeated for the each Row in Result set
-- 4. We can configure (in Query) on which Rows the WINDOW FUNCTION will be applied and how.

-- 1. OVER CONDITION

-- QUERY 1: SELECT AVG PRICE FOR EACH PRODUCT
SELECT product_name, group_name, price, AVG(price) OVER () AS avg_product_price
FROM products_with_groups_view;

-- 2. PARTITION BY CONDITION

-- QUERY 2: SELECT AVG PRICE FOR EACH PRODUCT GROUP
SELECT product_name,
       group_name,
       price,
       AVG(price) OVER (
            PARTITION BY group_name
       ) AS avg_group_price
FROM products_with_groups_view;

-- QUERY 3: SELECT COMMON SUM PRICE FOR EACH PRODUCT GROUP
SELECT product_name,
       group_name,
       price,
       SUM(price) OVER (
            PARTITION BY group_name
       ) AS common_group_price
FROM products_with_groups_view;

-- Result:
    product_name    | group_name |  price  | common_group_price
--------------------+------------+---------+--------------------
 HP Elite           | Laptop     | 1200.00 |            3400.00     # 1200 + 800 + 700 + 700
 Lenovo Thinkpad    | Laptop     |  700.00 |            3400.00     # 1200 + 800 + 700 + 700
 Sony VAIO          | Laptop     |  700.00 |            3400.00     # 1200 + 800 + 700 + 700
 Dell Vostro        | Laptop     |  800.00 |            3400.00     # 1200 + 800 + 700 + 700
 Microsoft Lumia    | Smartphone |  200.00 |            2000.00
 HTC One            | Smartphone |  400.00 |            2000.00
 Nexus              | Smartphone |  500.00 |            2000.00
 iPhone             | Smartphone |  900.00 |            2000.00
 iPad               | Tablet     |  700.00 |            1050.00
 Kindle Fire        | Tablet     |  150.00 |            1050.00
 Samsung Galaxy Tab | Tablet     |  200.00 |            1050.00

-- 3. ORDER BY INSIDE WINDOW

-- QUERY 4: SELECT CUMULATIVE SUM PRICE FOR EACH PRODUCT GROUP
SELECT product_name, group_name, price,
       SUM(price) OVER (
            PARTITION BY group_name
            ORDER BY price DESC
       ) AS cumul_group_price
FROM products_with_groups_view;

-- The Price in Each Row is summed up with the SUM of Prices in all previous Rows related to the current Group,
-- BUT, if several Rows have the SAME Price value:
-- - these Prices are summed up together
-- - the Result is added to the SUM of Prices in the previous rows
-- - EACH row with the SAME Price value gets the SAME "cumul_group_price" Value

-- Result: pay attention to the "cumul_group_price" column for 'Sony VAIO' and 'Lenovo Thinkpad' products
    product_name    | group_name |  price  | cumul_group_price
--------------------+------------+---------+-------------------
 HP Elite           | Laptop     | 1200.00 |           1200.00     # 1200
 Dell Vostro        | Laptop     |  800.00 |           2000.00     # 800 + 1200
 Sony VAIO          | Laptop     |  700.00 |           3400.00     # 700 + 700 + 800 + 1200
 Lenovo Thinkpad    | Laptop     |  700.00 |           3400.00     # 700 + 700 + 800 + 1200
 iPhone             | Smartphone |  900.00 |            900.00
 Nexus              | Smartphone |  500.00 |           1400.00
 HTC One            | Smartphone |  400.00 |           1800.00
 Microsoft Lumia    | Smartphone |  200.00 |           2000.00
 iPad               | Tablet     |  700.00 |            700.00
 Samsung Galaxy Tab | Tablet     |  200.00 |            900.00
 Kindle Fire        | Tablet     |  150.00 |           1050.00