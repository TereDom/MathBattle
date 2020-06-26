from requests import get, delete, put, post

print(put('http://127.0.0.1:8080/api/users/dimasik', data={'decided': 1, 'reported': 0, 'points': 1}).json())
print(get('http://127.0.0.1:8080/api/users/dimasik').json())
print(post('http://127.0.0.1:8080/api/user', json={'nickname': 'Dimka', 'login': 'Dimka26',
                                                            'hashed_password': '2626', 'birthday': '26.09.04'}).json())
print(get('http://127.0.0.1:8080/api/task/2').json())
print(put('http://127.0.0.1:8080/api/task/2').json())
print(post('http://127.0.0.1:8080/api/tasks/dimasik', json={'name': 'Dimka', 'answer': 'Dimka26',
                                                          'content': '2626', 'points': '25', 'user_login': 'dimasik'}).json())
print(get("http://127.0.0.1:8080/api/tasks/'").json())

