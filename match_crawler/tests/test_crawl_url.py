import pytest
import crawler

TEST_SITE = 'https://folmez.github.io'
TEST_SITE_OUTPUT = '<html>\n<body>\n<br>\n' + \
                    '<a href="IstanbulAmatorFutbol/istanbul.html">' + \
                    'Istanbul Amator Hakem Bulten Analiz</a>\n' + \
                    '</body>\n</html>\n'

@pytest.mark.slow
def test_crawl_url_using_urllib():
    assert crawler.crawl_url(TEST_SITE) == TEST_SITE_OUTPUT

TEST_SITE_INNER_HTML = '\n<br>\n' + \
                        '<a href="IstanbulAmatorFutbol/istanbul.html">' + \
                        'Istanbul Amator Hakem Bulten Analiz</a>' + \
                        '\n\n\n'

@pytest.mark.slow
def test_crawl_url_using_selenium():
    assert crawler.crawl_url(TEST_SITE, use_selenium=True) == TEST_SITE_INNER_HTML
