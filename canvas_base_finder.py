import re
from bs4 import BeautifulSoup

# Regex pattern for Google links
GOOGLE_LINK_PATTERN = re.compile(
    r"https?://(?:docs\.google\.com|drive\.google\.com|forms\.google\.com|goo\.gl|google\.com)\S*",
    re.IGNORECASE
)


class CanvasGoogleLinkFinderBase:
    def __init__(self, base_url: str, headers: dict):
        self.server_url = base_url.rstrip('/')
        self._headers = headers

    def get_next_page_url(self, link_header: str) -> str:
        """Gets the next page URI for the discussion page.

        Parameters
        ----------
        link_header (str) : Header for the next URI for the discussion page.

        Returns
        -------
        str : URI for the next page.
        """
        if link_header:
            links = link_header.split(',')
            for link in links:
                if 'rel="next"' in link:
                    return link.split(';')[0].strip('<> ')
        return ""

    def extract_google_links(self, text: str) -> list[str]:
        if not text:
            return []

        soup = BeautifulSoup(text, "html.parser")
        found_links = set()

        # ---- A) Parse <a href=""> elements ----
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            visible_text = a.get_text().strip()

            href_is_google = bool(GOOGLE_LINK_PATTERN.match(href))
            text_is_google_url = bool(GOOGLE_LINK_PATTERN.match(visible_text))

            # If text == href (like <a href="url">url</a>) → keep only once
            if href_is_google and visible_text == href:
                found_links.add(href)
            else:
                # Add href if it's a google link
                if href_is_google:
                    found_links.add(href)
                # Add inline text separately only if it's a google URL and differs from href
                if text_is_google_url and visible_text != href:
                    found_links.add(visible_text)

        # ---- B) Capture raw Google URLs outside links ----
        raw_text = soup.get_text()
        for url in GOOGLE_LINK_PATTERN.findall(raw_text):
            found_links.add(url)

        return list(found_links)

    def find_google_links(self, course_id: str) -> list:
        """
        Template method to fetch items, get content, find Google links.

        Parameters
        ----------
        course_id (str): The id of the course.

        Returns
        -------
        list: A list of Google links.
        """
        all_links = []
        batch = self.get_content_items(course_id)
        for item_id, title in batch[0]:
            print(f"Current item: {item_id}")
            print(f"Title: {title}")
            content = self.get_item_detail(course_id, item_id)
            links = self.extract_google_links(content)
            if links:
                all_links.extend(links)
            print(links)
        if batch[1] is not None:
            links = self.auxiliary_function(batch[1])
            print(f'The author message contains: {links}')
            if links:
                all_links.extend(links)
        return all_links

    # Functions below must be implemented by subclasses
    def get_content_items(self, course_id: str):
        raise NotImplementedError

    def get_item_detail(self, course_id: str, item_id: str):
        raise NotImplementedError

    def auxiliary_function(self, *args):
        raise NotImplementedError
