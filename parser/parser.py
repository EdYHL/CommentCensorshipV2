def parse_result(guaranteed: dict, high_risk: dict, low_risk: dict):
    g_keys = guaranteed.keys()
    h_keys = high_risk.keys()
    l_keys = low_risk.keys()

    for g in g_keys:
        if g in h_keys:
            del high_risk[g]
        if g in l_keys:
            del low_risk[g]
    for h in h_keys:
        if h in l_keys:
            del low_risk[h]

    return {
        'guaranteed': guaranteed,
        'highRisk': high_risk,
        'lowRisk': low_risk
    }


def parse_request_types(types: str) -> list:
    if types == 'all':
        return ['adv', 'cur', 'ero', 'oth', 'pol', 'scm', 'vio']
    else:
        result = []
        if 'adv' in types:
            result.append('adv')
        if 'cur' in types:
            result.append('cur')
        if 'ero' in types:
            result.append('ero')
        if 'oth' in types:
            result.append('oth')
        if 'pol' in types:
            result.append('pol')
        if 'scm' in types:
            result.append('scm')
        if 'vio' in types:
            result.append('vio')
        return result

