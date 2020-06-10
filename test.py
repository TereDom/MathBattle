from requests import get

# print(get('http://127.0.0.1:5000/api/get_task/1').json())
print(get('http://127.0.0.1:5000/api/get_count_of_task').json())
