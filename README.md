# Implicit Graph Neural Networks
This repository is the official PyTorch implementation of "Implicit Graph Neural Networks".

Fangda Gu*, Heng Chang*, Wenwu Zhu, Somayeh Sojoudi, Laurent El Ghaoui. Implicit Graph Neural Networks, NeurIPS 2020.


## New environments: cuda 11.4, pytorch 1.12
Install pytorch: 
* conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
Install pytorch geometric: 
* pip install torch-scatter -f https://data.pyg.org/whl/torch-1.12.0+cu113.html
* pip install torch-sparse -f https://data.pyg.org/whl/torch-1.12.0+cu113.html
* pip install torch-geometric
Install scipy, numpy and networkx
* conda install -c conda-forge scipy
* conda install numpy
* conda install networkx


## Tasks
There are two task ``nodeclassification`` and ``graphclassification``.

## Run node classification task
In the folder nodeclassification: python train_IGNN_{name_dataset}.py

## Datasets
For Amazon dataset, please use the following dropbox link to download:
```
https://www.dropbox.com/sh/3gwr2wgh455q9pi/AAB0i6EQimVGslrqtsTIWsL0a?dl=0
```
Then put the `amazon-all` folder under the `data` folder.

## Run node graph task
In the folder nodeclassification: python train_IGNN.py --dataset {name_dataset}

