
g++ -std=c++14 -O2 src/features.cpp -o src/features
rm -rf datasets/training/new-features

mkdir datasets/training/new-features
for i in datasets/training/samples/*; do
    echo $i
    mkdir datasets/training/new-features/$(basename $i)
    for j in $i/*; do
	echo $j | src/features > datasets/training/new-features/$(basename $i)/$(basename $j).json 
    done
done
