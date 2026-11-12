"""
Proyecto 3 - Criptografia RSA
Curso: Matematica discreta, seccion 20
Autores: Jose Pinto y Valeria Hernandez
Modalidad: Colaborativa
Modulo: rsa_math.py
Descripcion: Modulo central con la logica matematica pura del sistema RSA.
Contiene algoritmos implementados desde cero (primalidad, MCD, inverso modular
y exponenciacion modular), funciones de validacion y las rutinas de
encriptacion y desencriptacion paso a paso.
No tiene dependencias graficas (sin tkinter).
"""


# ==============================================================================
# ALGORITMOS MATEMATICOS (IMPLEMENTADOS DESDE CERO)
# ==============================================================================

def es_primo(numero):
    """
    Comprueba si un numero entero es primo.
    Implementacion directa por division de prueba hasta la raiz cuadrada.
    """
    if numero < 2:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False
    
    # Probamos con impares desde 3 en adelante
    divisor = 3
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor = divisor + 2
        
    return True


def calcular_mcd(a, b):
    """
    Calcula el Maximo Comun Divisor (MCD) entre dos numeros
    utilizando el Algoritmo de Euclides.
    """
    while b != 0:
        residuo = a % b
        a = b
        b = residuo
    return a


def inverso_modular(e, phi):
    """
    Calcula el inverso modular d tal que:
    (e * d) = 1 (mod phi) con 1 <= d < phi
    Utiliza el Algoritmo de Euclides Extendido.
    """
    r0 = phi
    r1 = e
    t0 = 0
    t1 = 1
    
    while r1 != 0:
        cociente = r0 // r1
        
        # Actualizamos los residuos
        r_siguiente = r0 - cociente * r1
        r0 = r1
        r1 = r_siguiente
        
        # Actualizamos los coeficientes
        t_siguiente = t0 - cociente * t1
        t0 = t1
        t1 = t_siguiente
        
    # r0 es el MCD(e, phi). Si no es 1, no existe inverso
    if r0 != 1:
        return None
    
    # Ajustamos el resultado para que este en el rango [1, phi - 1]
    d = t0 % phi
    if d < 0:
        d = d + phi
        
    return d


def exponenciacion_modular(base, exponente, modulo):
    """
    Calcula (base ** exponente) % modulo usando el metodo de
    exponenciacion binaria (cuadrados repetidos), reduciendo
    modulo n en cada paso para evitar numeros gigantescos.
    """
    resultado = 1
    base = base % modulo
    
    while exponente > 0:
        # Si el bit menos significativo es 1
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
            
        base = (base * base) % modulo
        exponente = exponente // 2
        
    return resultado


# ==============================================================================
# FUNCIONES DE VALIDACION
# ==============================================================================

def validar_parametros_rsa(p_str, q_str, e_str):
    """
    Valida que p, q y e cumplan todas las condiciones matematicas exigidas:
    - Deben ser enteros.
    - p y q deben ser primos distintos.
    - 126126 < n < 1000000 donde n = p * q.
    - e > 1 y e < phi.
    - MCD(e, phi) == 1.
    Retorna una tupla: (es_valido, mensaje_error, p, q, e, n, phi)
    """
    # 1. Comprobar que sean enteros
    try:
        p = int(p_str.strip())
        q = int(q_str.strip())
        e = int(e_str.strip())
    except ValueError:
        return False, "Los valores de p, q y e deben ser numeros enteros validos.", None, None, None, None, None

    # 2. Comprobar primalidad de p y q
    if not es_primo(p):
        return False, f"El valor p = {p} no es un numero primo.", None, None, None, None, None

    if not es_primo(q):
        return False, f"El valor q = {q} no es un numero primo.", None, None, None, None, None

    # 3. Comprobar que p y q sean distintos
    if p == q:
        return False, "Los numeros primos p y q deben ser distintos entre si.", None, None, None, None, None

    # 4. Calcular n y phi
    n = p * q
    phi = (p - 1) * (q - 1)

    # 5. Comprobar limites de n (126126 < n < 1000000)
    if n <= 126126:
        return False, f"El modulo n = p * q = {n} debe ser mayor que 126126 para admitir cualquier pareja de caracteres.", None, None, None, None, None

    if n >= 1000000:
        return False, f"El modulo n = p * q = {n} debe ser menor que 1000000 para que cada bloque cifrado tenga seis digitos.", None, None, None, None, None

    # 6. Comprobar exponente e
    if e <= 1:
        return False, f"El exponente e = {e} debe ser estrictamente mayor a 1.", None, None, None, None, None

    if e >= phi:
        return False, f"El exponente e = {e} debe ser menor que phi = {phi}.", None, None, None, None, None

    mcd = calcular_mcd(e, phi)
    if mcd != 1:
        return False, f"El exponente e = {e} no es coprimo con phi = {phi} (MCD = {mcd}).", None, None, None, None, None

    return True, "", p, q, e, n, phi


def validar_mensaje_original(mensaje):
    """
    Valida el mensaje original:
    - No puede ser vacio.
    - Cada caracter debe estar dentro del rango ASCII imprimible [32, 126].
    Retorna (es_valido, mensaje_error).
    """
    if len(mensaje) == 0:
        return False, "El mensaje a encriptar no puede estar vacio."

    for indice in range(len(mensaje)):
        caracter = mensaje[indice]
        codigo = ord(caracter)
        if codigo < 32 or codigo > 126:
            return False, f"El caracter '{caracter}' (posicion {indice + 1}, ASCII {codigo}) no es admitido. Solo se admiten caracteres ASCII imprimibles entre 32 y 126."

    return True, ""


def validar_cifrado_y_longitud(cifrado_str, longitud_str, n):
    """
    Valida el texto cifrado C y la longitud original L para desencriptar:
    - Longitud L debe ser un entero positivo.
    - C debe contener bloques de exactamente 6 digitos separados por espacios.
    - Cada bloque c debe cumplir 0 <= c < n.
    - Si hay k bloques, L debe ser 2k (sin relleno) o 2k - 1 (con relleno).
    Retorna (es_valido, mensaje_error, lista_bloques_int, L)
    """
    # 1. Validar longitud L
    try:
        L = int(longitud_str.strip())
        if L <= 0:
            return False, "La longitud original L debe ser un entero mayor a 0.", None, None
    except ValueError:
        return False, "La longitud original L debe ser un numero entero valido.", None, None

    # 2. Validar formato de C
    bloques_texto = cifrado_str.strip().split()
    if len(bloques_texto) == 0:
        return False, "El mensaje cifrado C no puede estar vacio.", None, None

    k = len(bloques_texto)

    # 3. Validar coherencia de L con la cantidad de bloques k
    if L != (2 * k) and L != (2 * k - 1):
        return False, f"La longitud L = {L} no es coherente con los k = {k} bloques cifrados. Debe ser exactamente {2 * k} (sin relleno) o {2 * k - 1} (con relleno).", None, None

    # 4. Validar cada bloque
    lista_bloques_int = []
    for b in bloques_texto:
        if len(b) != 6 or not b.isdigit():
            return False, f"El bloque cifrado '{b}' es invalido. Cada bloque debe contener exactamente 6 digitos decimales (0-9).", None, None
        
        valor_c = int(b)
        if valor_c < 0 or valor_c >= n:
            return False, f"El bloque '{b}' tiene valor {valor_c}, el cual no cumple la condicion 0 <= c < n ({n}).", None, None
            
        lista_bloques_int.append(valor_c)

    return True, "", lista_bloques_int, L


# ==============================================================================
# LOGICA DE ENCRIPTACION Y DESENCRIPTACION
# ==============================================================================

def ejecutar_encriptacion(mensaje, p, q, e, n, phi):
    """
    Realiza el proceso completo de encriptacion RSA:
    - Calcula L.
    - Aplica relleno si L es impar agregando un espacio (ASCII 32).
    - Agrupa en parejas de caracteres y crea bloques numericos m de 6 digitos.
    - Cifra cada bloque: c = m^e mod n.
    - Genera el reporte paso a paso y la salida final.
    """
    L = len(mensaje)
    mensaje_procesado = mensaje
    se_uso_relleno = False

    if L % 2 != 0:
        mensaje_procesado = mensaje + " "
        se_uso_relleno = True

    # Agrupamos en bloques de 2 caracteres
    detalles_bloques = []
    bloques_cifrados = []

    for i in range(0, len(mensaje_procesado), 2):
        char1 = mensaje_procesado[i]
        char2 = mensaje_procesado[i + 1]

        ascii1 = ord(char1)
        ascii2 = ord(char2)

        # Formato de 3 digitos para cada caracter
        ascii1_str = f"{ascii1:03d}"
        ascii2_str = f"{ascii2:03d}"

        # Bloque numerico de 6 digitos
        bloque_m_str = ascii1_str + ascii2_str
        m_num = int(bloque_m_str)

        # Cifrado con exponenciacion modular propia
        c_num = exponenciacion_modular(m_num, e, n)
        c_str = f"{c_num:06d}"

        bloques_cifrados.append(c_str)

        detalles_bloques.append({
            "par": f"'{char1}' y '{char2}'",
            "ascii1": ascii1_str,
            "ascii2": ascii2_str,
            "m_str": bloque_m_str,
            "m_num": m_num,
            "c_str": c_str,
            "c_num": c_num
        })

    cifrado_final = " ".join(bloques_cifrados)

    # Construimos el texto del resumen detallado
    lineas = []
    lineas.append("=" * 64)
    lineas.append("           RESUMEN DEL PROCESO DE ENCRIPTACION")
    lineas.append("=" * 64)
    lineas.append(f"Parametro p: {p}")
    lineas.append(f"Parametro q: {q}")
    lineas.append(f"Modulo n = p * q: {n}")
    lineas.append(f"Funcion de Euler phi = (p - 1) * (q - 1): {phi}")
    lineas.append(f"Exponente publico e: {e}")
    lineas.append(f"MCD(e, phi) = {calcular_mcd(e, phi)} (primos relativos)")
    lineas.append(f"Llave publica (e, n): ({e}, {n})")
    lineas.append("-" * 64)
    lineas.append(f"Mensaje original: \"{mensaje}\"")
    lineas.append(f"Longitud original (L): {L}")
    if se_uso_relleno:
        lineas.append(f"Relleno aplicado: SI (L es impar, se agrego un espacio al final)")
        lineas.append(f"Mensaje con relleno: \"{mensaje_procesado}\" (Longitud: {len(mensaje_procesado)})")
    else:
        lineas.append("Relleno aplicado: NO (L es par, no se requirio relleno)")
    lineas.append("-" * 64)
    lineas.append("DETALLE DE BLOQUES:")

    bloque_idx = 1
    for b in detalles_bloques:
        lineas.append(f"\nBloque #{bloque_idx}:")
        lineas.append(f"  Caracteres: {b['par']}")
        lineas.append(f"  Conversion a ASCII: {b['ascii1']} + {b['ascii2']} -> \"{b['m_str']}\"")
        lineas.append(f"  Bloque numerico (m): {b['m_num']}")
        lineas.append(f"  Operacion modular: c = {b['m_num']}^{e} mod {n}")
        lineas.append(f"  Bloque cifrado (c): {b['c_str']}")
        bloque_idx = bloque_idx + 1

    lineas.append("\n" + "=" * 64)
    lineas.append("RESULTADOS:")
    lineas.append(f"  Cifrado C: {cifrado_final}")
    lineas.append(f"  Longitud original L: {L}")
    lineas.append(f"  Llave publica: ({e}, {n})")
    lineas.append("=" * 64)

    resumen_texto = "\n".join(lineas)
    return cifrado_final, L, resumen_texto


def ejecutar_desencriptacion(bloques_c_int, L, p, q, e, n, phi):
    """
    Realiza el proceso completo de desencriptacion RSA:
    - Calcula el inverso modular d.
    - Descifra cada bloque: m = c^d mod n.
    - Convierte cada m a 6 digitos y extrae los 2 caracteres ASCII.
    - Si L es impar, verifica y retira el ultimo espacio de relleno.
    - Genera el reporte paso a paso y el mensaje recuperado.
    Retorna (mensaje_recuperado, d, resumen_texto, error)
    """
    d = inverso_modular(e, phi)
    if d is None:
        return None, None, None, f"No se pudo calcular el inverso modular de e = {e} modulo phi = {phi}."

    detalles_bloques = []
    texto_recuperado_con_relleno = ""

    bloque_idx = 1
    for c_num in bloques_c_int:
        c_str = f"{c_num:06d}"

        # Descifrado con exponenciacion modular propia
        m_num = exponenciacion_modular(c_num, d, n)
        m_str = f"{m_num:06d}"

        # Extraemos los dos codigos ASCII
        ascii1_str = m_str[0:3]
        ascii2_str = m_str[3:6]

        ascii1 = int(ascii1_str)
        ascii2 = int(ascii2_str)

        # Validamos que los codigos ASCII esten en el rango valido [32, 126]
        if ascii1 < 32 or ascii1 > 126:
            return None, d, None, f"El bloque {bloque_idx} descifrado produjo el codigo ASCII {ascii1}, fuera del rango permitido [32, 126]."

        if ascii2 < 32 or ascii2 > 126:
            return None, d, None, f"El bloque {bloque_idx} descifrado produjo el codigo ASCII {ascii2}, fuera del rango permitido [32, 126]."

        char1 = chr(ascii1)
        char2 = chr(ascii2)

        texto_recuperado_con_relleno = texto_recuperado_con_relleno + char1 + char2

        detalles_bloques.append({
            "idx": bloque_idx,
            "c_str": c_str,
            "c_num": c_num,
            "m_num": m_num,
            "m_str": m_str,
            "ascii1": ascii1_str,
            "ascii2": ascii2_str,
            "char1": char1,
            "char2": char2
        })
        bloque_idx = bloque_idx + 1

    # Verificacion y retiro del relleno
    se_uso_relleno = (L % 2 != 0)
    mensaje_final = texto_recuperado_con_relleno

    if se_uso_relleno:
        # El ultimo caracter debe ser exactamente un espacio (ASCII 32)
        if len(texto_recuperado_con_relleno) == 0 or texto_recuperado_con_relleno[-1] != " ":
            return None, d, None, "Se esperaba un espacio (ASCII 32) como caracter de relleno al final, pero no se encontro."
        # Retiramos unicamente el ultimo espacio
        mensaje_final = texto_recuperado_con_relleno[:-1]

    # Construimos el resumen detallado
    lineas = []
    lineas.append("=" * 64)
    lineas.append("          RESUMEN DEL PROCESO DE DESENCRIPTACION")
    lineas.append("=" * 64)
    lineas.append(f"Parametro p: {p}")
    lineas.append(f"Parametro q: {q}")
    lineas.append(f"Modulo n = p * q: {n}")
    lineas.append(f"Funcion de Euler phi = (p - 1) * (q - 1): {phi}")
    lineas.append(f"Exponente publico e: {e}")
    lineas.append(f"Exponente privado d (inverso de e mod phi): {d}")
    lineas.append(f"Llave privada (d, n): ({d}, {n})")
    lineas.append("-" * 64)
    lineas.append(f"Cantidad de bloques cifrados: {len(bloques_c_int)}")
    lineas.append(f"Longitud original esperada (L): {L}")
    if se_uso_relleno:
        lineas.append("Relleno detectado: SI (L es impar, se retirara el espacio final)")
    else:
        lineas.append("Relleno detectado: NO (L es par, no se retira ningun caracter)")
    lineas.append("-" * 64)
    lineas.append("DETALLE DE DESCIFRADO DE BLOQUES:")

    for b in detalles_bloques:
        lineas.append(f"\nBloque #{b['idx']}:")
        lineas.append(f"  Bloque cifrado (c): {b['c_str']}")
        lineas.append(f"  Operacion modular: m = {b['c_num']}^{d} mod {n}")
        lineas.append(f"  Bloque numerico recuperado (m): {b['m_str']}")
        lineas.append(f"  Separacion ASCII: {b['ascii1']} ('{b['char1']}') y {b['ascii2']} ('{b['char2']}')")
        lineas.append(f"  Texto obtenido: \"{b['char1']}{b['char2']}\"")

    lineas.append("\n" + "-" * 64)
    lineas.append(f"Texto antes de retirar relleno: \"{texto_recuperado_con_relleno}\"")
    if se_uso_relleno:
        lineas.append("Accion sobre el relleno: Se retiro exactamente el ultimo caracter (espacio).")
    else:
        lineas.append("Accion sobre el relleno: Ninguna (longitud par).")
    lineas.append("=" * 64)
    lineas.append("RESULTADOS:")
    lineas.append(f"  Exponente privado d: {d}")
    lineas.append(f"  Mensaje original recuperado (M): \"{mensaje_final}\"")
    lineas.append("=" * 64)

    resumen_texto = "\n".join(lineas)
    return mensaje_final, d, resumen_texto, None
