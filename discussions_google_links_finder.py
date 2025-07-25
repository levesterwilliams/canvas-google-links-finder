import requests
import json
from canvas_base_finder import CanvasGoogleLinkFinderBase


class CanvasDiscussionFinder(CanvasGoogleLinkFinderBase):

    def get_content_items(self, course_id: str) -> list[tuple]:
        """
        Returns a list of topics found in course.

        Parameters:
        ----------
        course_id (str): The id of course.

        Returns:
        -------
        list[tuple[str, str]]: A list featuring a tuple of topic id and topic
            name.
        """
        url = f"{self.server_url}/api/v1/courses/{course_id}/discussion_topics?per_page=10"
        topics_list = []
        while url:
            response = requests.get(url, headers=self._headers)
            if response.status_code == 200:
                try:
                    topics = response.json()
                    for topic in topics:
                        if topic.get('published', False):
                            topics_list.append((topic['id'], topic['title']))
                    url = self.get_next_page_url(response.headers.get('Link'))
                except json.JSONDecodeError:
                    print("Invalid JSON in discussion topics response")
                    break
            else:
                print(f"Error fetching discussion topics: {response.status_code}")
                break
        return topics_list

    def get_item_detail(self, course_id: str, topic_id: str) -> str:
        url = f"{self.server_url}/api/v1/courses/{course_id}/discussion_topics/{topic_id}/view"
        response = requests.get(url, headers=self._headers)
        # Need function to get full topic view!!!
        print(response.json())
        if response.status_code == 200:
            topic_view = response.json()
            # Combine all message text into one string for regex scan
            messages = []
            for entry in topic_view.get('view', []):
                messages.append(entry.get('message', ""))
            return " ".join(messages)
        elif response.status_code == 403:
            return ""
        else:
            print(f"Error fetching discussion topic {topic_id}: {response.status_code}")
            return ""
