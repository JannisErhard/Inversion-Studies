#!/bin/bash
n=0

MOLPRO=/home/quantura/molpro/bin/molpro
NUM_OMP_THREADS=20
MEM=1000

echo Molpro Path: $MOLPRO
echo Number of OMP threads: $NUM_OMP_THREADS
echo Memory: $MEM m

export OMP_THREAD_LIMIT=$NUM_OMP_THREADS

for i in `find -iname output_2`
do
	string=`grep NOT $i`
	string_2=`echo $i | sed "s/output_2//g"`
	if [[ ! -z $string ]]; then
		cd $string_2
		pwd
		echo "$i is unconverged"
		$MOLPRO -t $NUM_OMP_THREADS -m $MEM --no-xml-output < input_2 > output_2
		cd -
	let n=$n+1
	fi
done
echo "In total, there were $n unconverged calculations."
