# Manual de usuario

**Sistema predictivo basado en Inteligencia Artificial para la gestión de ventas de Zorros Revolution Biker**

Versión 0.2 · Septiembre de 2026 · Corresponde al MVP desplegado en https://prediccionzrb.duckdns.org

> **Cambios respecto a la versión 0.1 (22 de agosto).** Aquella versión documentaba el prototipo visual diseñado en Stitch, sin base de datos ni funciones conectadas. Esta versión documenta el **sistema en funcionamiento**: todas las pantallas, botones y procedimientos descritos aquí operan sobre datos reales almacenados en la base y han sido verificados. Donde algo sigue siendo una limitación, se dice explícitamente en la sección 10.

> **Nota para quien maqueta este documento.** Los marcadores `[Captura: …]` indican dónde va cada imagen y qué debe mostrar. Tomarlas directamente del sistema en producción, con la sesión de administrador abierta.

---

## Contenido

1. Introducción
2. Elementos generales de la interfaz
3. Acceso al sistema
4. Centro de control
5. Registro de ventas
6. Productos e inventario
7. Pronóstico de ventas con Inteligencia Artificial
8. Usuarios y roles
9. Flujo recomendado de uso
10. Limitaciones de esta versión
11. Recuperación de acceso (administrador técnico)
12. Glosario

---

## 1. Introducción

### 1.1 Objetivo

Este manual explica cómo usar el sistema para registrar ventas, controlar el inventario, consultar el pronóstico de demanda y administrar las cuentas de acceso. Está escrito para el personal de la tienda y para quien administre el sistema.

### 1.2 Usuarios previstos

El sistema tiene dos roles. Lo que cada uno puede hacer se controla en el servidor, no solo en la pantalla: un cajero que intente abrir una función de administrador recibe un mensaje de "sin permiso".

| Rol | Qué puede hacer |
|---|---|
| **Cajero** | Registrar ventas, consultar el historial, ver el catálogo, recibir stock, cambiar su propia contraseña. |
| **Administrador** | Todo lo anterior, más: crear y editar productos, consultar y recalibrar el pronóstico, ver señales y recomendaciones de reabastecimiento, gestionar usuarios y roles. |

### 1.3 Requisitos

Un navegador actual (Chrome, Edge, Firefox o Safari) y conexión a internet. No hay nada que instalar. Funciona también en la pantalla de un teléfono, aunque las tablas se leen mejor en una computadora.

---

## 2. Elementos generales de la interfaz

`[Captura: cualquier pantalla interna completa, con la barra lateral visible y las áreas numeradas 1–4]`

1. **Barra lateral (izquierda).** Contiene el menú de módulos; la opción activa se resalta en rojo. Los cajeros ven tres: **Dashboard**, **Ventas** y **Productos**. Los administradores ven además **Predicciones** y **Usuarios**.
2. **Bloque de usuario (abajo en la barra lateral).** Muestra el nombre y el rol con los que se inició sesión, el botón para cambiar entre **modo oscuro y modo claro**, y el botón de **cerrar sesión**.
3. **Encabezado del módulo.** Título de la pantalla, una línea de contexto y los botones de acción principales de ese módulo.
4. **Área de trabajo.** Tarjetas de indicadores, gráficas, tablas y formularios del módulo.

**Convenciones de color.** El rojo señala la opción activa, las acciones principales y lo que requiere atención (stock crítico, baja demanda). El verde indica un estado favorable (stock estable, alta demanda, cuenta activa).

**Accesibilidad.** Toda la interfaz se puede recorrer con el teclado: `Tab` avanza entre elementos, `Enter` activa botones y enlaces, `Esc` cierra las ventanas emergentes. Al inicio de cada página hay un enlace "Saltar al contenido".

**Sesión.** La sesión dura 12 horas. Al vencer, el sistema regresa a la pantalla de acceso y pide entrar de nuevo. Cerrar la pestaña no cierra la sesión; para hacerlo, usar el botón de cerrar sesión.

---

## 3. Acceso al sistema

`[Captura: pantalla de inicio de sesión]`

### 3.1 Iniciar sesión

1. Abrir https://prediccionzrb.duckdns.org.
2. Escribir el **correo electrónico** y la **contraseña**.
3. Pulsar **Ingresar**.

Si los datos son incorrectos, el sistema muestra "Credenciales inválidas" sin indicar cuál de los dos falló. Si la cuenta fue desactivada por un administrador, tampoco se puede entrar aunque la contraseña sea correcta.

### 3.2 Cambiar mi contraseña (administradores)

Desde el módulo **Usuarios**:

1. Pulsar **Mi contraseña**.
2. Escribir la **contraseña actual**. Sin ella no se puede cambiar: es lo que impide que alguien con acceso momentáneo al equipo se apropie de la cuenta.
3. Escribir la **contraseña nueva** y pulsar **Cambiar contraseña**.

**Política de contraseñas.** Mínimo 10 caracteres, con al menos una letra y un número. El sistema rechaza contraseñas que no cumplan y explica por qué.

**Cajeros.** En esta versión el botón está dentro del módulo Usuarios, al que los cajeros no tienen acceso, así que **un cajero todavía no puede cambiar su propia contraseña desde la pantalla**: debe pedírselo a un administrador (sección 8.4). Está previsto mover el botón al bloque de usuario de la barra lateral para que quede disponible a todos los roles.

### 3.3 Si olvidó su contraseña

No hay recuperación por correo. Un administrador puede restablecerla desde **Usuarios** (sección 8.4). Si el que olvidó la contraseña es el único administrador, ver la sección 11.

---

## 4. Centro de control

Es la pantalla inicial. Reúne el estado comercial del día y del mes, el inventario que requiere atención y la proyección del modelo.

`[Captura: Centro de control completo, con las tarjetas numeradas 1–4]`

1. **Indicadores del periodo.** Seis tarjetas:
   - **Ventas del día** — acumulado en quetzales de hoy.
   - **Ventas del mes** — acumulado del mes en curso, con la variación porcentual respecto al mes anterior.
   - **Cantidad de ventas** — transacciones registradas en el mes.
   - **Ticket promedio** — valor medio por transacción.
   - **Productos vendidos** — unidades del mes.
   - **Stock crítico** — cuántos productos están por debajo de su mínimo.
2. **Proyección próximo mes.** Monto estimado por el modelo para los próximos 30 días. Debajo aparece "Confianza del modelo: X %" (ver la nota de la sección 7.6 sobre cómo interpretar esta cifra).
3. **Ventas reales vs. proyectadas.** Gráfica mensual que compara el historial con la proyección. Las dos series se distinguen por color y por el trazo (la proyección va punteada).
4. **Reabastecimiento.** Solo para administradores: las recomendaciones más urgentes de compra, con la cantidad sugerida y el tiempo de envío desde China. Los cajeros ven en su lugar el aviso "Disponible solo para administradores".

### 4.1 Cómo leer la variación mensual

La variación de "Ventas del mes" compara el mes en curso —**hasta hoy**— contra el mes anterior **completo**. Los primeros días de cada mes la cifra será muy negativa por esa razón; no significa que las ventas hayan caído.

---

## 5. Registro de ventas

`[Captura: módulo Ventas con la tabla y el botón Nueva venta, numerados 1–3]`

1. **Nueva venta.** Abre el formulario de registro.
2. **Historial de transacciones.** Tabla con número, fecha, cajero, productos, total y forma de pago de las últimas ventas.
3. **Bloque de usuario.** El cajero que aparece en cada venta es el que tenía la sesión abierta al registrarla.

### 5.1 Registrar una venta

1. Pulsar **Nueva venta**.
2. Pulsar **Agregar producto** por cada artículo del ticket. En cada línea, elegir el producto de la lista (muestra precio y stock disponible) e indicar la **cantidad**.
3. Elegir el **método de pago**: Efectivo, Tarjeta, Transferencia o Crédito.
4. Pulsar **Registrar venta**.

`[Captura: formulario de nueva venta con dos líneas de producto]`

Al registrar:
- El **stock de cada producto se descuenta** de inmediato.
- La venta aparece en el historial y **los indicadores del Centro de control se actualizan**.
- Queda registrado quién la hizo, a qué hora y por qué medio.

**Validaciones.** El sistema no permite registrar una venta sin productos, ni vender más unidades de las que hay en existencia. En ambos casos muestra el motivo en el propio formulario.

### 5.2 Consultar el historial

La tabla muestra las ventas más recientes primero. Cada fila lista los productos con su cantidad. Por ahora no hay búsqueda ni filtros por fecha; ver la sección 10.

---

## 6. Productos e inventario

`[Captura: módulo Productos con indicadores, filtros y tabla, numerados 1–4]`

1. **Indicadores.** Total de productos activos, cuántos están en stock crítico y cuántas categorías hay.
2. **Filtros.** **Todo** muestra el catálogo completo; **Stock bajo** solo los productos por debajo de su mínimo.
3. **Catálogo.** Producto, SKU, categoría, precio, stock actual, lead time desde China y estado (Estable / Stock bajo).
4. **Acciones.** **Recibir stock** (todos los roles) y **Nuevo producto** (solo administradores).

### 6.1 Revisar productos con stock bajo

1. Abrir **Productos**.
2. Pulsar el filtro **Stock bajo**.
3. Contrastar cada producto con la recomendación de reabastecimiento del módulo Predicciones (administradores) antes de decidir la compra.

### 6.2 Recibir stock

Se usa cuando llega mercadería.

1. Pulsar **Recibir stock**.
2. Elegir el producto y escribir la **cantidad recibida**. La nota es opcional (por ejemplo, el número del pedido).
3. Pulsar **Registrar recepción**.

El stock del producto aumenta de inmediato y el movimiento queda registrado con fecha y usuario.

`[Captura: ventana de recepción de stock]`

### 6.3 Registrar un producto nuevo (administradores)

1. Pulsar **Nuevo producto**.
2. Completar: nombre, **SKU** (debe ser único), categoría, precio, costo, stock inicial, stock mínimo y **lead time desde China en días**.
3. Pulsar **Guardar producto**.

**Sobre el lead time.** Es el tiempo que tarda un pedido en llegar desde el proveedor. El sistema lo usa para calcular cuándo hay que pedir: si la demanda prevista durante ese tiempo supera el stock disponible, genera una alerta con anticipación. El valor por defecto es 60 días; conviene ajustarlo por producto según el proveedor real.

`[Captura: formulario de nuevo producto]`

---

## 7. Pronóstico de ventas con Inteligencia Artificial

Solo administradores. Muestra lo que el modelo espera vender, qué productos cambian de tendencia y qué conviene reabastecer.

`[Captura: módulo Predicciones completo, numerado 1–5]`

1. **Volumen proyectado.** Suma en quetzales del pronóstico para el horizonte elegido.
2. **Último entrenamiento.** Algoritmo publicado y sus métricas (ver 7.4).
3. **Próximo evento.** Cuál de los tres picos de demanda de Guatemala está más cerca —diciembre, Bono 14 o la Caravana del Zorro— y cuántos días faltan.
4. **Histórico vs. pronóstico.** Gráfica con el historial reciente y la proyección hacia adelante, en trazos distintos.
5. **Señales por producto** y **Reabastecimiento** (ver 7.2 y 7.3).

### 7.1 Elegir el horizonte

Los botones **7 días**, **30 días**, **3 meses** y **6 meses** cambian cuánto se proyecta hacia adelante. Cuanto más largo el horizonte, mayor la incertidumbre: el modelo predice día a día y cada día se apoya en los anteriores, así que el error se acumula. Para decisiones de compra conviene el horizonte que coincida con el lead time del producto.

### 7.2 Señales por producto

Tarjetas con los productos cuya venta reciente subió o bajó de forma marcada respecto al periodo anterior:
- **Alta demanda** (verde): el producto está vendiendo más.
- **Baja demanda** (rojo): está vendiendo menos.

El porcentaje indica la magnitud del cambio. Son señales de lo que ya ocurrió, para revisar; no son una predicción por sí mismas.

### 7.3 Recomendaciones de reabastecimiento

Para cada producto que lo requiera: stock actual, cantidad sugerida a pedir, lead time y un nivel de urgencia (crítico, atención). El cálculo considera la demanda reciente, el tiempo de envío, un margen de seguridad y si un evento de alta demanda cae dentro de la ventana de envío.

**Validar siempre** con el inventario físico, el presupuesto y las condiciones del proveedor antes de hacer un pedido. La recomendación es un apoyo, no una orden.

### 7.4 Recalibrar el modelo

Recalibrar significa volver a entrenar el modelo con todas las ventas registradas hasta hoy. Conviene hacerlo cuando se acumulan ventas nuevas (por ejemplo, cada semana o cada mes) o después de cargar un histórico.

1. Pulsar **Recalibrar modelo**. Tarda unos segundos.
2. Al terminar, la tarjeta **Último entrenamiento** muestra el algoritmo y sus métricas.

**Qué pasa por dentro.** El sistema no entrena un solo modelo: entrena **siete candidatos** —seis métodos de referencia (naïve, naïve estacional, media móvil, suavizamiento exponencial, Holt-Winters y ARIMA) y el modelo de inteligencia artificial— y los evalúa a todos con el mismo protocolo: cinco ventanas de validación sucesivas, reentrenando en cada una. Luego aplica un criterio de publicación:

- El modelo de IA **solo reemplaza al anterior** si mejora al menos un 10 % sobre el naïve estacional, no tiene un sesgo excesivo y gana en la mayoría de las ventanas.
- Si no lo cumple, **el modelo anterior se conserva** y la tarjeta muestra `no_publicado (mejor: …)` indicando qué candidato quedó mejor. El intento queda registrado con sus métricas.

Esto garantiza que una recalibración nunca deja el sistema con un modelo peor que el que tenía.

### 7.5 Cómo leer las métricas

| Métrica | Qué mide | Cómo interpretarla |
|---|---|---|
| **MASE** | Error del modelo comparado con el de repetir la semana anterior. | **Menor es mejor.** Por debajo de 1, el modelo le gana al método simple. 0.80 significa un 20 % menos de error. |
| **WAPE** | Error absoluto total como porcentaje del volumen vendido. | Menor es mejor. Un WAPE de 44 % significa que, sumando todos los días, el pronóstico se desvió un 44 % del total real. |
| **Mejora vs. base** | Cuánto reduce el error respecto al naïve estacional. | Debe superar el 10 % para que el modelo se publique. |

### 7.6 Sobre la "Confianza del modelo" del Centro de control

La cifra "Confianza del modelo: X %" que aparece bajo la proyección se calcula como `100 − WAPE`. **No es una probabilidad ni un intervalo de confianza estadístico.** Debe leerse solo como una orientación general de qué tan lejos suele quedar el pronóstico del real. Está previsto reemplazarla por las métricas de la sección 7.5.

---

## 8. Usuarios y roles

Solo administradores. Todas las contraseñas se guardan cifradas en la base de datos; ni el sistema ni los administradores pueden ver la contraseña de nadie, solo restablecerla.

`[Captura: módulo Usuarios con la tabla y los botones de acción]`

### 8.1 Crear un usuario

1. Pulsar **Nuevo usuario**.
2. Completar nombre, correo (será su identificador para entrar), rol y contraseña inicial.
3. Pulsar **Crear usuario**.

Entregar la contraseña inicial a la persona por un medio seguro y pedirle que la cambie al primer ingreso (sección 3.2).

### 8.2 Cambiar el rol de un usuario

En la fila del usuario, pulsar **Hacer admin** o **Hacer cajero**. El cambio aplica en el siguiente inicio de sesión de esa persona.

### 8.3 Activar o desactivar una cuenta

En la fila del usuario, pulsar **Desactivar** o **Activar**. Una cuenta desactivada no puede iniciar sesión, pero su historial de ventas se conserva. Es preferible desactivar a eliminar.

### 8.4 Restablecer la contraseña de otro usuario

En la fila del usuario, pulsar **Restablecer clave**, escribir la contraseña nueva y confirmar. La contraseña anterior deja de servir de inmediato.

### 8.5 Protecciones del sistema

Para evitar quedarse sin acceso, el sistema **no permite**:
- Que un administrador se quite a sí mismo el rol de administrador.
- Que un administrador desactive su propia cuenta.
- Degradar o desactivar al **último administrador activo**.

En los tres casos muestra el motivo y no realiza el cambio.

---

## 9. Flujo recomendado de uso

**Cada día (cajero)**
1. Registrar cada venta en el momento, con todos sus productos.
2. Registrar cada recepción de mercadería cuando llegue.

**Cada semana (administrador)**
3. Revisar el Centro de control: variación del mes, stock crítico.
4. Revisar **Productos → Stock bajo** y contrastar con las recomendaciones de **Predicciones → Reabastecimiento**.
5. Revisar las señales por producto para detectar cambios de tendencia.

**Cada mes (administrador)**
6. **Recalibrar el modelo** con las ventas acumuladas.
7. Confirmar en "Último entrenamiento" que el modelo se publicó y anotar sus métricas.
8. Comparar la proyección del mes anterior con lo realmente vendido.

**Antes de un evento de temporada** (diciembre, Bono 14, Caravana)
9. Consultar "Próximo evento" y las recomendaciones de reabastecimiento con suficiente anticipación respecto al lead time de cada producto.

---

## 10. Limitaciones de esta versión

Decirlas aquí evita interpretaciones equivocadas:

- **Los datos actuales son simulados.** No se dispuso del histórico real de la empresa en esta fase. Las ventas cargadas reproducen las características del negocio (demanda intermitente, quiebres de stock, calendario guatemalteco) pero no son ventas reales. Todo indicador y toda métrica deben leerse con esa salvedad.
- **El pronóstico es del total diario en quetzales**, no por producto. Las recomendaciones de reabastecimiento usan el promedio de ventas recientes de cada producto, no el modelo de IA.
- **Con 12 meses de historial, cada evento anual aparece una sola vez.** El modelo tiende a subestimar picos que no ha visto antes en su entrenamiento.
- **La "Confianza del modelo" no es una probabilidad** (sección 7.6).
- **No hay importación de archivos** ni exportación a Excel o PDF. La carga de un histórico real está prevista para la siguiente fase.
- **No hay búsqueda ni filtros** en el historial de ventas.
- **Los cajeros no pueden cambiar su propia contraseña desde la interfaz** (sección 3.2); debe hacerlo un administrador.
- **No hay recuperación de contraseña por correo.** La restablece un administrador (8.4) o, si no queda ninguno, el administrador técnico (sección 11).

---

## 11. Recuperación de acceso (administrador técnico)

Si se pierde la contraseña del único administrador, no hay forma de recuperarla desde la interfaz. Quien administre el servidor puede hacerlo desde la línea de comandos:

```bash
ssh zorros
cd /var/www/zorros-prediccion

# Ver las cuentas registradas
docker compose exec api python -m app.manage_users listar

# Generar una contraseña nueva para una cuenta (se muestra una sola vez)
docker compose exec api python -m app.manage_users password admin@zorrosrevolution.com --generar

# Crear un administrador adicional
docker compose exec api python -m app.manage_users crear-admin correo@ejemplo.com "Nombre" --generar
```

Las contraseñas nunca se escriben como parámetro del comando: se generan al azar o se piden en pantalla sin mostrarse. Así no quedan en el historial del servidor.

---

## 12. Glosario

| Término | Definición |
|---|---|
| **Administrador** | Rol con acceso completo: productos, pronóstico, usuarios. |
| **Cajero** | Rol operativo: registra ventas y recibe stock. |
| **Demanda intermitente** | Patrón en que un producto no vende la mayoría de los días. Es el caso de casi todo el catálogo. |
| **Horizonte** | Cuántos días hacia adelante se proyecta. |
| **Lead time** | Días que tarda un pedido en llegar desde el proveedor. |
| **Línea base** | Método de referencia sencillo (por ejemplo, repetir la semana anterior). El modelo de IA solo se publica si le gana. |
| **MASE** | Error del modelo dividido entre el error de la línea base. Menor que 1 es mejor que la referencia. |
| **Naïve estacional** | Línea base que pronostica cada día con el valor del mismo día de la semana anterior. |
| **Origen móvil** | Forma de evaluar el modelo en varias ventanas de tiempo sucesivas, reentrenando en cada una, para no depender de un solo periodo. |
| **Publicar (un modelo)** | Ponerlo como modelo activo para las predicciones. Solo ocurre si supera el criterio de aceptación. |
| **Punto de reorden** | Nivel de stock a partir del cual conviene hacer un pedido, calculado con la demanda prevista durante el lead time más un margen. |
| **Recalibrar** | Reentrenar el modelo con las ventas acumuladas. |
| **SKU** | Código único de cada producto. |
| **Stock crítico / bajo** | Existencia por debajo del mínimo definido para el producto. |
| **WAPE** | Error absoluto total como porcentaje del volumen vendido. |

---

*Fin del manual, versión 0.2. Actualizar cuando se agreguen módulos o cambien los flujos.*
