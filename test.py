from requests import get, delete

# print(get('http://127.0.0.1:5000/api/get_task/1').json())
# print(get('http://127.0.0.1:5000/api/get_count_of_task').json())
delete('http://127.0.0.1:8080/api/delete_task/1')
