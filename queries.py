SQL_GET_VACANCIES = "select vacancy_id, title, url, body from vacancies_7st;"
SQL_ADD_VACANCIES_7ST = "INSERT IGNORE INTO vacancies_7st(vacancy_id, title, url, body) VALUES(%s, %s, %s, %s)"
SQL_ADD_VACANCIES_ITS = "INSERT INTO vacancies_its(vacancy_id, title, url, body) VALUES(%s, %s, %s, %s)"
SQL_ADD_VACANCIES_JC = "INSERT INTO vacancies_jc(vacancy_id, title, url, body) VALUES(%s, %s, %s, %s)"



