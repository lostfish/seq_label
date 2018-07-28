#! /bin/bash

entity_file=./conf/person.txt
template_file=./conf/template
text_file=./test/test.u8
text_field=0
out_dir=model

# train
./do_train.sh $entity_file $template_file $text_file $text_field $out_dir

# predict
model_file=$out_dir/model.bin
out_file=$out_dir/result.txt
./do_predict.sh $model_file $text_file $text_field $out_file

# eval
rec_file=$out_dir/train.txt.debug
eval_file=$out_dir/eval.txt
new_word_file=$out_dir/new_word.txt
./do_eval.py $rec_file $out_file > $eval_file
awk -F'\t' '$1=="new:"{n=split($3,a,";");for(i=1;i<=n;i++)b[a[i]]++}END{for(k in b) print k,b[k]}' OFS='\t' $eval_file|sort -t$'\t' -k2nr > $new_word_file
