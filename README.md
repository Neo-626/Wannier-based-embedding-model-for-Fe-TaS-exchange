# Wannier-based embedding model for Fe/TaS₂ exchange

This notebook calculates the exchange interaction between two Fe adatoms on
monolayer 1H-TaS₂ using a Wannier-based *ab initio* embedding model.

## Run

In the repository folder, install the requirements.

```bash
pip install -r requirements.txt
```

Open [`wannier_embedding_exchange.ipynb`](notebooks/wannier_embedding_exchange.ipynb)
in Jupyter and select **Run → Run All Cells**. Numerical parameters are in the
first code cell.

Requires Python 3.9+ and NumPy 1.22+.

## Method

The notebook extracts a spin-dependent impurity potential from matched 4×4
Wannier Hamiltonians, calculates the pristine-host Green function, and evaluates
the exchange interaction using the Lloyd formula.

$$
\mathcal H=-J\\mathbf e_1\cdot\mathbf e_2,
\qquad
J=\frac{\Omega_{\mathrm{AFM}}-\Omega_{\mathrm{FM}}}{2}.
$$

Positive $J$ favors parallel moments.

