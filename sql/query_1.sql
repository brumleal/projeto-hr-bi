-- Query 1: Salário por Departamento e Cargo
-- Objetivo: analisar a distribuição de salários por departamento e cargo.
-- Filtro: WHERE e.DEPARTMENT_ID IS NOT NULL (remove funcionários sem departamento)

SELECT
    e.EMPLOYEE_ID,
    e.FIRST_NAME,
    e.LAST_NAME,
    d.DEPARTMENT_NAME,
    j.JOB_TITLE,
    e.SALARY,
    j.MIN_SALARY,
    j.MAX_SALARY
FROM HR.EMPLOYEES e
LEFT JOIN HR.DEPARTMENTS d
    ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
LEFT JOIN HR.JOBS j
    ON e.JOB_ID = j.JOB_ID
WHERE e.DEPARTMENT_ID IS NOT NULL
ORDER BY d.DEPARTMENT_NAME, e.SALARY DESC;
