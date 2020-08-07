mkdir test_data_public

chmod u+x code.py

wget https://www2.ims.uni-stuttgart.de/data/sem-eval-ulscd/semeval2020_ulscd_eng.zip
unzip -n semeval2020_ulscd_eng.zip
mv semeval2020_ulscd_eng test_data_public/english
rm semeval2020_ulscd_eng.zip

# German
wget https://www2.ims.uni-stuttgart.de/data/sem-eval-ulscd/semeval2020_ulscd_ger.zip
unzip -n semeval2020_ulscd_ger.zip
mv semeval2020_ulscd_ger test_data_public/german
rm semeval2020_ulscd_ger.zip

# Latin
wget https://zenodo.org/record/3734089/files/semeval2020_ulscd_lat.zip
unzip -n semeval2020_ulscd_lat.zip
mv semeval2020_ulscd_lat test_data_public/latin
rm semeval2020_ulscd_lat.zip

# Swedish
wget https://zenodo.org/record/3730550/files/semeval2020_ulscd_swe.zip
unzip -n semeval2020_ulscd_swe.zip
mv semeval2020_ulscd_swe test_data_public/swedish
rm semeval2020_ulscd_swe.zip

mkdir -p answer/task1/ && mkdir -p answer/task2/

python3 code.py

zip -r models_trained models_trained/ && rm -r models_trained/
