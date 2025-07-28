import requests
import json
from canvas_base_finder import CanvasGoogleLinkFinderBase


class CanvasDiscussionFinder(CanvasGoogleLinkFinderBase):

    def get_content_items(self, course_id: str) -> tuple[
        list[tuple[int, str]], str]:
        """
        Returns a list of topics and author messages found in course's Canvas
            Discussion Topics.

        Parameters:
        ----------
        course_id (str): The id of course.

        Returns:
        -------
        tuple[list[tuple[str, str]], str]: A tuple that contains 1) a list
            featuring a tuple of topic id and topic and 2) a string containing
            topic messages from author.
        """
        url = f"{self.server_url}/api/v1/courses/{course_id}/discussion_topics?per_page=10"
        topics_list = []
        messages = []
        while url:
            response = requests.get(url, headers=self._headers)
            if response.status_code == 200:
                try:
                    topics = response.json()
                    for topic in topics:
                        if topic.get('published', False):
                            messages.append(topic.get('message'))
                            topics_list.append((topic['id'], topic['title']))
                    url = self.get_next_page_url(response.headers.get('Link'))
                except json.JSONDecodeError:
                    print("Invalid JSON in discussion topics response")
                    break
            else:
                print(
                    f"Error fetching discussion topics: {response.status_code}")
                break
        messages_from_topic_author = " ".join(messages)
        topic_list_and_messages = (topics_list, messages_from_topic_author)
        return topic_list_and_messages

    def get_item_detail(self, course_id: str, topic_id: str) -> str:
        full_topic_view_url = f"{self.server_url}/api/v1/courses/{course_id}/discussion_topics/{topic_id}/view"
        response = requests.get(full_topic_view_url, headers=self._headers)
        print(response.json())
        if response.status_code == 200:
            try:
                full_topic_view = response.json()
            except json.JSONDecodeError:
                print("Invalid JSON in discussion topics response")
                return ""
        elif response.status_code == 403:
            return ""
        else:
            print(
                f"Error fetching discussion topic {topic_id}: {response.status_code}")
            return ""
            # Combine all message text into one string for regex scan
        messages = []
        # Flatten the full topic to gather threaded replies
        for entry in full_topic_view.get('view', []):
            messages.append(entry.get('message', ""))
            for replies in entry.get('replies', []):
                messages.append(replies.get('message', ""))
            print(f'Topic {topic_id} contains the message: {messages}')
        return " ".join(messages)

    def auxiliary_function(self, authors_messages: str) -> list:
        """
        Returns a list of Google links found in messages from authors
            of Discussion topics.

        Parameters:
        ----------
        authors_messages (str): The messages from authors
            of Discussion topics..

        Returns:
        list: A list of Google links found in messages from authors
            of Discussion topics.
        """
        links = self.extract_google_links(authors_messages)
        return links
