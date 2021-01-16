import jieba as jb
class wordSplit():
    def __init__(self, stop_word_path="stopWords.txt"):
        self.stop_word_path = stop_word_path
        self.stop_word_list = self.get_stop_word_list(self.stop_word_path)
        self.extend_word_list = [' ', '\xa0', '\n', '\t']    # 一些无法列在stopWords.txt中的停用词
    #获取停用词列表
    def get_stop_word_list(self, stop_word_path):
        stop_word_list = [line.strip() for line in open(self.stop_word_path, encoding='UTF-8').readlines()]
        return stop_word_list

    #对句子进行分词
    def separate_sentence(self, sentence):
        print('正在进行分词')
        sentence_seperated = jb.lcut(sentence.strip()) #lcut返回list
        # 去停用词
        outstr = ''
        for word in sentence_seperated:
            if word not in self.stop_word_list:
                if word not in self.extend_word_list:
                    outstr += word
                    outstr += " "
        return outstr

    #生成分词文档
    def separate_txt(self,r_path,w_path):
        inputs = open(r_path, 'r', encoding='UTF-8')
        outputs = open(w_path, 'w', encoding='UTF-8')
        for line in inputs:
            line_seg = self.separate_sentence(line)
            outputs.write(line_seg)
        outputs.close()
        inputs.close()
        print("删除停用词和分词成功！！！")
