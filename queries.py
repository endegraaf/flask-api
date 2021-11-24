SQL_GET_VACANCIES = "select distinct vacancy_id, title, url, body from \
vacancies where vacancy_id IN (select distinct(vacancy_id) from vacancies);"
SQL_ADD_VACANCIES_7ST = "INSERT INTO vacancies(vacancy_id, title, url, body) VALUES(%s, %s, %s, %s)"
SQL_ADD_VACANCIES_JC = "INSERT INTO vacancies(vacancy_id, title, url, body) VALUES(%s, %s, %s, %s)"
