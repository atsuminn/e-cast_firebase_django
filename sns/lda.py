#形態素解析インポート
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import *
from janome.charfilter import *
t = Tokenizer()
token_filters = [POSStopFilter(['記号','助詞','助動詞','接続詞','接頭詞']), LowerCaseFilter(), ExtractAttributeFilter('base_form')]
char_filters = [UnicodeNormalizeCharFilter(), 
                RegexReplaceCharFilter(u'♯', u''), 
                RegexReplaceCharFilter(u'「', u''), 
                RegexReplaceCharFilter(u'」', u''),
                RegexReplaceCharFilter(u'\(', u''),
                RegexReplaceCharFilter(u'\)', u''),
                RegexReplaceCharFilter(u'/', u'')]
a = Analyzer(char_filters, t, token_filters)

from gensim import corpora, models

dictionary = corpora.Dictionary.load('sns/datasets/dictionary.dic')
lda_model = models.LdaModel.load('sns/datasets/lda.model')

def getTopic(message):
    new_doc = [word for word in a.analyze(message)]
    new_vec = dictionary.doc2bow(new_doc)

    topics_in_doc = lda_model.get_document_topics(new_vec)
    top_topic = sorted(topics_in_doc, key=lambda topic:topic[1], reverse=True)
    
    topic_rel = top_topic[0][1]
    if topic_rel > 0.5:
        return  top_topic[0][0]
    else:
        return -1