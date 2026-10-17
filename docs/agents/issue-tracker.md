# Issue tracker: GitHub

Los issues y las specs de este repo viven en GitHub Issues. Todas las operaciones usan el CLI `gh`.

## Convenciones

- **Crear un issue**: `gh issue create --title "..." --body "..."`. Para cuerpos de varias líneas, usar heredoc.
- **Leer un issue**: `gh issue view <number> --comments`, filtrando con `jq` y pidiendo también los labels.
- **Listar issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` con los filtros de `--label` y `--state` que correspondan.
- **Comentar**: `gh issue comment <number> --body "..."`.
- **Agregar o quitar labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`.
- **Cerrar**: `gh issue close <number> --comment "..."`.

El repo se infiere de `git remote -v`; `gh` lo resuelve solo cuando corre dentro del clon.

## Pull requests as a request surface

**PRs as a request surface: no.** _(Poner en yes si el repo trata PRs externos como pedidos de features; `/triage` lee este flag.)_

Cuando el flag está en yes, los PRs pasan por los mismos labels y estados que los issues, con los equivalentes de `gh pr`:

- **Leer un PR**: `gh pr view <number> --comments` y `gh pr diff <number>` para el diff.
- **Listar PRs externos para triage**: `gh pr list --state open --json number,title,body,labels,author,authorAssociation,comments` y quedarse solo con los `authorAssociation` de `CONTRIBUTOR`, `FIRST_TIME_CONTRIBUTOR` o `NONE`.
- **Comentar, etiquetar o cerrar**: `gh pr comment`, `gh pr edit --add-label` o `--remove-label`, `gh pr close`.

GitHub comparte la numeración entre issues y PRs, así que un `#42` puede ser cualquiera de los dos: resolver con `gh pr view 42` y caer a `gh issue view 42`.

## Cuando un skill dice "publicar en el issue tracker"

Crear un issue de GitHub.

## Cuando un skill dice "traer el ticket"

Correr `gh issue view <number> --comments`.
