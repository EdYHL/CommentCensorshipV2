from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from utils.logic import find_censored_words
from utils.load import load_from_db


def parallel_censor(tokens: set, blacklist: dict, data_types: list, sts_list: list):
    result = {}
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = []
        i = 1
        for data_type in data_types:
            futures.append([data_type, executor.submit(find_censored_words, tokens, blacklist[data_type], sts_list[i - 1])])
            i = i + 1
        for future in futures:
            result[future[0]] = future[1].result()
        # future1 = executor.submit(find_censored_words, tokens, blacklist[data_types[0]], sts_list[0], 1)
        # future2 = executor.submit(find_censored_words, tokens, blacklist[data_types[1]], sts_list[1], 2)
        # future3 = executor.submit(find_censored_words, tokens, blacklist[data_types[2]], sts_list[2], 3)
        # future4 = executor.submit(find_censored_words, tokens, blacklist[data_types[3]], sts_list[3], 4)
        # future5 = executor.submit(find_censored_words, tokens, blacklist[data_types[4]], sts_list[4], 5)
        # future6 = executor.submit(find_censored_words, tokens, blacklist[data_types[5]], sts_list[5], 6)
        # future7 = executor.submit(find_censored_words, tokens, blacklist[data_types[6]], sts_list[6], 7)
        #
        # result[data_types[0]] = future1.result()
        # result[data_types[1]] = future2.result()
        # result[data_types[2]] = future3.result()
        # result[data_types[3]] = future4.result()
        # result[data_types[4]] = future5.result()
        # result[data_types[5]] = future6.result()
        # result[data_types[6]] = future7.result()

    return result


def parallel_load():
    blacklist = {}
    table_list = ['adv', 'cur', 'ero', 'oth', 'pol', 'scm', 'vio']
    db_name = 'censor_new'
    try:
        with ThreadPoolExecutor(max_workers=4) as thread_executor:
            futures = []
            for table in table_list:
                futures.append([table, thread_executor.submit(load_from_db, table, db_name)])
            for future in futures:
                blacklist[future[0]] = future[1].result()
        return blacklist
    except Exception as e:
        print('加载失败：' + str(e))
