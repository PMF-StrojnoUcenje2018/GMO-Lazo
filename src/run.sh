
src/build-all-test.sh
python3 src/evaluate.py
python3 evaluation/mozgalo_test.py output.tsv evaluation/test.labels
