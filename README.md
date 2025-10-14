# commitizen-cz-fogoprobr

## Instalação

```
pip install commitizen-cz-fogoprobr
```

## Uso

Listar commitizen instalados

```
cz ls
```

*Commit* de *code* em *stage*

```
cz --name cz_fogoprobr commit
```

Alternativamente, definindo o commitizen do projeto em um arquivo ```.cz``` do projeto

```
(echo [commitizen] & echo.name = cz_fogoprobr) >> .cz
cz commit
```

## Requisitos

- [commitizen](https://github.com/commitizen-tools/commitizen) ```4.9.1```

## Autor
Joao Fogo (fogo.melatto@gmail.com)

# Como o template funciona

- ```TYPES```

    Os “tipos” de *commit* que serão exibidos no prompt.  
    Cada item possui:

    - ```value```: o valor inserido na mensagem (ex: ```feat```, ```fix```, …)
    - ```name```: o rótulo amigável mostrado no menu.

- ```SCHEMA_PATTERN```

    Expressão regular usada pelo Commitizen para validar e depois analisar o cabeçalho de cada *commit*.

    O padrão aplicado é:

    ``` 
    <type>(<scope>)!: <subject>
    ```

    onde:

    - ```type``` ∈ ```feat|fix|docs|refactor|perf|test|chore```
    - ```scope``` é opcional: ```(<algo>)```
    - ```!``` é opcional: indica uma mudança que quebra compatibilidade (*breaking change*)
    - ```subject``` é o texto livre após o ```:```

- ```BUMP_PATTERN``` / ```BUMP_MAP```

    Define como o comando ```cz bump``` calcula a próxima versão com base no histórico de *commits*:

  - Se o corpo ou rodapé do *commit* contém **BREAKING CHANGE**, → **MAJOR**
  - Se o ```type``` do cabeçalho é **feat**, → **MINOR**
  - Se o ```type``` do cabeçalho é **fix**, → **PATCH**

- ```CHANGELOG_PATTERN```

    Define quais *commits* serão incluídos no *changelog* (de acordo com a lista de tipos definida).

- Métodos de ```CzFogoprobr```

  - ```info()``` / ```example()``` / ```schema()``` → usados pelos comandos de ajuda.
  - ```schema_pattern()``` → retorna a expressão regular mencionada acima.
  - ```questions()``` → define as perguntas interativas exibidas por ```cz commit```:

    1. Escolher o ```type``` (a partir de ```TYPES```)
    2. Definir o ```scope``` (opcional)
    3. Indicar se é ```is_breaking``` (sim/não)
    4. Escrever o ```subject``` (validado entre 5 e 72 caracteres)

  - ```message(answers)``` → monta o texto final do *commit*:
    ```
    {type}({scope}){!}: {subject}
    ```
  - ```subject(commit)``` → define como a linha aparecerá nas seções do *changelog*.
  
## Comandos rápidos

```bash
cz --name cz_fogoprobr info       # mostra informações do adaptador
cz --name cz_fogoprobr example    # mostra um exemplo de commit
cz commit                         # executa commit guiado com os prompts
cz check                          # valida mensagens em um intervalo
cz bump                           # calcula e aplica a próxima versão
cz changelog                      # regenera o arquivo CHANGELOG.md
cz ls                             # lista adaptadores disponíveis (seu plugin deve aparecer)