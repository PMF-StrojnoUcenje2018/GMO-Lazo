
g++ -std=c++14 -O2 src/features.cpp -o src/features
rm -rf datasets/test/new-features

mkdir datasets/test/new-features
for i in datasets/test/samples/*; do
    echo $i
    mkdir datasets/test/new-features/$(basename $i)
    for j in $i/*; do
	echo $j | src/features > datasets/test/new-features/$(basename $i)/$(basename $j).json 
    done
done
