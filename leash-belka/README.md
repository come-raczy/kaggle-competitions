package name is kaggle-leash-BELKA

https://www.kaggle.com/competitions/leash-BELKA/overview

data subdirectory can be created as follows:

    mkdir data
    cd data
    kaggle competitions download -c leash-BELKA
    unzip leash-BELKA.zip

The descriptors produced by rdkit contain 'inf' instead of the NaN that xgboost
expects. All the descriptors files must be edited:

    for f in desc01_consolidated_train_*.csv ; do echo $f ; sed -i 's/inf/NaN/g' $f ; done



