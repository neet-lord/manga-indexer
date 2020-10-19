from scrapy.http import Request

from manga_indexer.indexer.parsers import (
    BaseMangaParser,
    BaseMangaPageParser,
    BaseMangaPager
)

class MangadexMangaPageParser(BaseMangaPageParser):
    def _get_manga_on_page(self) -> list:
        mangas = self._document.css(".manga-entry .manga_title::attr('href')").getall()
        formatted_urls = list()
        
        for manga in mangas:
            formatted_urls.append(
                'https://mangadex.org{manga}'.format(
                    manga=manga
                )
            )

        return formatted_urls
    
    def _get_page_url(self, page_number) -> str:
        return self._document.request.url

class MangadexMangaParser(BaseMangaParser):
    def _get_title(self) -> str:
        title = self._document.css('#content.container div.card.mb-3 h6.card-header.d-flex.align-items-center.py-2 span.mx-1::text').get()
        return title
    
    def _get_url(self) -> str:
        return self._document.request.url

class MangadexMangaPager(BaseMangaPager):
    def _get_page_list(self):
        if self._page_list is None:

            element = self._document.css("#content.container nav ul.pagination.justify-content-center li.page-item:last-child > a:nth-child(1)")
            href = element.attrib['href']

            total_number_of_pages = int(href.split('/')[3])
            page_format = 'https://mangadex.org/titles/0/{page}'

            page_list = list()

            for x in range(total_number_of_pages):
                page_list.append(
                        page_format.format(
                        page=x+1
                    )
                )

            self.__page_list = page_list

        return self.__page_list

    def _get_current_page_number(self):
        return int(self._document.css('#content.container nav ul.pagination.justify-content-center li.page-item.active').get())
        
