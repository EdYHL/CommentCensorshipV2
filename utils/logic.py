from parser import parser
import psutil
import multiprocessing


def compare(source: str, target: str):
    count = 0
    index = 0
    for c in source:
        if c in target[index:]:
            index = index + target[index:].find(c) + 1
            count = count + 1
        elif c not in target[index:] and source.find(c) == 0:
            break
    return count / len(target)


def contains(source: str, target: str) -> float:
    if len(source) == 0 or len(target) == 0:
        return 0.0
    elif source == target:
        return 1.0
    else:
        result = compare(source, target)
        reversed_result = compare(source[::-1], target)
        if result >= reversed_result:
            return result
        else:
            return reversed_result


def preprocessing(source: str, HanLP, form: str, whitelist: set) -> (list, bool):
    parsed_1 = HanLP(source)
    tokens_coarse: list = parsed_1[form]
    tokens_ctb: list = parsed_1['pos/ctb']
    # tokens_ner: list = parsed_1['ner/msra']
    contains_website = False
    for i in range(len(tokens_ctb)):
        if tokens_ctb[i] == 'PU':
            tokens_coarse[i] = ''
        elif tokens_ctb[i] == 'URL':
            tokens_coarse[i] = ''
            contains_website = True
    # for value in tokens_ner:
    #     if value[1] == 'WWW':
    #         contains_website = True
    #         tokens_coarse.remove(value[0])
    # tokens_new = []
    # new_source = new_source.join(tokens_coarse)
    # new_parsed = HanLP(filter_char(new_source, regrex))
    # for token in tokens_coarse:
    #     tokens_new.append(filter_char(token, regrex))
    # processed_list = [filter_char(token, regrex) for token in tokens_coarse if token not in whitelist and token != '']
    # return processed_list, contains_website
    new_str = ''
    new_str = new_str.join(tokens_coarse)
    new_list = HanLP(new_str)[form]
    processed_list = [token for token in new_list if token not in whitelist and token != '']
    return processed_list, contains_website


def filter_char(source: str, regrex: str):
    result = ''
    for c in regrex:
        result = source.replace(c, '')
    return result

# def find_censored_websites(websites: list, banned_websites: list):
#     for website in websites:
#         for banned_website in banned_websites:
#             if website == banned_website:
#                 return True
#     return False


def find_censored_words(tokens: set, blacklist: set, sts):
    guaranteed = {}
    high_risk = {}
    low_risk = {}
    for token in tokens:
        guaranteed_token = {}
        high_risk_token = {}
        low_risk_token = {}
        for word in blacklist:
            relativity = contains(token, word)
            if relativity == 1.0 and token == word:
                guaranteed_token[word] = 1.0
            elif 0.5 < relativity <= 1.0:
                similarity = sts((token, word))
                if 0.6 <= similarity < 0.8:
                    low_risk_token[word] = similarity
                elif 0.8 <= similarity < 0.95:
                    high_risk_token[word] = similarity
                elif 0.95 <= similarity:
                    guaranteed_token[word] = similarity
        if len(guaranteed_token) > 0:
            guaranteed[token] = guaranteed_token
        if len(high_risk_token) > 0:
            high_risk[token] = high_risk_token
        if len(low_risk_token) > 0:
            low_risk[token] = low_risk_token
    return parser.parse_result(guaranteed, high_risk, low_risk)


# Temp
def add_censors(original: str, censored_words: str):
    for char in censored_words:
        original.replace(char, '*')
    return original
