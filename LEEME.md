# Proyecto, Parte 1: Diseño del control de acceso (Verdeazul Carbono S.A.)

**CE-1115 Seguridad de la Información, Grupo 6.** Entrega: jueves 15 de octubre de 2026, antes de la clase.
Integrantes: Randall Bolaños López, Javier Tenorio Cervantes, Julio Varela Venegas, Axel Flores Lara.

## Estado

El cliente respondió las consultas por escrito y sus respuestas ya están incorporadas en los seis
archivos de entrega, que compilan. **Quedan dos fechas por escribir en la minuta** (ver «Lo que falta»).

## Qué hay en la carpeta

| Carpeta o archivo | Qué es | ¿Se entrega? |
|---|---|---|
| `Entregables/P1_Politicas_grupo6` (.tex, .pdf) | Informe de políticas. 12 páginas de contenido; Anexo A = minuta, Anexo B = supuestos declarados | Sí |
| `Entregables/P1_ControlAcceso_grupo6` (.tex, .pdf) | Modelo, HBAC y separación de responsabilidades. 12 páginas de contenido | Sí |
| `Entregables/P1_Matriz_grupo6` (.tex, .pdf) | La matriz (10 sujetos, 10 objetos), sus 20 reglas, 37 casos de prueba | Sí |
| `Entregables/P1_Arquitectura_grupo6` (.tex, .pdf) | Componentes, tecnologías y decisiones. 12 páginas de contenido; diagramas en anexo | Sí |
| `Entregables/P1_AtributoDI_grupo6` (.tex, .pdf) | Indicadores DI1 a DI4 | Sí |
| `Entregables/P1_Presentacion_grupo6.pdf` | 25 láminas de la defensa | Sí |
| `Consultas_cliente/Respuesta_cliente.md` | La respuesta del cliente, tal como llegó | No: es la fuente de la minuta |
| `Consultas_cliente/P1_ConsultasCliente_grupo6` (.tex, .pdf) | Las 26 preguntas que preparó el equipo | No |
| `Consultas_cliente/Correo_solicitud_cita.md` | Borrador del correo de solicitud | No |
| `Presentacion_fuente/` | Fuente de las láminas y versión con notas del orador (guion de estudio) | No |

Los tres documentos con límite (políticas, control de acceso y arquitectura) están **justo en 12 páginas
de contenido**, el máximo del enunciado. Si se agrega texto a alguno hay que quitar otro tanto, y
comprobarlo al recompilar: el contenido termina donde empieza el Anexo A.

## Lo que falta, en orden

1. **Escribir las dos fechas de la minuta.** Al inicio de `P1_Politicas_grupo6.tex`, sustituir
   `\porllenar` en `\fechasolicitud` (día en que se envió el correo) y en `\fecharespuesta` (día en
   que respondió el cliente). Son las únicas marcas ámbar que quedan en los PDF. Recompilar.
2. **Leer los cinco documentos completos, los cuatro.** El diseño cambió en varios puntos y las
   preguntas del profesor son individuales.
3. **Revisar las decisiones que tomó el equipo** (siguiente sección) y ajustar las que no compartan.
4. **Entregar** por la plataforma del curso: los cinco `.tex`, los cinco `.pdf` y el PDF de las láminas.

## Qué cambió con las respuestas del cliente

El cliente respondió 14 de las 26 consultas. **Numeró sus respuestas de corrido (P-01 a P-14)**; los
documentos usan la numeración del equipo. La equivalencia está en `Respuesta_cliente.md` y en la minuta.

| Consulta | Respuesta | Cambio en el diseño |
|---|---|---|
| P-01 | Un verificador puede medir, por excepción | Habilitación temporal de técnico; la exclusión TEC–VER pasa a dinámica. La regla C3 no cambia |
| P-02 | No hay cifras; sin cantidades fijas | Umbrales por rol, calibrados con datos; supuestos de capacidad en Arquitectura, Anexo B |
| P-03 | El verificador devuelve, no edita | Se confirma |
| P-04 | Demostrar autenticidad, estado y quién autorizó | Sello de la empresa + comprobación pública por código (fila PUB, regla C20). No se exige firma digital por persona |
| P-05 | Períodos: decide la coordinación, registra administración. Asignan los supervisores | Rol nuevo SUP (son siete). ADM registra y GER abre y cierra |
| P-06 | La revisión sigue después del cierre | El cierre detiene registrar y modificar, no revisar ni aprobar |
| P-07 | Revisión técnica antes de la autorización final | Enmienda: solicitar, corregir, revisar, autorizar. Verificador distinto si es material |
| P-08 | Nunca dos certificados vigentes ni uno borrado | Revocar y reemitir en un solo acto si cambian las toneladas |
| P-10 | Avisar primero; no bloquear de inmediato | Tres niveles: aviso, verificación adicional, restricción temporal |
| P-11 | Fincas asignadas, con flexibilidad | Asignaciones temporales que crea el supervisor y vencen solas |
| P-15 | Personas físicas y sociedades; sin registro de vínculos | Declaración de vínculos y abstención (regla C17) |
| P-18 | Sin norma definida; acceso remoto; exportan evidencia | Las ISO quedan como referencia; verbo «exportar» para AUD (regla C18) |
| P-22 | Señal inestable; registro posterior; sin app sin conexión | Fecha de medición y fecha de registro; equipos no confiables |
| P-23 | Hospedaje por decidir; sin especialistas; sin presupuesto para llaves | Servidor virtual contratado; passkey del propio equipo; llaves físicas solo para cuentas privilegiadas |

### Decisiones que tomó el equipo y conviene revisar

El cliente dejó varias cosas «a criterio del equipo consultor». Están justificadas en los documentos,
pero son decisiones nuestras y hay que poder defenderlas:

- **GER incluye a la «coordinación de certificación».** El cliente usa los dos nombres; el diseño los
  reúne en un rol. Si son puestos distintos, sería un rol más.
- **Enmienda material.** Revisa un verificador distinto del original solo cuando cambia un dato del
  cálculo de toneladas o ya hay certificado (Control de acceso §5.3).
- **Comprobación pública de certificados.** Entra en el diseño por la respuesta a P-04, aunque la
  pregunta P-25 no se respondió.
- **Hospedaje y llaves físicas.** Arquitectura §5 y Políticas §7. El rango de precio de las llaves
  (25 a 60 dólares) es de referencia: conviene cotizar antes de la defensa.
- **Sello electrónico de persona jurídica** (Arquitectura §4.8). Se menciona como mejora opcional para
  dar presunción legal al sello. Confirmar con la autoridad certificadora cómo se emite y se custodia
  antes de afirmarlo en la defensa.
- **Si además de la respuesta escrita hubo reunión**, agregar su fecha y medio en «Datos de la
  consulta» de la minuta: hoy dice solo que el cliente respondió por escrito.
- **Supuestos de capacidad** (100 cuentas internas, 2 000 fincas, etc.): Arquitectura, Anexo B.
- **Doce consultas sin respuesta** quedaron como supuestos declarados: Políticas, Anexo B.

## Cosas que conviene confirmar ya

- **Número de grupo.** Se usó el 6. Si es otro: cambiar `\newcommand{\numgrupo}{6}` al inicio de cada
  `.tex` y renombrar los archivos.
- **Reparto de la defensa.** Es una propuesta; el nombre aparece abajo a la derecha de cada lámina
  (`\quien{...}` en la fuente).
- **Duración de la defensa.** Las 25 láminas están pensadas para unos 20 minutos.

| Bloque | Láminas | Expone |
|---|---|---|
| Cliente y activos | 2 a 4 | Randall |
| Amenazas y marco legal | 5 y 6 | Javier |
| Modelo de control de acceso | 7 a 9 | Julio |
| Controles de historial | 10 y 11 | Axel |
| Separación de responsabilidades | 12 a 14 | Randall |
| Fricción | 15 | Javier |
| Recorrido por la matriz | 16 a 18 | Julio |
| Arquitectura | 19 a 21 | Axel |
| Riesgos residuales, respuestas del cliente y decisiones delegadas | 22 a 24 | Javier |

Las preguntas del profesor son individuales. `Presentacion_fuente/P1_Presentacion_grupo6_notas.pdf`
trae, después de cada lámina, qué decir y qué responder si preguntan. Lo deben leer los cuatro completo.

## Cómo recompilar

Cada `.tex` es autónomo. Dos pasadas, para el índice y las referencias cruzadas:

```
pdflatex P1_Politicas_grupo6.tex
pdflatex P1_Politicas_grupo6.tex
```

Las láminas: `pdflatex P1_Presentacion_grupo6.tex` en `Presentacion_fuente/`, y copiar el PDF a
`Entregables/`. La versión con notas: `pdflatex P1_Presentacion_grupo6_notas.tex`.

En los documentos, la marca `[minuta P-07]` señala una decisión que sale de una respuesta del cliente
y `[supuesto P-13]` una que el equipo fijó porque el cliente no dio el dato.

## El diseño en seis frases

1. **Modelo:** siete roles con restricciones (RBAC₂), sin jerarquía, más condiciones de atributo que solo pueden quitar.
2. **Historial:** cuatro controles, uno de cada tipo. H1 frecuencia, H2 tiempo, H3 combinada, H4 secuencia. Los tres primeros responden por niveles: aviso, verificación, restricción temporal.
3. **Separación:** por etapas del flujo y comprobada por medición, no por puesto. Nadie emite: emite el sistema.
4. **Matriz:** diez sujetos, diez objetos, veinte reglas (C1 a C20), treinta y siete casos de prueba.
5. **Arquitectura:** un solo punto de decisión en el servidor (OPA) y un segundo candado en la base (PostgreSQL), en un servidor virtual contratado.
6. **Bitácora:** solo se inserta, va encadenada y su huella sale del servidor cada día.
