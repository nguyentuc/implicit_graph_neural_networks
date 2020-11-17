# Implicit Graph Neural Networks
This repository is the official PyTorch implementation of "Implicit Graph Neural Networks".

Fangda Gu*, Heng Chang*, Wenwu Zhu, Somayeh Sojoudi, Laurent El Ghaoui, [Implicit Graph Neural Networks](https://arxiv.org/abs/2009.06211), NeurIPS 2020.

## Requirements
The script has been tested running under Python 3.6.9, with the following packages installed (along with their dependencies):
* pytorch (tested on 1.6.0)
* torch_geometric (tested on 1.6.1)
* scipy (tested on 1.5.2)
* numpy (tested on 1.19.2)

## Tasks
We provide examples on the tasks of node classification and graph classification consistent with the experimental results of our paper. Please refer to ``nodeclassification`` and ``graphclassification`` for usage.

## Reference
- If you find ``IGNN`` useful in your research, please cite the following in your manuscript:

```
@inproceedings{gu2020implicit,
  title={Implicit Graph Neural Networks},
  author={Gu, Fangda and Chang, Heng and Zhu, Wenwu and Sojoudi, Somayeh and El Ghaoui, Laurent},
  journal={Advances in Neural Information Processing Systems},
  volume={33},
  year={2020}
}
```

