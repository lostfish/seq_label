#! /bin/bash

if [ $# -ne 5 ];then
    echo "usage: $0 <entity_file> <template_file> <text_file> <text_field> <out_dir>"
    exit -1
fi

entity_file=$1
template_file=$2
text_file=$3
text_field=$4
out_dir=$5

mkdir -p $out_dir
if [ ! -e $out_dir ];then
    echo "not exist out_dir: $out_dir"
    exit -1
fi

train_file=$out_dir/train.txt
model_file=$out_dir/model.bin

# recognize entity word of vocab
# get crf input: one char and one tag pre line, null line marks the sentence end
# tag: B E M O
./gen_crf_train.py $entity_file $text_file $text_field $train_file > $train_file.debug

# train model: cost, template input_file, output_file
./crf_learn -c 1.5 $template_file $train_file $model_file
