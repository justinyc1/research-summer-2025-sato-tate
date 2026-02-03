# Component Group $\text{ST}(\text{Jac}(\text{C}_{p^2}))/\text{ST}^{0}(\text{Jac}(\text{C}\_{p^2}))$

This folder contains the code used pertaining to the component group of $\text{ST}(\text{Jac}(\text{C}_{p^2}))$.

## Organization

- `component_group_generator.sage` — Contains the function used to compute a generator of the component group.
- `example.ipynb` — A demonstration of computing a component group generator for $p=5, 7$.

## Installation and Prerequisites  

Please ensure to have the latest version of Sage/SageMath installed. An official installation guide can be found [here](https://doc.sagemath.org/html/en/installation/index.html#) for Windows, macOS, and Linux-based users.

> Tested with version 10.7  

- **(Optional)** To run ```example.ipynb``` locally, one method to do so is

    1. Download and install Sage/SageMath
    2. Launch Jupyter from Sage's terminal/shell with

    ```bash
        sage -pip install jupyter
        sage -n jupyter
    ```
    
        and follow the instructions on the screen

    3. Open ```example.ipynb``` and ensure SageMath is selected as the kernel.

    > Note: Installing Sage/SageMath via ```pip install sagemath``` is insufficient, as a limited package of Sage/SageMath will be installed. Instead, please install the *full* Sage/SageMath distribution from its [official website](https://www.sagemath.org/).

## Cloning

To clone the repository, please install Git and run the following in a terminal:

```bash
    git clone https://github.com/justinyc1/Degeneracy-and-Sato-Tate-Groups-of-C_p2.git
    cd Degeneracy-and-Sato-Tate-Groups-of-C_p2
```
