Thank you for contributing to AtCoderAPI

contributing guides are coming soon.


# build document 
(to do: make readthedocs.yaml) 
```bash
$ poetry run sphinx-apidoc -F -H atcoder-api -A kagemeka -V <version> docs/ src/
$ cd docs/
$ make clean && make html
```


## update version
edit 
- pyproject.toml