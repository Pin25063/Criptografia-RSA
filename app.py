"""Adaptación a interfaz web
"""
from flask import Flask, jsonify, render_template_string, request

import rsa_math


app = Flask(__name__)
app.json.ensure_ascii = False


def leer_campos(nombres):
    """Comprueba el formato HTTP; las validaciones RSA siguen en rsa_math."""
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return None, "La solicitud debe contener un objeto JSON."
    for nombre in nombres:
        if not isinstance(datos.get(nombre), str):
            return None, f"El campo {nombre} debe enviarse como texto."
    return datos, None


@app.after_request
def evitar_cache_de_resultados(respuesta):
    if request.path.startswith("/api/"):
        respuesta.headers["Cache-Control"] = "no-store"
    return respuesta


@app.get("/")
def inicio():
    return render_template_string(PAGINA_HTML)


@app.get("/health")
def salud():
    return jsonify(estado="ok")


@app.post("/api/cifrar")
def cifrar():
    datos, error = leer_campos(("mensaje", "p", "q", "e"))
    if error:
        return jsonify(error=error), 400

    valido, error = rsa_math.validar_mensaje_original(datos["mensaje"])
    if not valido:
        return jsonify(error=error), 400

    valido, error, p, q, e, n, phi = rsa_math.validar_parametros_rsa(
        datos["p"], datos["q"], datos["e"]
    )
    if not valido:
        return jsonify(error=error), 400

    cifrado, longitud, resumen = rsa_math.ejecutar_encriptacion(
        datos["mensaje"], p, q, e, n, phi
    )
    return jsonify(
        cifrado=cifrado,
        longitud=longitud,
        parametros={"p": p, "q": q, "e": e, "n": n},
        resumen=resumen,
    )


@app.post("/api/descifrar")
def descifrar():
    datos, error = leer_campos(("cifrado", "longitud", "p", "q", "e"))
    if error:
        return jsonify(error=error), 400

    valido, error, p, q, e, n, phi = rsa_math.validar_parametros_rsa(
        datos["p"], datos["q"], datos["e"]
    )
    if not valido:
        return jsonify(error=error), 400

    try:
        valido, error, bloques, longitud = rsa_math.validar_cifrado_y_longitud(
            datos["cifrado"], datos["longitud"], n
        )
    except ValueError:
        # Algunos simbolos numericos Unicode no se pueden convertir con int().
        # El aviso pertenece a la interfaz; no se modifica la funcion original.
        return jsonify(error="El cifrado debe contener digitos del 0 al 9 separados por espacios."), 400
    if not valido:
        return jsonify(error=error), 400

    mensaje, d, resumen, error = rsa_math.ejecutar_desencriptacion(
        bloques, longitud, p, q, e, n, phi
    )
    if error is not None:
        return jsonify(error=error), 400
    return jsonify(mensaje=mensaje, d=d, resumen=resumen)


PAGINA_HTML = r'''
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Proyecto 3 - Criptografia RSA | Matematica Discreta</title>
  <style>
    * { box-sizing: border-box; }
    [hidden] { display: none !important; }
    body { margin: 0; background: #f0f0f0; color: #000; font: 12px "Segoe UI", Arial, sans-serif; }
    .ventana { width: 820px; max-width: 100%; min-width: 750px; height: 720px; min-height: 620px; display: flex; flex-direction: column; margin: 0 auto; }
    header { background: #1e3a8a; padding: 10px; text-align: center; flex: none; }
    h1 { color: white; font: bold 20px Helvetica, Arial, sans-serif; margin: 0 0 3px; }
    header p { color: #e0e7ff; font: 13px Helvetica, Arial, sans-serif; margin: 0; }
    .cuaderno { display: flex; flex-direction: column; flex: 1; min-height: 0; margin: 10px; }
    .pestanas { display: flex; align-items: end; height: 28px; padding-left: 2px; }
    .pestana { border: 1px solid #adadad; border-bottom: 0; border-radius: 3px 3px 0 0; padding: 5px 12px; background: #e5e5e5; color: #000; }
    .pestana[aria-selected="true"] { background: #f0f0f0; padding-top: 7px; position: relative; top: 1px; }
    .panel { display: flex; flex-direction: column; flex: 1; min-height: 0; border: 1px solid #adadad; padding: 4px 0; }
    fieldset { margin: 5px 10px; border: 1px solid #c0c0c0; padding: 10px; min-width: 0; }
    legend { padding: 0 4px; }
    form { margin: 0; }
    .entradas { display: grid; grid-template-columns: max-content minmax(100px, 1fr) max-content 86px max-content 86px; align-items: center; gap: 6px 5px; }
    label { white-space: nowrap; }
    input, textarea, button { font: inherit; }
    input { min-width: 0; width: 100%; height: 23px; border: 1px solid #8c8c8c; border-radius: 0; padding: 1px 3px; background: white; color: #000; }
    input[readonly] { background: #f0f0f0; }
    .ancho { grid-column: 2 / 7; }
    .numero { width: 86px; justify-self: start; }
    .botones { grid-column: 1 / 7; display: flex; gap: 10px; padding: 5px; margin-top: 2px; }
    button { cursor: pointer; color: #000; background: linear-gradient(#fafafa, #e5e5e5); border: 1px solid #adadad; border-radius: 2px; padding: 4px 10px; white-space: nowrap; }
    button:hover { border-color: #0078d7; background: #e5f1fb; }
    button:focus-visible, input:focus-visible, textarea:focus-visible { outline: 2px solid #0078d7; outline-offset: 1px; }
    button:disabled { cursor: wait; opacity: .65; }
    .encriptar, .desencriptar { color: white; font: bold 13px Helvetica, Arial, sans-serif; padding: 4px 14px; border: 1px solid #888; border-radius: 0; }
    .encriptar, .encriptar:hover { background: #2563eb; }
    .desencriptar, .desencriptar:hover { background: #059669; }
    .salida { padding: 8px; margin-top: 3px; margin-bottom: 3px; }
    .salida label { font-size: 12px; font-weight: bold; }
    .salida input, output { font: 13px Consolas, monospace; }
    .salida-enc { display: grid; grid-template-columns: max-content minmax(100px, 1fr) max-content max-content max-content max-content; align-items: center; gap: 5px; }
    .enviar { grid-column: 1 / 7; justify-self: end; margin-top: 3px; }
    .salida-des { display: grid; grid-template-columns: max-content 115px max-content minmax(120px, 1fr); align-items: center; gap: 5px; }
    #res-mensaje { font-weight: bold; }
    .detalle { flex: 1; min-height: 0; display: flex; padding: 8px; }
    .detalle textarea { flex: 1; width: 100%; min-height: 0; resize: none; overflow-y: scroll; border: 1px solid #888; background: white; color: #000; font: 12px Consolas, monospace; padding: 3px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <main class="ventana">
    <header>
      <h1>Criptografia RSA - Matematica Discreta 1</h1>
      <p>Jose Pinto y Valeria Hernandez | Seccion 20</p>
    </header>
    <div class="cuaderno">
      <div class="pestanas" role="tablist" aria-label="Operacion">
        <button class="pestana" id="tab-enc" role="tab" aria-selected="true" aria-controls="panel-enc" type="button">Encriptar Mensaje</button>
        <button class="pestana" id="tab-des" role="tab" aria-selected="false" aria-controls="panel-des" tabindex="-1" type="button">Desencriptar Mensaje</button>
      </div>
      <section class="panel" id="panel-enc" role="tabpanel" aria-labelledby="tab-enc">
        <form id="form-enc">
          <fieldset><legend>Entradas de Encriptacion</legend>
            <div class="entradas">
              <label for="enc-mensaje">Mensaje original (M):</label><input class="ancho" id="enc-mensaje" name="mensaje" value="RSA" autocomplete="off" spellcheck="false">
              <label for="enc-p">Primo p:</label><input class="numero" id="enc-p" name="p" value="367" autocomplete="off">
              <label for="enc-q">Primo q:</label><input class="numero" id="enc-q" name="q" value="373" autocomplete="off">
              <label for="enc-e">Exponente e:</label><input class="numero" id="enc-e" name="e" value="17" autocomplete="off">
              <div class="botones">
                <button class="encriptar" type="submit">Encriptar</button>
                <button type="button" data-ejemplo="enc">Cargar Ejemplo de Referencia</button>
                <button type="button" data-limpiar="enc">Limpiar</button>
              </div>
            </div>
          </fieldset>
        </form>
        <fieldset class="salida"><legend>Resultados de Salida</legend>
          <div class="salida-enc">
            <label for="res-cifrado">Cifrado (C):</label><input id="res-cifrado" readonly>
            <label for="res-longitud">Longitud (L):</label><output id="res-longitud">-</output>
            <label for="res-publica">Llave Publica (e, n):</label><output id="res-publica">-</output>
            <button class="enviar" id="enviar" type="button">Enviar a Desencriptar</button>
          </div>
        </fieldset>
        <fieldset class="detalle"><legend>Resumen Detallado del Proceso</legend>
          <textarea id="resumen-enc" aria-label="Resumen Detallado del Proceso de Encriptacion" spellcheck="false"></textarea>
        </fieldset>
      </section>
      <section class="panel" id="panel-des" role="tabpanel" aria-labelledby="tab-des" hidden>
        <form id="form-des">
          <fieldset><legend>Entradas de Desencriptacion</legend>
            <div class="entradas">
              <label for="des-cifrado">Cifrado (C):</label><input class="ancho" id="des-cifrado" name="cifrado" autocomplete="off" spellcheck="false">
              <label for="des-longitud">Longitud (L):</label><input class="numero" id="des-longitud" name="longitud" autocomplete="off">
              <label for="des-p">Primo p:</label><input class="numero" id="des-p" name="p" autocomplete="off">
              <label for="des-q">Primo q:</label><input class="numero" id="des-q" name="q" autocomplete="off">
              <label for="des-e">Exponente e:</label><input class="numero" id="des-e" name="e" autocomplete="off">
              <div class="botones">
                <button class="desencriptar" type="submit">Desencriptar</button>
                <button type="button" data-ejemplo="des">Cargar Ejemplo de Referencia</button>
                <button type="button" data-limpiar="des">Limpiar</button>
              </div>
            </div>
          </fieldset>
        </form>
        <fieldset class="salida"><legend>Resultados de Salida</legend>
          <div class="salida-des">
            <label for="res-d">Exponente Privado (d):</label><input id="res-d" readonly>
            <label for="res-mensaje">Mensaje Recuperado (M):</label><input id="res-mensaje" readonly>
          </div>
        </fieldset>
        <fieldset class="detalle"><legend>Resumen Detallado del Proceso</legend>
          <textarea id="resumen-des" aria-label="Resumen Detallado del Proceso de Desencriptacion" spellcheck="false"></textarea>
        </fieldset>
      </section>
    </div>
  </main>
  <script>
    "use strict";
    const porId = (id) => document.getElementById(id);
    const ejemplos = {
      enc: { mensaje: "RSA", p: "367", q: "373", e: "17" },
      des: { cifrado: "026054 123875", longitud: "3", p: "367", q: "373", e: "17" }
    };

    function seleccionar(nombre, enfocar = false) {
      for (const prefijo of ["enc", "des"]) {
        const activa = prefijo === nombre;
        porId(`tab-${prefijo}`).setAttribute("aria-selected", String(activa));
        porId(`tab-${prefijo}`).tabIndex = activa ? 0 : -1;
        porId(`panel-${prefijo}`).hidden = !activa;
      }
      if (enfocar) porId(`tab-${nombre}`).focus();
    }

    function rellenar(prefijo, valores) {
      for (const campo of porId(`form-${prefijo}`).querySelectorAll("[name]")) {
        campo.value = valores[campo.name] ?? "";
      }
    }

    function limpiar(prefijo) {
      rellenar(prefijo, {});
      porId(`resumen-${prefijo}`).value = "";
      if (prefijo === "enc") {
        porId("res-cifrado").value = "";
        porId("res-longitud").textContent = "-";
        porId("res-publica").textContent = "-";
      } else {
        porId("res-d").value = "";
        porId("res-mensaje").value = "";
      }
    }

    async function ejecutar(evento, prefijo) {
      evento.preventDefault();
      const datos = Object.fromEntries(new FormData(evento.currentTarget));
      const controles = document.querySelectorAll("button, input:not([readonly])");
      controles.forEach((control) => { control.disabled = true; });
      try {
        const ruta = prefijo === "enc" ? "cifrar" : "descifrar";
        const respuesta = await fetch(`/api/${ruta}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(datos)
        });
        const resultado = await respuesta.json().catch(() => null);
        if (!respuesta.ok || !resultado) {
          window.alert(`${resultado?.titulo || "Error"}\n\n${resultado?.error || "No se pudo completar la operacion. Intente nuevamente."}`);
          return;
        }
        if (prefijo === "enc") {
          porId("res-cifrado").value = resultado.cifrado;
          porId("res-longitud").textContent = String(resultado.longitud);
          porId("res-publica").textContent = `(${resultado.parametros.e}, ${resultado.parametros.n})`;
        } else {
          porId("res-d").value = String(resultado.d);
          porId("res-mensaje").value = resultado.mensaje;
        }
        porId(`resumen-${prefijo}`).value = resultado.resumen;
        porId(`resumen-${prefijo}`).scrollTop = 0;
      } catch {
        window.alert("Error de conexion\n\nNo se pudo conectar con el servidor. Intente nuevamente.");
      } finally {
        controles.forEach((control) => { control.disabled = false; });
      }
    }

    for (const prefijo of ["enc", "des"]) {
      porId(`form-${prefijo}`).addEventListener("submit", (evento) => ejecutar(evento, prefijo));
      porId(`tab-${prefijo}`).addEventListener("click", () => seleccionar(prefijo));
      porId(`tab-${prefijo}`).addEventListener("keydown", (evento) => {
        if (["ArrowLeft", "ArrowRight", "Home", "End"].includes(evento.key)) {
          evento.preventDefault();
          const otra = prefijo === "enc" ? "des" : "enc";
          seleccionar(evento.key === "Home" ? "enc" : evento.key === "End" ? "des" : otra, true);
        }
      });
    }
    document.querySelectorAll("[data-ejemplo]").forEach((boton) => {
      boton.addEventListener("click", () => rellenar(boton.dataset.ejemplo, ejemplos[boton.dataset.ejemplo]));
    });
    document.querySelectorAll("[data-limpiar]").forEach((boton) => {
      boton.addEventListener("click", () => limpiar(boton.dataset.limpiar));
    });
    porId("enviar").addEventListener("click", () => {
      const cifrado = porId("res-cifrado").value;
      if (!cifrado) {
        window.alert("Aviso\n\nPrimero debe encriptar un mensaje para copiar los datos.");
        return;
      }
      rellenar("des", {
        cifrado,
        longitud: porId("res-longitud").textContent,
        p: porId("enc-p").value,
        q: porId("enc-q").value,
        e: porId("enc-e").value
      });
      seleccionar("des");
    });
  </script>
</body>
</html>
'''


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
