class CustomError(Exception):
    def __init__(self, code, status_code, err_info):  # 为自定义数据赋值
        super().__init__(self)
        self.code = code
        self.err_info = err_info
        self.status_code = status_code

    def __str__(self):  # 将自定义错误转换为字符串
        return 'code: {} status code: {} err information: {}'.format(
            str(self.code), str(self.status_code), str(self.err_info))
