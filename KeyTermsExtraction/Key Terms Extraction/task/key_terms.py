from collections import Counter

from lxml import etree
from nltk.tokenize import word_tokenize


page_content = etree.parse("news.xml").getroot()

for news in page_content.iter():
    if news.get('name') == 'head':
        print(f'{news.text}:')
    if news.get('name') == 'text':
        word_list = word_tokenize(news.text.lower())
        counted_dict = Counter(sorted(word_list, reverse=True))
        print(*[x[0] for x in counted_dict.most_common(5)])