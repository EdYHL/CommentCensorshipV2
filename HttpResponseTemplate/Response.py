from utils.logic import add_censors


class Response:
    def __init__(self):
        self.code = 0  # 返回码
        self.message = ''  # 与返回码对应的信息
        self.risk = 0  # 有无风险
        self.level1 = 0  # 一级风险度
        self.level2 = 0  # 二级风险度
        self.level3 = 0  # 三级风险度
        self.containsWebsite = 0  # 是否包含网站
        self.details = {}  # 匹配到的违禁词汇
        self.riskTypes = []  # 信息涉嫌的违规类别
        self.replacedResult = ''  # 屏蔽后的字符串
        self.attention = 0  # 是否需要人工处理
        self.finalResult = 0  # 机器的处理方式

    def risk_factor(self) -> float:
        value = self.level1 + self.level2 + self.level3 + self.containsWebsite
        return value / (1 + value)

    def success(self, data: dict, contains_website: bool, original: str) -> None:
        self.code = 101
        self.message = '成功'
        self.details = data
        self.containsWebsite = int(contains_website)
        censor_chars = ''
        if len(data) > 0:
            for v in data.values():
                self.level1 = self.level1 + len(v)
                # self.level1 = self.level1 + len(v['guaranteed'])
                self.level2 = self.level2 + len(v)
                # self.level2 = self.level2 + len(v['highRisk'])
                self.level3 = self.level3 + len(v)
                # self.level3 = self.level3 + len(v['lowRisk'])
                for k in v['guaranteed'].keys():
                    censor_chars.join(k)
                for k in v['highRisk'].keys():
                    censor_chars.join(k)
                for k in v['lowRisk'].keys():
                    censor_chars.join(k)
        if contains_website:
            self.attention = 1
        risk_factor = self.risk_factor()
        self.risk = risk_factor >= 0.5
        if risk_factor > 0:
            risk_type_dict = {
                'adv': '广告',
                'cur': '辱骂',
                'ero': '色情',
                'oth': '其他',
                'pol': '政治',
                'scm': '诈骗',
                'vio': '暴力'
            }
            for k in data.keys():
                self.riskTypes.append(risk_type_dict[k])
            self.replacedResult = add_censors(original, censor_chars)
            self.finalResult = 1

    def error(self, msg: str):
        self.clear()
        self.code = 109
        self.message = msg

    def to_dict(self):
        result: dict = {}
        if self.code is not None:
            result['code'] = self.code
        if self.message is not None and self.message != '':
            result['message'] = self.message
        if self.risk is not None:
            result['risk'] = self.risk
        result['level1'] = self.level1
        result['level2'] = self.level2
        result['level3'] = self.level3
        if self.containsWebsite is not None:
            result['containsWebsite'] = self.containsWebsite
        if len(self.details) > 0:
            result['details'] = self.details
        if len(self.riskTypes) > 0:
            result['riskTypes'] = self.riskTypes
        if self.replacedResult != '':
            result['replacedResult'] = self.replacedResult
        if self.attention != 0:
            result['attention'] = self.attention
        result['finalResult'] = self.finalResult
        return result

    def clear(self):
        self.code = None  # 返回码
        self.message = None  # 与返回码对应的信息
        self.risk = None  # 有无风险
        self.level1 = None  # 一级风险度
        self.level2 = None  # 二级风险度
        self.level3 = None  # 三级风险度
        self.containsWebsite = None  # 是否包含网站
        self.details = None  # 匹配到的违禁词汇
        self.riskTypes = None  # 信息涉嫌的违规类别
        self.replacedResult = None  # 屏蔽后的字符串
        self.attention = None  # 是否需要人工处理
        self.finalResult = None  # 机器建议处理方式