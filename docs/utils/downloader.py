import requests
import time
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

class Downloader:
    def __init__(self, max_retries=30, delay=1):
        self.max_retries = max_retries
        self.delay = delay

    def download_file(self, url):
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename

    def download_page(self, url):
        retries = 0
        while retries < self.max_retries:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
                }

                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return response
                elif response.status_code in [403, 404, 429, 500]:
                    retries += 1
                    time.sleep(self.delay)
                else:
                    return None
            except requests.exceptions.RequestException:
                retries += 1
                time.sleep(self.delay)
        return None
    
    def download_page_html(self, url):
        loader = AsyncChromiumLoader([url])
        html = loader.load()
        print(html)
        return html
    
    def download_page_html_section(self, url, section_name = "article"):
        html = self.download_page_html(url)
        if html is not None:
            bs_transformer = BeautifulSoupTransformer()
            docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=[section_name])
    
            return docs_transformed
        return None