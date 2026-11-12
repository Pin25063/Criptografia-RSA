# Proyecto 3 - Criptografía RSA

**Curso:** Matemática Discreta, sección 20  
**Autores:** Jose Pinto y Valeria Hernandez  
**Modalidad:** Colaborativa  
**Versión de Python recomendada:** Python 3.8 o superior (probado en Python 3.10+)  

---

## 1. Descripción del Proyecto

Este proyecto consiste en una aplicación de escritorio desarrollada en Python con la biblioteca gráfica estándar **Tkinter**, la cual permite **encriptar** y **desencriptar** mensajes de texto mediante el algoritmo de clave pública **RSA**.

El sistema aplica el principio de **separación de responsabilidades** organizando el código en tres módulos funcionales y bien definidos:
1. **`rsa_math.py`**: Módulo que concentra la lógica matemática y algorítmica pura, construido sin librerías externas ni dependencias gráficas.
2. **`rsa_gui.py`**: Módulo responsable exclusivamente de la presentación visual y la interacción con el usuario mediante Tkinter.
3. **`main.py`**: Módulo disparador y punto de entrada principal del programa.

El programa implementa desde cero y de forma artesanal (sin usar librerías externas ni funciones avanzadas como `math.gcd`, `pow()` con 3 argumentos o bibliotecas criptográficas) todos los algoritmos matemáticos requeridos:
- Comprobación de primalidad de los números $p$ y $q$.
- Cálculo del Máximo Común Divisor (MCD) mediante el algoritmo de Euclides.
- Cálculo del inverso modular mediante el algoritmo de Euclides extendido.
- Exponenciación modular reduciendo el módulo $n$ paso a paso.

---

## 2. Estructura Modular del Código

El proyecto fue refactorizado siguiendo una arquitectura modular limpia y funcional (sin clases innecesarias), facilitando su mantenimiento y lectura:

```text
Proyecto3/
├── rsa_math.py         # Lógica central: algoritmos matemáticos, validaciones y encriptación/desencriptación pura
├── rsa_gui.py          # Interfaz gráfica: construcción de ventanas, eventos y componentes de Tkinter
├── main.py             # Punto de entrada principal (launcher de la aplicación)
├── requirements.txt    # Información de dependencias (solo librería estándar)
└── README.md           # Documentación completa del proyecto
```

### Detalle de cada módulo:

- **`rsa_math.py` (Lógica Central y Matemática Pura):**
  - Implementa las operaciones matemáticas: `es_primo`, `calcular_mcd`, `inverso_modular` y `exponenciacion_modular`.
  - Contiene las validaciones matemáticas y de formato: `validar_parametros_rsa`, `validar_mensaje_original` y `validar_cifrado_y_longitud`.
  - Aloja la lógica completa de los procesos criptográficos: `ejecutar_encriptacion` y `ejecutar_desencriptacion`.
  - **No** posee importaciones ni dependencias de `tkinter`, lo que permite probar la lógica de forma totalmente aislada.

- **`rsa_gui.py` (Interfaz Gráfica de Usuario):**
  - Construye la ventana principal, el encabezado, las pestañas (`ttk.Notebook`), cuadros de texto, botones y campos de entrada.
  - Importa `rsa_math` localmente para invocar las validaciones y cálculos al presionar los botones "🔐 Encriptar" y "🔓 Desencriptar".
  - Gestiona la visualización de resultados y resúmenes detallados paso a paso.
  - Ofrece la función `iniciar_interfaz()` para iniciar el bucle de eventos (`mainloop`).

- **`main.py` (Disparador Principal):**
  - Actúa como el punto de inicio de la aplicación.
  - Su única responsabilidad es importar `iniciar_interfaz` desde `rsa_gui.py` y ejecutarla dentro de la cláusula estándar `if __name__ == "__main__":`.

---

## 3. Instrucciones Rápidas de Ejecución

### Requisitos previos
- Disponer de Python instalado (versión 3.8 o superior).
- El sistema utiliza exclusivamente la **biblioteca estándar de Python** (`tkinter`), por lo que **no** requiere instalar paquetes externos mediante `pip`.

### Ejecución
Abre una terminal o consola de comandos en la carpeta del proyecto y ejecuta:

```bash
python main.py
```

Se abrirá automáticamente la interfaz gráfica del sistema RSA.

---

## 4. Funciones que Implementan los Algoritmos Matemáticos

Todas las funciones matemáticas se encuentran en el módulo [rsa_math.py](rsa_math.py) y están construidas con aritmética básica:

1. **`es_primo(numero)`:**
   - Comprueba si un número entero es primo.
   - Descarta casos menores a 2 y pares mayores a 2.
   - Emplea divisiones de prueba únicamente con números impares hasta la raíz cuadrada del número ($\sqrt{n}$) mediante un ciclo `while`.

2. **`calcular_mcd(a, b)`:**
   - Implementa el **Algoritmo de Euclides clásico**.
   - Calcula el residuo iterativo `a % b` hasta que `b` sea cero, retornando el último residuo no nulo que corresponde al Máximo Común Divisor.

3. **`inverso_modular(e, phi)`:**
   - Implementa el **Algoritmo de Euclides Extendido**.
   - Calcula los coeficientes de Bézout para resolver la ecuación $e \cdot d + \varphi \cdot y = \text{MCD}(e, \varphi)$.
   - Si $\text{MCD}(e, \varphi) = 1$, ajusta y devuelve el representante $d$ que cumple $1 \le d < \varphi$ tal que $(e \cdot d) \equiv 1 \pmod \varphi$.

4. **`exponenciacion_modular(base, exponente, modulo)`:**
   - Implementa el método de **exponenciación binaria** (cuadrados repetidos).
   - En cada iteración evalúa el bit menos significativo del exponente (`exponente % 2 == 1`), multiplica y reduce inmediatamente con `% modulo`. Luego eleva la base al cuadrado (`(base * base) % modulo`) y divide el exponente entre 2 (`exponente // 2`).
   - Esto evita calcular números astronómicos en memoria y garantiza alta velocidad y precisión.

---

## 5. Funcionamiento del Sistema RSA

### A. Relleno (Padding)
- Cada carácter permitido (ASCII del 32 al 126) se representa con **3 dígitos decimales** (ejemplo: `'A'` $\rightarrow$ `065`).
- El texto se agrupa en parejas de 2 caracteres, formando **bloques numéricos $m$ de 6 dígitos**.
- Si la longitud original del mensaje ($L$) es **impar**, se añade exactamente **un espacio** (`ASCII 032`) al final del mensaje como relleno antes de dividirlo en bloques.
- Durante la desencriptación: si la longitud $L$ ingresada es impar, el programa comprueba que el último carácter recuperado sea un espacio y retira **únicamente** ese carácter final, preservando íntegros todos los espacios originales del mensaje (al inicio, intermedios o al final).

### B. Encriptación
1. Se valida que $p$ y $q$ sean primos distintos y que $126126 < n < 1000000$.
2. Se valida que $e > 1$, $e < \varphi$ y $\text{MCD}(e, \varphi) = 1$.
3. Se verifica que todos los caracteres de $M$ pertenezcan al rango ASCII $[32, 126]$.
4. Se calcula $L = \text{len}(M)$ y se añade relleno si es necesario.
5. Para cada bloque $m$, se calcula $c \equiv m^e \pmod n$.
6. Cada $c$ se formatea con **exactamente 6 dígitos decimales** (con ceros a la izquierda si hiciera falta) y se separan por un espacio.
7. **Salidas en la GUI:**
   - En el cuadro de **Resultados de Salida** se muestran el cifrado $C$, la longitud original $L$ y la llave pública $(e, n)$.
   - En el panel inferior **Resumen Detallado del Proceso** se muestra el desglose completo: valores de $n$, $\varphi$, verificación del MCD, longitud $L$, aplicación de relleno, códigos ASCII de cada carácter, bloques $m$, fórmula aplicada y bloques resultantes $c$.
   - Se incluye un botón **"➡️ Enviar a Desencriptar"** que transfiere automáticamente $C$, $L$, $p$, $q$ y $e$ a la pestaña de desencriptación.

### C. Desencriptación
1. Se ingresan $C$, $L$, $p$, $q$ y $e$.
2. Se validan los parámetros RSA ($p, q, e$) y se calculan $n$ y $\varphi$.
3. Se valida el formato de $C$: bloques de exactamente 6 dígitos decimales y que cumplan $0 \le c < n$.
4. Se valida la coherencia de $L$: si $C$ tiene $k$ bloques, $L$ debe ser estrictamente $2k$ (longitud par, sin relleno) o $2k - 1$ (longitud impar, con relleno).
5. Se calcula la llave privada $d = \text{inverso\_modular}(e, \varphi)$.
6. Para cada bloque $c$, se calcula $m \equiv c^d \pmod n$.
7. Se divide cada $m$ en dos códigos de 3 dígitos, se verifica que ambos estén en $[32, 126]$ y se convierten a caracteres con `chr()`.
8. Si $L$ es impar, se comprueba y retira el último espacio de relleno.
9. **Salidas en la GUI:**
   - En el cuadro de resultados se muestran el exponente privado $d$ y el mensaje original recuperado $M$.
   - En el panel inferior se detalla el proceso bloque a bloque.

---

## 6. Ejemplo de Referencia (del Documento Oficial)

| Dato | Valor |
| :--- | :--- |
| **Mensaje original ($M$)** | `"RSA"` |
| **Entradas RSA** | $p = 367$, $q = 373$, $e = 17$ |
| **Valores calculados** | $n = 136891$, $\varphi = 136152$, $\text{MCD}(e, \varphi) = 1$ |
| **Longitud y relleno** | $L = 3$; mensaje con relleno: `"RSA "` (4 caracteres) |
| **Bloques del mensaje ($m$)** | `082083 065032` (valores: $82083$ y $65032$) |
| **Cifrado ($C$)** | `026054 123875` (nótese el cero inicial en el primer bloque) |
| **Exponente privado ($d$)** | $d = 8009$ |
| **Mensaje recuperado** | `"RSA"` |

> Ambos botones **"💡 Cargar Ejemplo de Referencia"** en la interfaz permiten cargar este caso de prueba con un solo clic para verificar el funcionamiento inmediato.

---

## 7. Comprobaciones y Pruebas Realizadas

Se implementaron y ejecutaron pruebas exhaustivas de validación y funcionamiento:

1. **Mensajes de longitud par e impar:**
   - Longitud impar: `"RSA"` ($L=3$), `"A"` ($L=1$), `"Hola mundo!"` ($L=11$) $\rightarrow$ Se agregó y retiró el relleno correctamente.
   - Longitud par: `"1234"` ($L=4$), `"  Espacios  "` ($L=12$) $\rightarrow$ No se alteraron los caracteres.

2. **Tipos de caracteres admitidos:**
   - Mayúsculas y minúsculas: `"Texto Mixto"`.
   - Números y dígitos: `"2026"`, `"1234567890"`.
   - Signos de puntuación y símbolos permitidos: `"!#$%&'()*+,-./:;<=>?@[]^_{|}~"`.
   - Espacios consecutivos e iniciales/finales: `"  inicio y fin  "`, `"A  B"` $\rightarrow$ Se preservaron exactamente sin usar funciones destructivas como `strip()`.

3. **Ceros a la izquierda:**
   - Bloques cifrados con cero inicial como `026054` conservan fielmente sus 6 dígitos decimales.

4. **Validaciones y rechazo de errores (sin cierres inesperados):**
   - Parámetros no enteros: Produce mensaje de error comprensible.
   - Parámetros no primos ($p=368$ o $q=374$): Rechazados con aviso explícito.
   - Primos iguales ($p=q$): Rechazados.
   - Módulo $n \le 126126$ o $n \ge 1000000$: Rechazados por estar fuera del rango permitido.
   - Exponente $e \le 1$ o no coprimo con $\varphi$ ($\text{MCD} \neq 1$): Rechazados.
   - Caracteres fuera del rango ASCII $[32, 126]$ (ej. tildes, `ñ`, saltos de línea): Rechazados indicando la posición y el carácter inválido.
   - Mensaje o cifrado vacío: Rechazados.
   - Bloques cifrados que no tengan exactamente 6 dígitos o contengan letras: Rechazados.
   - Bloques con valor $c \ge n$: Rechazados.
   - Incoherencia de longitud $L$ respecto a los $k$ bloques ($L \ne 2k$ y $L \ne 2k-1$): Rechazados.
