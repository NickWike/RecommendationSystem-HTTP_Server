import jieba
import time
from string import punctuation

# 禁用 jieba 的打印日志
jieba.setLogLevel(0)


class MyTokenizer(jieba.Tokenizer):
    def __init__(self):
        super().__init__()
        # 加载自己的词汇模型
        # self.load_userdict("/home/zh123/PycharmProjects/RS_HttpServer/conf/search_worlds.txt")

        # 定义不需要的特殊符号
        self._not_used_worlds = punctuation + ' \t\n\f\r'

    def start_cut(self, text):
        result_list = []

        # list() 操作是将生成器转换一下避免 不能回访
        # 进行分词操作
        seg_list = list(self.cut_for_search(text))

        # 将分出来的词条过滤掉特殊符号
        word_list = list(filter(lambda s: s not in self._not_used_worlds, seg_list))
        # 过滤掉列表中有(包含于)关系的词汇
        for word in word_list:
            is_pre = False
            for item in word_list:
                if len(word) < len(item) and word in item:
                    is_pre = True
                    break
            if not is_pre:
                result_list.append(word)
        # 将拆分的词条去重
        result_list = list(set(result_list))
        return result_list


# 实例化一个分词器供外部调用
tokenizer = MyTokenizer()


if __name__ == '__main__':
    m = MyTokenizer()
    start_time = time.time()
    for i in range(100000):
        l = m.start_cut("钛合金框架书籍")
    print(time.time() - start_time)
