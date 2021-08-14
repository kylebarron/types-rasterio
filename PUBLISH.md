Steps to publish

```
poetry run bumpversion minor
rm -rf dist
poetry build
poetry run twine upload dist/*
```
