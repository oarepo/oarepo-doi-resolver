OARepo DOI resolver
====================
OArepo module that returns records metadata from its public DOI.

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]


Instalation
----------
```bash
    pip install oarepo_doi_resolver
```

Usage
-----
Module provides entrypoint for DOI resolving on url ```/resolve-doi/<doi>```
##### example
```https://127.0.0.1:5000/resolve-doi/10.5281/zenodo.5347031```

Entrypoint is reachable only for authenticated users. 



  [image]: https://img.shields.io/github/license/oarepo/oarepo-doi-resolver.svg
  [1]: https://github.com/oarepo/oarepo-doi-resolver/blob/master/LICENSE
  [2]: https://img.shields.io/travis/oarepo/oarepo-doi-resolver.svg
  [3]: https://travis-ci.org/oarepo/oarepo-doi-resolver
  [4]: https://img.shields.io/coveralls/oarepo/oarepo-doi-resolver.svg
  [5]: https://coveralls.io/r/oarepo/oarepo-doi-resolver
  [6]: https://img.shields.io/pypi/v/oarepo-doi-resolver.svg
  [7]: https://pypi.org/pypi/oarepo-doi-resolver