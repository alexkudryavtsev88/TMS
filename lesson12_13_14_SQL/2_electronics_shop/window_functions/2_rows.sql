-- Using ROWS BETWEEN ... AND ... syntax we can define HOW the AGGREGATE Function will be applied inside the WINDOW

-- QUERY 1: UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
SELECT product_name, group_name, price,
       SUM(price) OVER (
            PARTITION BY group_name
            ORDER BY price DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS group_sum_price
FROM products_with_groups_view
WHERE group_name = 'Laptop';

-- the ALL Prices related to the Group are summed up together,
-- and each Row of Group gets the same Result

-- NOTE: this is equivalent to the Query if we DOESN'T specify ORDER BY... and ROWS...
-- conditions at all inside the OVER clause, but except that here we got the DESC Ordering in "price" column

    product_name    | group_name |  price  | group_sum_price
--------------------+------------+---------+-------------------
 HP Elite           | Laptop     | 1200.00 |           3400.00     # 1200 + 800 + 700 + 700
 Dell Vostro        | Laptop     |  800.00 |           3400.00     # 1200 + 800 + 700 + 700
 Sony VAIO          | Laptop     |  700.00 |           3400.00     # 1200 + 800 + 700 + 700
 Lenovo Thinkpad    | Laptop     |  700.00 |           3400.00     # 1200 + 800 + 700 + 700


-- QUERY 2: UNBOUNDED PRECEDING AND CURRENT ROW
SELECT product_name, group_name, price,
       SUM(price) OVER (
            PARTITION BY group_name
            ORDER BY price DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS group_sum_price
FROM products_with_groups_view
WHERE group_name = 'Laptop';

-- the Price in EACH Row is summed up with the SUM of Prices in previous Row/Rows related to the current Group
-- (there is NO duplications of "group_sum_price" result for Rows with the SAME Price)

    product_name    | group_name |  price  | group_sum_price
--------------------+------------+---------+-------------------
 HP Elite           | Laptop     | 1200.00 |           1200.00     # 1200  (no preceding rows)
 Dell Vostro        | Laptop     |  800.00 |           2000.00     # 800 + 1200
 Sony VAIO          | Laptop     |  700.00 |           2700.00     # 700 + (800 + 1200)
 Lenovo Thinkpad    | Laptop     |  700.00 |           3400.00     # 700 + (700 + 800 + 1200)


-- QUERY 3: CURRENT ROW AND UNBOUNDED FOLLOWING
SELECT product_name, group_name, price,
       SUM(price) OVER (
            PARTITION BY group_name
            ORDER BY price DESC
            ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
       ) AS group_sum_price
FROM products_with_groups_view
WHERE group_name = 'Laptop';

-- The "group_sum_price" value is Cumulative SUM which calculation starts
-- from the LOWEST Price in the Group and goes "from down to up"

    product_name    | group_name |  price  | group_sum_price
--------------------+------------+---------+-------------------
 HP Elite           | Laptop     | 1200.00 |           3400.00     # 1200 + (800 + 700 + 700)
 Dell Vostro        | Laptop     |  800.00 |           2200.00     # 800 + (700 + 700)
 Sony VAIO          | Laptop     |  700.00 |           1400.00     # 700 + 700
 Lenovo Thinkpad    | Laptop     |  700.00 |            700.00     # 700  (no following rows)


-- QUERY 4: 1 PRECEDING AND CURRENT ROW
SELECT product_name, group_name, price,
       SUM(price) OVER (
            PARTITION BY group_name
            ORDER BY price DESC
            ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
       ) AS group_sum_price
FROM products_with_groups_view
WHERE group_name = 'Laptop';

-- For EACH Row the "group_sum_price" value is calculated as SUM of this Row's Price and previous Row's Price

    product_name    | group_name |  price  | group_sum_price
--------------------+------------+---------+-------------------
 HP Elite           | Laptop     | 1200.00 |           1200.00    # 1200  (no preceding rows)
 Dell Vostro        | Laptop     |  800.00 |           2000.00    # 1200 + 800
 Sony VAIO          | Laptop     |  700.00 |           1500.00    # 800 + 700
 Lenovo Thinkpad    | Laptop     |  700.00 |           1400.00    # 700 + 700


-- QUERY 5: CURRENT ROW AND 1 FOLLOWING
SELECT product_name, group_name, price,
       SUM(price) OVER (
            PARTITION BY group_name
            ORDER BY price DESC
            ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING
       ) AS group_sum_price
FROM products_with_groups_view
WHERE group_name = 'Laptop';


    product_name    | group_name |  price  | group_sum_price
--------------------+------------+---------+------------------
 HP Elite           | Laptop     | 1200.00 |           2000.00     # 800 + 1200
 Dell Vostro        | Laptop     |  800.00 |           1500.00     # 700 + 800
 Sony VAIO          | Laptop     |  700.00 |           1400.00     # 700 + 700
 Lenovo Thinkpad    | Laptop     |  700.00 |            700.00     # 700


-- QUERY 6: 1 PRECEDING AND UNBOUNDED FOLLOWING
SELECT product_name, group_name, price,
       SUM(price) OVER (
            PARTITION BY group_name
            ORDER BY price DESC
            ROWS BETWEEN 1 PRECEDING AND UNBOUNDED FOLLOWING
       ) AS group_sum_price
FROM products_with_groups_view;

    product_name    | group_name |  price  | group_sum_price
--------------------+------------+---------+-------------------
 HP Elite           | Laptop     | 1200.00 |           3400.00    # 700 + 700 + 800 + 1200
 Dell Vostro        | Laptop     |  800.00 |           3400.00    # 700 + 700 + 800 + 1200
 Sony VAIO          | Laptop     |  700.00 |           2200.00    # 700 + 700 + 800
 Lenovo Thinkpad    | Laptop     |  700.00 |           1400.00    # 700 + 700
 iPhone             | Smartphone |  900.00 |           2000.00
 Nexus              | Smartphone |  500.00 |           2000.00
 HTC One            | Smartphone |  400.00 |           1100.00
 Microsoft Lumia    | Smartphone |  200.00 |            600.00
 iPad               | Tablet     |  700.00 |           1050.00
 Samsung Galaxy Tab | Tablet     |  200.00 |           1050.00
 Kindle Fire        | Tablet     |  150.00 |            350.00


-- QUERY 7: UNBOUNDED PRECEDING AND 1 FOLLOWING
SELECT product_name, group_name, price,
       SUM(price) OVER (
            PARTITION BY group_name
            ORDER BY price DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 FOLLOWING
       ) AS group_sum_price
FROM products_with_groups_view;

``    product_name    | group_name |  price  | group_sum_price
--------------------+------------+---------+-------------------
 HP Elite           | Laptop     | 1200.00 |           2000.00     # 1200 + 800
 Dell Vostro        | Laptop     |  800.00 |           2700.00     # 1200 + 800 + 700
 Sony VAIO          | Laptop     |  700.00 |           3400.00     # 1200 + 800 + 700 + 700
 Lenovo Thinkpad    | Laptop     |  700.00 |           3400.00     # 1200 + 800 + 700 + 700
 iPhone             | Smartphone |  900.00 |           1400.00
 Nexus              | Smartphone |  500.00 |           1800.00
 HTC One            | Smartphone |  400.00 |           2000.00
 Microsoft Lumia    | Smartphone |  200.00 |           2000.00
 iPad               | Tablet     |  700.00 |            900.00
 Samsung Galaxy Tab | Tablet     |  200.00 |           1050.00
 Kindle Fire        | Tablet     |  150.00 |           1050.00

