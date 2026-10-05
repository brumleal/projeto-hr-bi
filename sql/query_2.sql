-- Query 2: Funcionários por Região (com localização)
-- Objetivo: analisar salários e distribuição geográfica (cidade, estado, país e região).
-- Filtro: WHERE r.REGION_NAME IS NOT NULL (mantém apenas funcionários com região identificada)

SELECT
    e.EMPLOYEE_ID,
    e.FIRST_NAME,
    e.LAST_NAME,
    e.SALARY,
    d.DEPARTMENT_NAME,
    l.CITY,
    l.STATE_PROVINCE,
    c.COUNTRY_NAME,
    r.REGION_NAME
FROM HR.EMPLOYEES e
LEFT JOIN HR.DEPARTMENTS d
    ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
LEFT JOIN HR.LOCATIONS l
    ON d.LOCATION_ID = l.LOCATION_ID
LEFT JOIN HR.COUNTRIES c
    ON l.COUNTRY_ID = c.COUNTRY_ID
LEFT JOIN HR.REGIONS r
    ON c.REGION_ID = r.REGION_ID
WHERE r.REGION_NAME IS NOT NULL
ORDER BY r.REGION_NAME, c.COUNTRY_NAME, e.SALARY DESC;
