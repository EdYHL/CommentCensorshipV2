import hanlp
from flask import Flask, request

from HttpResponseTemplate.Response import Response
from parser import parser
from utils.load import load_from_db
from utils.logic import preprocessing, find_censored_words

app = Flask(__name__)
# print(logic.preprocessing("这是一条cnmb.jp信息", HanLP, '！@#￥%…（）&*', 'tok/coarse'))
# print(sts([('www.baidu.com', 'www..com'), ('www.baidu.com', 'www.baidu.baike.com')]))

# print(logic.filter_website('https://www.baidu.com'))

# print(HanLP('google.com'))
#


@app.route('/censor', methods=['POST'])
def censor():
    result = Response()
    try:
        params: dict = request.get_json()
        types = parser.parse_request_types(params['types'])
        comment = params['comment']
        tokens, contains_website = preprocessing(comment, HanLP, 'tok/coarse', whitelist)
        # data = parallel_censor(tokens, blacklist, types, sts_list)
        data = find_censored_words(tokens, blacklist, sts)
        result.success(data, contains_website, comment)
        return result.to_dict()
    except Exception as e:
        result.error(str(e))
        return result.to_dict()


#
#
if __name__ == '__main__':
    # blacklist = parallel_load()
    blacklist = load_from_db('blacklist', 'censors')
    whitelist = load_from_db('whitelist', 'censor_new')
    # sts_list = []
    # for i in range(7):
    #     sts_list.append(hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH))
    sts = hanlp.load(hanlp.pretrained.sts.STS_ELECTRA_BASE_ZH)
    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 分词
    # regrex = ('*#\\/+=-_<>——-·`。，、＇：∶；?‘’“”〝〞ˆˇ﹕︰﹔﹖﹑•¨….¸;！´？！～—ˉ｜‖＂〃｀@﹫¡¿﹏﹋﹌︴々﹟#﹩$﹠&﹪%*﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎+=<＿_'
              # '-ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼❝❞')
    # print(HanLP('这是一段测试语句，包含了违禁信息。www.baidu.com'))
    app.run(host='127.0.0.1', port=5000, debug=True)
    # print(blacklist)
    # result = parallel_censor(['a', 'b', 'cd', 'ef'], {'alpha': ['a'], 'beta': 'b'}, sts, ['alpha', 'beta'])
    # print(result)
