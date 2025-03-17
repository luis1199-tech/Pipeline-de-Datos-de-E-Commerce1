-- top_10_revenue_categories.sql
SELECT 
    p.product_category_name AS Category,
    COUNT(o.order_id) AS Num_order,
    SUM(i.price) AS Revenue
FROM olist_order_items i
JOIN olist_products p ON i.product_id = p.product_id
JOIN olist_orders o ON i.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY Revenue DESC
LIMIT 10;

-- TODO: Esta consulta devolverá una tabla con las 10 categorías con mayores ingresos
-- (en inglés), el número de pedidos y sus ingresos totales. La primera columna será
-- Category, que contendrá las 10 categorías con mayores ingresos; la segunda será
-- Num_order, con el total de pedidos de cada categoría; y la última será Revenue,
-- con el ingreso total de cada categoría.
-- PISTA: Todos los pedidos deben tener un estado 'delivered' y tanto la categoría
-- como la fecha real de entrega no deben ser nulas.
