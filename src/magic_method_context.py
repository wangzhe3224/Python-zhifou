import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)


# 上下文管理
class DisableLogging:

    def __enter__(self):
        print(f"> 进入上下文，日志暂时取消")
        logging.disable(logging.CRITICAL)
    
    def __exit__(self, exception_type, exception_val, trace):
        logging.disable(logging.NOTSET)
        print(f"> 离开上下文")
        

if __name__ == '__main__':

    logging.info('进入无日志上下文以前')

    with DisableLogging():
        logging.info('不会显示INFO')

    logging.info('重新显示INFO')

    # 一些IO资源
    # 创建一些临时的环境，可以特殊的环境变量等等