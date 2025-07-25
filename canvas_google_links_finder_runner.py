from canvas_utils import get_token, headers, set_course_name
from discussions_google_links_finder import CanvasDiscussionFinder
import sys

server_url = {'LPS_Production': 'https://canvas.upenn.edu/', 'LPS_Test':
    'https://upenn.test.instructure.com/'}

if __name__ == "__main__":
    token = get_token()
    if token is None:
        print("API credentials were not found.")
        # could place logic to prompt user to manually input API token or
        # path location to locally stored token
        sys.exit(1)
    api_headers = headers(token, "LPS_Test")
    course_id = "1854667"
    course_name = set_course_name(server_url['LPS_Test'], api_headers,
                                  course_id)
    print(f"Current course name is {course_name}.")
    finder = CanvasDiscussionFinder(server_url['LPS_Test'], api_headers)
    google_links = finder.find_google_links(course_id)

    for link in google_links:
        print(f"Discussions, {link}")