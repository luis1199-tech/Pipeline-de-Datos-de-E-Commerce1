SELECT 
    c.customer_state,
    SUM(payments.total_payment) AS Revenue
FROM olist_customers c
JOIN olist_orders o ON c.customer_id = o.customer_id
JOIN (
    SELECT order_id, SUM(payment_value) AS total_payment
    FROM olist_order_payments
    GROUP BY order_id
) payments ON o.order_id = payments.order_id
GROUP BY c.customer_state
ORDER BY Revenue DESC
LIMIT 10;


-- TODO: Esta consulta devolverá una tabla con dos columnas; customer_state y Revenue.
-- La primera contendrá las abreviaturas que identifican a los 10 estados con mayores ingresos,
-- y la segunda mostrará el ingreso total de cada uno.
-- PISTA: Todos los pedidos deben tener un estado "delivered" y la fecha real de entrega no debe ser nula.
