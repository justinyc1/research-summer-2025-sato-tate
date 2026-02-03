# Component Group $\text{ST}(\text{Jac}(\text{C}_{p^2}))/\text{ST}^{0}(\text{Jac}(\text{C}\_{p^2}))$

This folder contains the code used pertaining to the component group of $\text{ST}(\text{Jac}(\text{C}_{p^2}))$.

## Installation and Prerequisites  

- Please ensure to have the latest version of Sage/SageMath installed.

> Tested with version 10.7

An official Sage/SageMath installation guide can be found [here](https://doc.sagemath.org/html/en/installation/index.html#) for Windows, macOS, and Linux-based users.  

- *(Optional)* To run [example.ipynb](https://github.com/justinyc1/research-summer-2025-sato-tate/blob/paper/component_group/example.ipynb) locally, please install Jupyter Notebook with 
```
pip install  notebook
```
and run
```
jupyter notebook example.ipynb
```

- To clone the repository, please install Git and run the following in a terminal:

```bash
git clone https://github.com/justinyc1/Degeneracy-and-Sato-Tate-Groups-of-C_p2.git
cd Degeneracy-and-Sato-Tate-Groups-of-C_p2
```

## Organization

- `component_group_generator.sage` contains the function used to compute a generator of the component group.
- `example.ipynb` is a demonstration of computing a component group generator for $p=5, 7$.
