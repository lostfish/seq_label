
# 基于CRF的命名实体识别

训练CRF模型识别命名实体

utf-8 encoding

## 运行

1. 编译CRF++

	    cd ./tools
	    tar zxvf CRF++-0.58.tar.gz
	    ./configure
	    make
	    make intall
	    cp crf_learn ..
	    cp crf_test ..
	    cd -

2. 安装marisa-trie

	    cd tools
	    tar zxvf marisa-trie-0.7.tar.gz
	    python setup.py intall
	    cd -

3. 测试实例

	sh test.sh

	在./model/下生成文件:

	    eval.txt
	    model.bin
	    new_word.txt
	    result.txt
	    train.txt
	    train.txt.debug

	其中，model.bin就是训练的模型文件，result.txt是识别的结果文件，第一列为文本，第二列为实体，实体用;分隔。new_word.txt是新实体文件，eval.txt为评估结果文件，有实体识别的**准确率**和**召回率**。


如果只是训练模型，可以调用脚本do_train.sh

	./do_train.sh <entity_file> <template_file> <text_file> <text_field> <out_dir>

如果只是预测，那么可以调用脚本do_predict.sh

	./do_predict.sh <model_file> <input_file> <text_field> <out_file>

## 改进

+ crf_learn的参数可以调节
+ ./conf/template的特征模块可以调节
+ 用实体匹配文本获取的训练语料存在不准的情况，可以优化

    例如：一万块的iPhone X很贵？俄罗斯人把它卖到了三万块 -> 罗斯


## 其他

###CRF++训练和预测文件格式

固定列数，第一列是token，最后一列是tag, 中间可以是其他的

###模版格式

%x[row,col] 
row 相对位置
col 绝对位置

两种模版:

1. U unigram features
2. B bigram features

unigram: |output tag| x |all possible strings expanded with a macro|
bigram: |output tag| x |output tag| x |all possible strings expanded with a macro|

Only one bigram template ('B') is used. This means that only combinations of previous output token and current token are used as bigram features. 

如果只有两列，'B' 相当于 %x[-1,1] ?

## 参考

+ https://taku910.github.io/crfpp/
+ http://www.52nlp.cn/%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D%E5%85%A5%E9%97%A8%E4%B9%8B%E5%AD%97%E6%A0%87%E6%B3%A8%E6%B3%954
+ http://www.hankcs.com/nlp/the-crf-model-format-description.html
