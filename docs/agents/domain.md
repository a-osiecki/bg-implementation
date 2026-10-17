# Domain docs

Cómo consumen los skills la documentación de dominio de este repo durante la exploración.

## Antes de explorar, leer

- **`CONTEXT.md`** en la raíz del repo, o
- **`CONTEXT-MAP.md`** en la raíz si existe: apunta a un `CONTEXT.md` por contexto. Leer los que correspondan al tema.
- **`docs/adr/`**: leer los ADR que toquen el área de trabajo.

Si alguno de estos archivos no existe, **seguir en silencio**. No marcar su ausencia ni proponer crearlos de entrada. El skill `domain-modeling` los crea cuando un término o una decisión realmente se resuelve.

## Estructura de archivos

Repo single-context, que es el caso de este repo:

```
/
├── CONTEXT.md
├── docs/adr/
│   └── 0001-decision.md
└── src/
```

## Usar el vocabulario del glosario

Cuando una salida nombre un concepto de dominio, usar el término definido en `CONTEXT.md`. No cambiarlo por sinónimos que el glosario evite.

Si el concepto no está en el glosario, es una señal: o se está inventando lenguaje que el proyecto no usa, o hay un hueco real para el skill `domain-modeling`.

## Conflictos con un ADR

Si una salida contradice un ADR existente, marcarlo en vez de pisarlo en silencio:

> _Contradice el ADR-0007, pero conviene reabrirlo porque..._
