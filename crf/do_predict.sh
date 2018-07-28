#! /bin/bash

if [ $# -ne 4 ];then
    echo "usage: $0 <model_file> <input_file> <text_field> <out_file>"
    exit -1
fi

model_file=$1
input_file=$2
text_field=$3
out_file=$4

./gen_crf_test.py $input_file $text_field > $input_file.1

./crf_test -m $model_file $input_file.1 > $out_file.1

./gen_norm_result.py $out_file.1 $out_file

rm -rf $input_file.1
rm -rf $out_file.1
