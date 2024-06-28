from concurrent.futures import ThreadPoolExecutor

from utils.load import load_from_db


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
