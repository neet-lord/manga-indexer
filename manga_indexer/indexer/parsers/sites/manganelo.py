from scrapy.http import Request

from lxml import etree as ET

from manga_indexer.indexer.items import ChapterItem

from manga_indexer.indexer.parsers import (
    BaseMangaParser,
    BaseMangaPageParser,
    BaseMangaPager
)

class ManganeloMangaPageParser(BaseMangaPageParser):
    def _get_manga_on_page(self) -> list:
        return self._document.css(
            'html body div.body-site '
            'div.container.container-main '
            'div.panel-content-genres div.content-genres-item '
            'div.genres-item-info '
            'h3 a.genres-item-name.text-nowrap.a-h::attr(\'href\')'
        ).getall()

    def _get_page_url(self, page_number) -> str:
        return self._document.request.url

class ManganeloMangaParser(BaseMangaParser):
    def _get_title(self) -> str:
        title = self._document.css(
            'html body div.body-site '
            'div.container.container-main '
            'div.container-main-left '
            'div.panel-story-info div.story-info-right h1::text'
        ).get().strip()
        
        return title
    
    def _get_tags(self) -> str:
        tags = self._document.xpath(
            '/html/body/div[1]/div[3]'
            '/div[1]/div[3]/div[2]'
            '/table/tbody/tr/'
            'td[contains(text(),\'Genres\')]'
            '/../td[2]/a/text()'
        ).getall()

        return tags

    def _get_description(self) -> str:
        description =  ''.join(
                self._document.xpath(
                '//*[@id="panel-story-info-description"]/text()'
            ).getall()
        ).strip()

        return description

    def _get_alternate_names(self) -> str:
        try:
            alternate_names = self._document.css(
                'html body div.body-site '
                'div.container.container-main '
                'div.container-main-left '
                'div.panel-story-info '
                'div.story-info-right '
                'table.variations-tableInfo '
                'tbody tr td.table-value h2::text'
            ).get().split(';')

            return alternate_names
        except:
            return list()
        
    def _get_authors(self) -> str:
        authors = self._document.xpath(
            '/html/body/div[1]/div[3]'
            '/div[1]/div[3]/div[2]'
            '/table/tbody/tr/'
            'td[contains(text(),\'Author\')]'
            '/../td[2]/a/text()'
        ).getall()

        return authors
    def _get_status(self) -> str:
        status = self._document.xpath(
            '/html/body/div[1]/div[3]'
            '/div[1]/div[3]/div[2]'
            '/table/tbody/tr/'
            'td[contains(text(),\'Status\')]'
            '/../td[2]/text()'
        ).get().strip()

        return status

    def _get_url(self) -> str:
        return self._document.request.url

    def _get_chapters(self) -> list:
        chapters = list()

        chapters_nodes = self._document.xpath(
            '/html//div[contains(@class, \'panel-story-chapter-list\')]//'
            'a[contains(@class, \'chapter-name\')]'
        ).getall()

        chapters_nodes = chapters_nodes[::-1]

        n = len(chapters_nodes)

        for idx in range(n):
            node = ET.fromstring(chapters_nodes[idx])

            url = node.attrib['href']
            name = node.text

            chapter = ChapterItem(
                idx=idx,
                name=name,
                url=url
            )

            chapters.append(chapter)

        return chapters
class ManganeloMangaPager(BaseMangaPager):
    def _get_page_list(self):
        if self._page_list is None:

            total_number_of_pages = int(
                self._document.css(
                    ".page-last::attr('href')"
                ).get().split('/')[-1]
            )

            page_format = 'https://manganelo.com/genre-all/{page}'

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
        return int(
            self._document.css(
                'html body div.body-site '
                'div.container.container-main '
                'div.panel-page-number '
                'div.group-page a.page-select'
            ).get()
        )
        
