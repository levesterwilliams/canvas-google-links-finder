import requests
import json

def set_course_name(server_url: str, headers: str, course_id: str) -> str:
    """Sets the name of the course.

    Parameters:
    -----------
    course_id (str) : The id of the course.

    Returns:
    --------
    str : The name of the course.
    """
    course_url = f'{server_url}api/v1/courses/{course_id}'
    response = requests.get(course_url, headers=headers)
    course = None
    if response.status_code == 200:
        course = response.json()
        course = course.get('name', 'Unknown Course')
    else:
        print(f"Error receiving course name: {response.status_code},"
              f" {response.text}")
        return ""
    return course


