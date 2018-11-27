# Check shape outlines for radial structure

This code accompanies the paper

Schmidtmann & Fruend (2018): Radial frequency patterns describe a small and
perceptually distinct subset of all possible shapes. Vision Res, in press.

Please cite the original work if you use it.

# Installation

You may not need to install `check_rf.py`. It may be possible to simply
run the script. If you however want to install the script, we hightly
recommend using a [virtual
environment](https://docs.python.org/3/tutorial/venv.html). This may seem
complicated now, but it will save you a lot of headache in the future.
For installation run

    python setup.py install

from the location where this file is located. Pip installation is
currently not available.

# Usage

You can use `check_rf.py` either as a script or as a library.

## As a script

Run

    python check_rf.py -h

from the installation folder, or (if you installed it) run

    python -m check_rf -h

This will show you a help screen with more specific usage information.

## A a library

Here is a simple example

```python
>>> from check_rf import check_rf
>>> import numpy as np
>>> # Create an rf pattern 
>>> t = 2*np.pi*np.arange(50, dtype='d')/50
>>> rf4 = np.exp(1j*t)*(1 + np.cos(4*t))
>>> # Check on a small grid (up 21 points)
>>> result = check_rf(rf4, 21)
>>> result.center
0j
>>> result.error < 1e-10   # Should be basically 0
True

```

In the same way, you can check outlines in your own scripts.
