# Input data

This directory contains only the raw structure and Wannier90 files required by
`notebooks/wannier_embedding_exchange.ipynb`.

| Directory | Physical role | Orbitals per spin |
|---|---|---:|
| `host_wannier/` | Clean nonmagnetic 1x1 host used for the propagator | 11 |
| `fe4x4_wannier/` | Spin-resolved Fe-containing 4x4 twin | 181 |
| `pristine4_wannier/` | Spin-resolved, Fe-free matched 4x4 twin | 176 |

Each directory contains a VASP `POSCAR`, Cartesian Wannier centers, and a
gzip-compressed Wannier90 real-space Hamiltonian. The notebook reads the gzip
files directly; do not decompress them into the repository.

The spin-resolved suffixes have the following meaning in this collinear,
spin-orbit-free calculation:

- `.1_*`: majority-spin channel;
- `.2_*`: minority-spin channel.

The source locations recorded with the dataset were:

- host: `fullrelax_host_20260716/z0/host1x1/wannier`;
- Fe/pristine twins:
  `nmgeom_j_20260712/z0/{fe4x4,pristine4_defgeom}/wannier`.

No production-reference arrays or derived Hamiltonians are included. Confirm
that you have permission to redistribute these first-principles data before
making the repository public.
