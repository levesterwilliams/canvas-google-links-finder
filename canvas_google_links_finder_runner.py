from canvas_utils import get_token, headers, set_course_name
from discussions_google_links_finder import CanvasDiscussionFinder
from pathlib import Path
import sys
import csv


server_url = {'LPS_Production': 'https://canvas.upenn.edu/', 'LPS_Test':
    'https://upenn.test.instructure.com/'}

if __name__ == "__main__":
    token = get_token()
    server_type = "LPS_Test"
    if token is None:
        print("API credentials were not found.")
        # could place logic here to prompt user to manually input either 1) API
        # token or 2) path location to locally stored token
        sys.exit(1)
    api_headers = headers(token, server_type)
    course_id = "1854667"
    course_name = set_course_name(server_url[server_type], api_headers,
                                  course_id)
    print(f"Current course name is {course_name}.")
    discussions_finder = CanvasDiscussionFinder(server_url[server_type], api_headers)
    canvas_finders = {"Discussions": discussions_finder.find_google_links(
        course_id)}

    download_folder = Path.home() / 'Downloads'
    if not download_folder.exists():
        download_folder.mkdir()
    output_file_path = download_folder / 'google_links_finder.csv'
    with open(output_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Course Name", "Course URL", "Canvas Object",
                         "Google Link Found in Canvas"])

        course_url = f"{server_url['LPS_Test']}courses/{course_id}"
        for canvas_object in canvas_finders:
            for google_link in canvas_finders[canvas_object]:
                writer.writerow([course_name, course_url, canvas_object, google_link])

    print(f"Results written to: {output_file_path}")