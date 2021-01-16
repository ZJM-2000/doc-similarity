'''
相似度计算模块
使用算法:使用算法:TF-IDF
@:param artical_directory[文章分词列表文件夹路径]
'''
import  os
from gensim import corpora, models, similarities
from word_split import wordSplit
from artical_handler import ArticalHandler

class SimilarityCalculator():
    def __init__(self, artical_directory=None):
        self.all_words = []
        self.artical_directory = artical_directory
        self.word_split = wordSplit()
        self.artical_handler = ArticalHandler(self.artical_directory)


    #读取所有txt文档的分词词组
    def get_txt_words(self):
        artical_paths = os.listdir(self.artical_directory)  # 返回指定的文件夹包含的文件或文件夹的名字的列表
        for artical_path in artical_paths:
            if".txt" in artical_path:
                r_path = os.path.join(self.artical_directory, artical_path)  # 连接两个或更多的路径名 **\**\
                w_path = os.path.join(self.artical_directory, 'o'+artical_path)
                self.word_split.separate_txt(r_path,w_path) #到此实现了生成分词文档以o开头的文档
                #将分好词的文档转换为list
                txt=open(w_path,'r',encoding='UTF-8').read().split()
                self.all_words.append(txt)
                #print(self.all_words)
            else:
                if '.docx' in artical_path:
                    r_path = os.path.join(self.artical_directory, artical_path)  # 连接两个或更多的路径名 **\**\
                    d_path = os.path.join(self.artical_directory, artical_path[:-5] + '.txt')#去掉后缀.docx转换为.txt
                    w_path = os.path.join(self.artical_directory, 'o' + artical_path[:-5] + '.txt')
                    #Docx处理成txt文档存储起来
                    self.artical_handler.change_docx_to_txt(r_path,d_path)
                    #处理成分词
                    self.word_split.separate_txt(d_path,w_path)
                    #读取
                    docx=open(w_path,'r',encoding='UTF-8').read().split()
                    self.all_words.append(docx)
                elif '.pdf' in artical_path:
                    r_path = os.path.join(self.artical_directory, artical_path)  # 连接两个或更多的路径名 **\**\
                    d_path = os.path.join(self.artical_directory, artical_path[:-4] + '.txt')  # 去掉后缀.pdf转换为.txt
                    w_path = os.path.join(self.artical_directory, 'o' + artical_path[:-4] + '.txt')
                    #将pdf处理成txt存储
                    self.artical_handler.change_pdf_to_txt(r_path,d_path)
                    #处理分词
                    self.word_split.separate_txt(d_path,w_path)
                    #读取
                    pdf=open(w_path,'r',encoding='UTF-8').read().split()
                    self.all_words.append(pdf)



    #建立语料特征索引字典
    def get_corpus(self):
        dictionary = corpora.Dictionary(self.all_words)
        '''
        测试：
        print('词典：',dictionary)
        feature_cnt = len(dictionary.token2id)
        print('词典特征数：%d' % feature_cnt)
        doc_vectors = [dictionary.doc2bow(doc) for doc in self.all_words]
        print(len(doc_vectors))
        print(doc_vectors)
        '''
        #使用迭代器，方便后续使用
        for doc_words in self.all_words:
            yield dictionary.doc2bow(doc_words)

    # 生成所有文档的TFIDF模型
    def get_TFIDF_model(self):
        '''
        测试：
        tfidf = models.TfidfModel(doc_vectors)
        tfidf_vectors = tfidf[doc_vectors]
        print(len(tfidf_vectors))
        print(len(tfidf_vectors[0]))
        test_bow = dictionary.doc2bow(docT)
        print(len(test_bow))
        print(test_bow)
        '''
        tfidf=models.TfidfModel(self.get_corpus())
        return tfidf



    # 得到目录下每个txt文档和目标文档的TF-IDF相似度
    def get_test_TFIDF_similarities(self,target_path):
        docs_corpus = self.get_corpus  #获取doc_vectors
        TFIDF_model = self.get_TFIDF_model() #获取了models.TfidfModel(doc_vectors)=tfidf
        # 初始化一个相似度计算的对象[可用save()序列化保存到本地]
        TFIDF_similarity_calculator = similarities.MatrixSimilarity(corpus=list(TFIDF_model[docs_corpus()]))
        #print('sim',TFIDF_similarity_calculator)
        docT=open(target_path,'r',encoding='UTF-8').read().split()
        test_bow=corpora.Dictionary(self.all_words).doc2bow(docT)
        #print('test_bow',test_bow)
        sims=TFIDF_similarity_calculator[test_bow]
        print('每个文档与测试文档的相似度列表：', list(enumerate(sims)))

    # 两两文档相似度，并排序打印结果
    def get_all_TFIDF_similarities(self):
        docs_corpus = self.get_corpus
        TFIDF_model = self.get_TFIDF_model()
        # 初始化一个相似度计算的对象[可用save()序列化保存到本地]
        TFIDF_similarity_calculator = similarities.MatrixSimilarity(corpus=list(TFIDF_model[docs_corpus()]))
        for doc_vectors in docs_corpus():
            doc_similarities = list(enumerate(TFIDF_similarity_calculator[TFIDF_model[doc_vectors]]))
            #print('每个文档与其他文档的相似度列表：', doc_similarities)
            #美化
            yield self.prettify(doc_similarities)
    #两两排序结果
    # 两两文档相似度，并排序打印结果
    def get_all_TFIDF_similarities_sort(self):
        docs_corpus = self.get_corpus
        TFIDF_model = self.get_TFIDF_model()
        # 初始化一个相似度计算的对象[可用save()序列化保存到本地]
        TFIDF_similarity_calculator = similarities.MatrixSimilarity(corpus=list(TFIDF_model[docs_corpus()]))
        a=[]
        i=0
        for doc_vectors in docs_corpus():
            doc_similarities = list(enumerate(TFIDF_similarity_calculator[TFIDF_model[doc_vectors]]))
            j=0
            for sim in doc_similarities:
                if j>i:
                    b=(i,sim)
                    a.append(b)
                else:
                    j +=1
            i +=1
        sort_result=sorted(a,key=lambda item:-item[1][1])
        print('两两文档排序结果为：', sort_result)

    @staticmethod
    def prettify(doc_similarities):
        pretty_doc_similarities = []
        for each_similarity in doc_similarities:
            data = {
                'index': each_similarity[0],
                'similarity': '%.2f' % (each_similarity[1] * 100)
            }
            pretty_doc_similarities.append(data)
        return pretty_doc_similarities


if __name__ == '__main__':
    #单独分词test文档
    test_word_split = wordSplit()
    test_word_split.separate_txt('test.txt','otest.txt')

    sc=SimilarityCalculator('E:\pyproject\similarity\doc_sim\doc')
    sc.get_txt_words()
    sc.get_test_TFIDF_similarities('otest.txt') #与目标文档的相似度
    #两两文档结果：
    for index, doc in enumerate(sc.get_all_TFIDF_similarities()):
        print('文档{}与其他文档对比结果:'.format(index))
        for i in doc:
            print(i)

    sc.get_all_TFIDF_similarities_sort()
    print('----------------------------------')