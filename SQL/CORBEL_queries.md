# Interrogation de la BDD Employees

Rendu par Marianne CORBEL.

Note: only_full_group_by

## Requêtes d'interrogation simples

```
1.	SELECT emp_no, last_name, first_name, gender, birth_date
	FROM employees;
	--- ok ! ---

2.  SELECT emp_no, first_name, last_name, gender
	FROM employees
	WHERE first_name = "Troy";
	--- ok ! ---

3.  SELECT *
	FROM employees
	WHERE `gender` = "F";
	--- ok ! ---

4.  SELECT *
	FROM employees
	WHERE `gender` = "M" AND `birth_date` >= "1965-01-31";
	--- ok ! ---

5.  SELECT DISTINCT title
	FROM titles;
	--- ok ! ---

6.  SELECT COUNT(*) AS "nombreDep"
	FROM departments;
	--- ok ! ---

7.  SELECT emp_no, MAX(salary) AS "maxSalary"
	FROM salaries;
	--- ok ! ---

8.  SELECT emp_no, AVG(salary) AS salaireMoy
	FROM salaries
	WHERE emp_no = 287323;
	--- ok ! ---

9.  SELECT *
	FROM employees
	WHERE first_name LIKE "%ard";
	--- ok ! ---

10. SELECT COUNT(*) AS "count"
	FROM employees
	WHERE gender = "F" AND first_name = "Richard";
	--- ok ! ---

11. SELECT COUNT(DISTINCT title) AS "nombreTitre"
	FROM titles;
	--- ok ! ---

12. SELECT COUNT(*) AS "nombreDep"
	FROM dept_emp
	WHERE emp_no = 287323;
	--- meh... ---
	CORRECTION: count(dept_no) au lieu de count(*)
	Question: ↑↑↑

13. SELECT *
	FROM employees
	WHERE MONTH(hire_date) = 1 AND YEAR(hire_date) = 2000
	ORDER BY hire_date;
	--- ok ! ---
	Question: qu'est-ce qui est mieux entre dates limites manuelles et ça ?

14. SELECT SUM(salary) AS "sommeSalaireTotale"
	FROM salaries;
	--- ok ! ---
```

## Requêtes avec jointures

```
15. SELECT employees.emp_no, first_name, last_name, titles.title FROM employees
	INNER JOIN titles ON employees.emp_no = titles.emp_no
	WHERE first_name = "Danny" AND last_name = "Rando"
	AND "1990-01-12" BETWEEN titles.from_date AND titles.to_date;
	--- ok ! ---
	Note: Natural Join aurait fait la liaison seul entre une PK et une FK.

16. SELECT COUNT(*) as nb_emp
	FROM dept_emp
	LEFT JOIN departments ON departments.dept_no = dept_emp.dept_no
	WHERE departments.dept_name = "Sales"
	AND "2000-01-01" BETWEEN dept_emp.from_date AND dept_emp.to_date;
	--- ok ! ---
	Question: quelle table est prioritaire ?

17. SELECT employees.emp_no, first_name, last_name, SUM(salaries.salary) AS "sommeSalaire"
	FROM employees
	JOIN salaries ON salaries.emp_no = employees.emp_no
	WHERE employees.first_name = "Richard"
	GROUP BY employees.emp_no;
	--- ok ! ---
	Question: Group by doit avoir toutes les clés du select non aggrégatives?

18. SELECT employees.emp_no, first_name, last_name, SUM(salary) AS "sommeSalaire"
	FROM employees
	JOIN salaries ON salaries.emp_no = employees.emp_no
	WHERE first_name = "Richard"
	GROUP BY employees.emp_no;
	--- ok ! ---
	Correction: GROUP BY s.emp_no, first_name, last_name ;
```

## Requêtes avec agrégation

```
19. SELECT first_name, gender, COUNT(*) AS "nombre"
	FROM employees
	WHERE first_name IN ("Richard", "Leandro", "Lena")
	GROUP BY first_name, gender
	ORDER BY first_name DESC, gender;
20. SELECT last_name, COUNT(*) AS nombre
	FROM employees
	GROUP BY last_name
	HAVING COUNT(*) > 200
	ORDER BY COUNT(*), last_name ASC;
	--- ok ! ---
	Note: Parfois utiliser un alias dans l'order (ici nombre) peut lancer une erreur.
	Réutiliser count() ne devrait pas causer de problèmes de perf (mise en cache).

21. SELECT employees.emp_no, first_name, last_name, hire_date, SUM(salary) AS sommeSalaire
	FROM employees
	INNER JOIN salaries ON salaries.emp_no = employees.emp_no
	WHERE first_name = "Richard"
	GROUP BY s.emp_no , first_name, last_name, hire_date,
	HAVING SUM(salary) > 1000000;
	--- ok ! ---

22. SELECT employees.emp_no, employees.first_name, employees.last_name, title, salary
	FROM employees
	INNER JOIN salaries ON salaries.emp_no = employees.emp_no
	INNER JOIN titles ON titles.emp_no = employees.emp_no
	ORDER BY salary DESC LIMIT 1;
22+ SELECT m.emp_no, m.first_name, m.last_name, title
		FROM employees e
		JOIN dept_emp AS de ON de.emp_no = e.emp_no
		JOIN dept_manager AS dm ON dm.dept_no = de.dept_no
		JOIN employees AS m ON dm.emp_no = m.emp_no
		JOIN titles AS t ON t.emp_no = m.emp_no
		WHERE e.first_name = "Martine" AND e.last_name = "Hambrick"
		AND CURRENT_DATE BETWEEN dm.from_date AND dm.to_date
		ORDER BY t.from_date DESC LIMIT 1;
```

## Requêtes supplémentaires

```
23. SELECT titles.title, AVG(salary) AS salaireMoyen FROM salaries
		JOIN titles ON salaries.emp_no = titles.emp_no
		GROUP BY titles.title
		ORDER BY salaireMoyen;
24. SELECT d.dept_no, d.dept_name, COUNT(*) AS nbManagers FROM departments AS d
		JOIN dept_manager AS dm ON dm.dept_no = d.dept_no
		GROUP BY d.dept_no
		ORDER BY d.dept_name;
25. SELECT d.dept_no, d.dept_name, AVG(s.salary) AS salaireMoyen FROM departments AS d
		JOIN dept_emp AS de ON de.dept_no = d.dept_no
		JOIN salaries AS s ON s.emp_no = de.emp_no
		GROUP BY dept_no
		ORDER BY salaireMoyen DESC LIMIT 1;
26. SELECT e.* FROM employees AS e
		JOIN titles AS t ON t.emp_no = e.emp_no
		WHERE t.title = "Senior Staff"
		AND NOT EXISTS (
			SELECT * FROM employees AS e2
				JOIN titles AS t ON t.emp_no = e2.emp_no
				WHERE t.title = "Staff" AND e2.emp_no = e.emp_no
		);
27. SELECT e.emp_no, e.first_name, e.last_name, title, salary FROM salaries AS s
		JOIN employees AS e ON e.emp_no = s.emp_no
		JOIN titles AS t ON t.emp_no = s.emp_no
		WHERE e.hire_date BETWEEN s.from_date AND s.to_date;
28. SELECT e.emp_no, e.first_name, e.last_name FROM employees AS e
		WHERE
			(SELECT salary FROM salaries as s
				WHERE s.emp_no = e.emp_no
				ORDER BY s.to_date DESC LIMIT 1) <
			(SELECT salary FROM salaries as s
				WHERE s.emp_no = e.emp_no
				ORDER BY s.to_date DESC LIMIT 1 OFFSET 1);
```
