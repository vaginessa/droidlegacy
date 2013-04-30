find data/ -type f -exec rm -f '{}' \;
rm detectionResults.txt
rm -rf data/flatClasses/*
rm -rf data/disassembled/*
cp toAnalyze/* data/apk/
