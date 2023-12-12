#!/bin/bash
n=0
for i in `find -iname output`
do 
	string=`grep NOT $i`
	if [[ ! -z $string ]]; then
		echo "$i is unconverged"
	let n=$n+1
	fi
done
echo "In total, there were $n unconverged calculations."
