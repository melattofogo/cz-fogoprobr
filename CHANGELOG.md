## v2.1.1 (2026-10-18)

### Fix

- **base**: expor padrões de bump e changelog como atributos de classe

### Test

- **test_cli**: cobrir cz changelog e cz bump em repositório temporário
- **test_cz_fogoprobr**: importar commitizen antes do plugin

### Chore

- **pyproject**: ler a versão do project.version no cz bump

## v2.1.0 (2026-02-22)

### Feat

- **src/cz_fogoprobr/cz_fogoprobr.py**: adiciona body como input optional no template

### Refactor

- **src/cz_fogoprobr/__init__.py**: export CzFogoprobr from package root
- **src/cz_fogoprobr/cz_fogoprobr.py**: remove redundant module to fix circular imports
- **src/cz_fogoprobr/base.py**: move plugin class to dedicated base module

### Docs

- **README.md**: normaliza liguagem para pt-br

### Test

- **tests/test_cz_fogoprobr.py**: update imports and add configuration mocks

### Chore

- **pyproject.toml**: atualiza versionamento
- **pyproject.toml**: update entry point to point to package root

## v2.0.0 (2026-02-21)

### BREAKING CHANGE

- **cz_fogoprobr**: Template recriado para versao atual do commitizen

### Refactor

- **src/cz_fogoprobr/**: Move arquivos de src/ para src/cz_fogoprobr

### Chore

- **pyproject.toml**: atualiza versionamento
- **.gitignore**: atualiza .gitignore
- **py.typed**: adiciona py.typed
- **setup.py**: remove setup.py para usar apenas pyproject.toml
- **fogoprobr/**: renomeia fogoprobr/ para src/
- **tests/**: move tests/ para raiz

## v1.0.2 (2022-03-29)

### Feat

- **setup.py**: patch update de 1.0.1 para 1.0.2
- **setup.py**: patch update de 1.0.0 para 1.0.1
- **setup.py**: major update de 0.1.0 para 1.0.0
- **__init__.py**: adiciona __version__
- **setup.py**: adiciona README como long_description do package
- **setup.py**: adiciona url do repo do github do projeto
- **setup.py**: adiciona arquivo de setup para criacao do package commitizen-cz-fogoprobr
- **cz_fogoprobr.py**: adiciona FogoprobrCz

### Test

- **test_cz_fogoprobr.py**: adiciona testes de cz_fogoprobr

### Chore

- **README.md**: ajuste de caracteres de unicode non-utf8
- **README.md**: ajustes de caracteres de unicode non-utf8
- **README.md**: typo em autor
- **cz_fogoprobr.py**: alteracoes nas descricoes de prefix em choices
- **.gitignore**: adiciona gitignore em fogoprobr/
- **.gitignore**: Adiciona gitignore
