from flask import Flask, render_template_string, request
from datetime import date
import webbrowser
import threading
import re

app = Flask("preoperacional")


PAGINA = r"""
<!DOCTYPE html>
<html lang="es">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Formulario Preoperacional</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 15px;
    background: #eef2f6;
    font-family: Arial, sans-serif;
    color: #263445;
}

.contenedor {
    max-width: 550px;
    margin: 20px auto;
    background: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 4px 18px #00000015;
}

.encabezado {
    background: #202f40;
    color: white;
    padding: 22px;
    margin: -25px -25px 25px;
    border-radius: 14px 14px 0 0;
    text-align: center;
}

.encabezado h2 {
    margin: 0 0 10px;
    font-size: 20px;
}

.encabezado p {
    margin: 0;
    color: #52d3e5;
    font-size: 13px;
}

.progreso {
    background: #e3eaf0;
    height: 7px;
    border-radius: 10px;
    margin: 15px 0 25px;
    overflow: hidden;
}

.barra {
    height: 100%;
    width: 25%;
    background: #168aad;
    transition: width 0.3s;
}

.seccion-titulo {
    color: #168aad;
    font-size: 19px;
    margin-bottom: 20px;
}

label {
    display: block;
    font-weight: bold;
    margin: 19px 0 8px;
}

input, select, textarea {
    width: 100%;
    padding: 13px;
    border: 1px solid #cbd5df;
    border-radius: 8px;
    background: white;
    font-size: 16px;
    color: #263445;
}

textarea {
    min-height: 100px;
    resize: vertical;
}

input:focus, select:focus, textarea:focus {
    outline: 2px solid #168aad;
    border-color: #168aad;
}

.opciones {
    display: flex;
    gap: 9px;
}

.opciones label {
    flex: 1;
    margin: 0;
    cursor: pointer;
}

.opciones input {
    display: none;
}

.opciones span {
    display: block;
    text-align: center;
    padding: 13px 5px;
    border: 1px solid #cbd5df;
    border-radius: 8px;
    font-weight: normal;
}

.opciones input:checked + span {
    background: #168aad;
    color: white;
    border-color: #168aad;
}

.pregunta {
    padding-bottom: 16px;
    border-bottom: 1px solid #e5eaf0;
}

.ayuda {
    color: #64748b;
    font-size: 13px;
    margin-top: 6px;
}

.aviso {
    color: #d62828;
    font-size: 13px;
    margin-top: 6px;
    display: none;
}

.oculto {
    display: none;
}

.botones {
    display: flex;
    gap: 10px;
    margin-top: 28px;
}

button {
    flex: 1;
    padding: 15px;
    border: none;
    border-radius: 8px;
    background: #168aad;
    color: white;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
}

button.secundario {
    background: #64748b;
}

button:hover {
    opacity: 0.9;
}
</style>
</head>

<body>

<div class="contenedor">

<div class="encabezado">
    <h2>FORMULARIO PREOPERACIONAL</h2>
    <p>INSPECCIÓN DEL EQUIPO</p>
</div>

<div class="progreso">
    <div class="barra" id="barra"></div>
</div>

<form method="POST" id="formulario">

<!-- FASE 1 -->

<section id="fase1">

<h3 class="seccion-titulo">
FASE 1 - SITIO DE TRABAJO E INFORMACIÓN DEL OPERADOR
</h3>

<label>1. Fecha</label>
<input type="date" name="fecha" value="{{ hoy }}" required>

<label>2. Turno</label>
<select name="turno" required>
    <option value="">Seleccionar turno</option>
    <option>Día</option>
    <option>Noche</option>
</select>

<label>3. Operador</label>
<select name="operador" required>
    <option value="">Seleccionar operador</option>
    <option>Leonardo López</option>
    <option>Edinson Luna</option>
</select>

<label>4. Máquina</label>
<select name="maquina" required>
    <option value="">Seleccionar máquina</option>
    {% for i in range(1, 12) %}
    <option>#{{ i }}</option>
    {% endfor %}
</select>

<label>5. Horómetro inicial</label>
<input
    type="text"
    name="horometro"
    class="numero"
    inputmode="decimal"
    placeholder="Escribir horómetro"
    required
>
<div class="aviso">Solo se pueden escribir números.</div>

<div class="botones">
    <button type="button" onclick="siguiente(2)">
        CONTINUAR
    </button>
</div>

</section>


<!-- FASE 2 -->

<section id="fase2" class="oculto">

<h3 class="seccion-titulo">
FASE 2 - NIVELES Y FUGAS
</h3>

<div class="pregunta">
<label>1. Nivel de aceite de motor</label>
<select name="aceite_motor" required>
    <option value="">Seleccionar</option>
    <option>Full</option>
    <option>Medio</option>
    <option>Bajo</option>
</select>
</div>

<div class="pregunta">
<label>2. Nivel de refrigerante</label>
<select name="refrigerante" required>
    <option value="">Seleccionar</option>
    <option>Full</option>
    <option>Medio</option>
    <option>Bajo</option>
</select>
</div>

<div class="pregunta">
<label>3. Nivel de hidráulico</label>
<select name="hidraulico" required>
    <option value="">Seleccionar</option>
    <option>Full</option>
    <option>Medio</option>
    <option>Bajo</option>
</select>
</div>

<div class="pregunta">
<label>4. Nivel de combustible</label>
<input
    type="text"
    name="combustible"
    id="combustible"
    class="numero"
    inputmode="decimal"
    placeholder="Escribir cantidad"
    required
>
<div class="ayuda">
    Al salir del campo aparecerá automáticamente la palabra centímetros.
</div>
<div class="aviso">Solo se pueden escribir números.</div>
</div>

<div class="pregunta">
<label>5. Nivel de motor de giro</label>
<select name="motor_giro" required>
    <option value="">Seleccionar</option>
    <option>Full</option>
    <option>Medio</option>
    <option>Bajo</option>
    <option>No aplica</option>
</select>
</div>

<div class="pregunta">
<label>6. Nivel de aceite de servotransmisión</label>
<select name="servotransmision" required>
    <option value="">Seleccionar</option>
    <option>Full</option>
    <option>Medio</option>
    <option>Bajo</option>
    <option>No aplica</option>
</select>
</div>

<div class="pregunta">
<label>7. Nivel de líquido de frenos</label>
<select name="liquido_frenos" required>
    <option value="">Seleccionar</option>
    <option>Full</option>
    <option>Medio</option>
    <option>Bajo</option>
    <option>No aplica</option>
</select>
</div>

<div class="pregunta">
<label>8. Estado de pastillas</label>
<select name="pastillas" required>
    <option value="">Seleccionar</option>
    <option>Bueno</option>
    <option>Regular</option>
    <option>Malo</option>
    <option>No aplica</option>
</select>
</div>

<div class="pregunta">
<label>9. Estado de llantas u orugas</label>
<select name="llantas_orugas" required>
    <option value="">Seleccionar</option>
    <option>Bueno</option>
    <option>Regular</option>
    <option>Malo</option>
</select>
</div>

<div class="pregunta">
<label>10. ¿El equipo cuenta con engrase necesario?</label>

<div class="opciones">
    <label>
        <input type="radio" name="engrase" value="Sí" required>
        <span>Sí</span>
    </label>

    <label>
        <input type="radio" name="engrase" value="No">
        <span>No</span>
    </label>
</div>
</div>

<h3 class="seccion-titulo" style="margin-top:30px">
FUGAS
</h3>

<label>11. ¿El equipo presenta fugas?</label>

<div class="opciones">
    <label>
        <input
            type="radio"
            name="fugas"
            value="Sí"
            onchange="mostrarDescripcion()"
            required
        >
        <span>Sí</span>
    </label>

    <label>
        <input
            type="radio"
            name="fugas"
            value="No"
            onchange="mostrarDescripcion()"
        >
        <span>No</span>
    </label>
</div>

<div id="descripcionFuga" class="oculto">

    <label>Describa dónde presenta la fuga</label>

    <textarea
        name="detalle_fuga"
        id="detalleFuga"
        placeholder="Ejemplo: fuga de aceite hidráulico en una manguera..."
    ></textarea>

    <div class="ayuda">
        Si selecciona Sí, debe describir obligatoriamente la fuga.
    </div>

</div>

<div class="botones">

    <button
        type="button"
        class="secundario"
        onclick="anterior(1)"
    >
        REGRESAR
    </button>

    <button type="button" onclick="siguiente(3)">
        CONTINUAR
    </button>

</div>

</section>


<!-- FASE 3 -->

<section id="fase3" class="oculto">

<h3 class="seccion-titulo">
FASE 3 - ESTADO GENERAL DE LA MÁQUINA
</h3>

<div class="pregunta">
<label>1. Luces</label>
<select name="luces" required>
    <option value="">Seleccionar</option>
    <option>Bueno</option>
    <option>Regular</option>
    <option>Malo</option>
</select>
</div>

<div class="pregunta">
<label>2. Limpiaparabrisas</label>
<select name="limpiaparabrisas" required>
    <option value="">Seleccionar</option>
    <option>Bueno</option>
    <option>Regular</option>
    <option>Malo</option>
</select>
</div>

<div class="pregunta">
<label>3. Aire acondicionado</label>
<select name="aire_acondicionado" required>
    <option value="">Seleccionar</option>
    <option>Bueno</option>
    <option>Regular</option>
    <option>Malo</option>
</select>
</div>

<div class="pregunta">
<label>4. Espejos</label>
<select name="espejos" required>
    <option value="">Seleccionar</option>
    <option>Bueno</option>
    <option>Regular</option>
    <option>Malo</option>
</select>
</div>

<div class="pregunta">
<label>5. Pito</label>
<select name="pito" required>
    <option value="">Seleccionar</option>
    <option>Bueno</option>
    <option>Regular</option>
    <option>Malo</option>
</select>
</div>

<div class="pregunta">
<label>6. Silla</label>
<select name="silla" required>
    <option value="">Seleccionar</option>
    <option>Bueno</option>
    <option>Regular</option>
    <option>Malo</option>
</select>
</div>

<div class="pregunta">
<label>7. Cinturón de seguridad</label>
<select name="cinturon" required>
    <option value="">Seleccionar</option>
    <option>Bueno</option>
    <option>Regular</option>
    <option>Malo</option>
</select>
</div>

<div class="pregunta">
<label>8. Extintor</label>

<div class="opciones">
    <label>
        <input type="radio" name="extintor" value="Sí" required>
        <span>Sí</span>
    </label>

    <label>
        <input type="radio" name="extintor" value="No">
        <span>No</span>
    </label>
</div>
</div>

<div class="pregunta">
<label>9. Kit antiderrames</label>

<div class="opciones">
    <label>
        <input type="radio" name="kit_antiderrames" value="Sí" required>
        <span>Sí</span>
    </label>

    <label>
        <input type="radio" name="kit_antiderrames" value="No">
        <span>No</span>
    </label>
</div>
</div>

<div class="botones">

    <button
        type="button"
        class="secundario"
        onclick="anterior(2)"
    >
        REGRESAR
    </button>

    <button type="button" onclick="siguiente(4)">
        CONTINUAR
    </button>

</div>

</section>


<!-- FASE 4 -->

<section id="fase4" class="oculto">

<h3 class="seccion-titulo">
FASE 4 - ESTADO DEL OPERADOR Y SEGURIDAD DEL ÁREA DE TRABAJO
</h3>

<div class="pregunta">
<label>
1. ¿Se encuentra en buenas condiciones físicas y mentales para realizar su turno?
</label>

<div class="opciones">
    <label>
        <input type="radio" name="condiciones_operador" value="Sí" required>
        <span>Sí</span>
    </label>

    <label>
        <input type="radio" name="condiciones_operador" value="No">
        <span>No</span>
    </label>
</div>
</div>

<div class="pregunta">
<label>
2. ¿Presenta sueño, fatiga o cansancio en este momento?
</label>

<div class="opciones">
    <label>
        <input type="radio" name="sueno_fatiga" value="Sí" required>
        <span>Sí</span>
    </label>

    <label>
        <input type="radio" name="sueno_fatiga" value="No">
        <span>No</span>
    </label>
</div>
</div>

<div class="pregunta">
<label>
3. ¿Se siente concentrado y atento para operar la máquina?
</label>

<div class="opciones">
    <label>
        <input type="radio" name="concentracion" value="Sí" required>
        <span>Sí</span>
    </label>

    <label>
        <input type="radio" name="concentracion" value="No">
        <span>No</span>
    </label>
</div>
</div>

<div class="pregunta">
<label>
4. ¿Presenta algún malestar físico que pueda afectar su trabajo?
</label>

<div class="opciones">
    <label>
        <input type="radio" name="malestar_fisico" value="Sí" required>
        <span>Sí</span>
    </label>

    <label>
        <input type="radio" name="malestar_fisico" value="No">
        <span>No</span>
    </label>
</div>
</div>

<div class="pregunta">
<label>
5. ¿Se encuentra bajo algún estado de estrés, preocupación o alteración emocional que pueda afectar su concentración?
</label>

<div class="opciones">
    <label>
        <input type="radio" name="estres" value="Sí" required>
        <span>Sí</span>
    </label>

    <label>
        <input type="radio" name="estres" value="No">
        <span>No</span>
    </label>
</div>
</div>

<div class="pregunta">
<label>
6. ¿Inspeccionó el área de trabajo y considera que ofrece condiciones seguras para iniciar la operación?
</label>

<div class="opciones">
    <label>
        <input type="radio" name="area_segura" value="Sí" required>
        <span>Sí</span>
    </label>

    <label>
        <input type="radio" name="area_segura" value="No">
        <span>No</span>
    </label>
</div>
</div>

<div class="pregunta">
<label>
7. ¿Cómo considera el flujo de vehículos y personas en el área de trabajo?
</label>

<div class="opciones">
    <label>
        <input type="radio" name="flujo_area" value="Normal" required>
        <span>Normal</span>
    </label>

    <label>
        <input type="radio" name="flujo_area" value="Alto">
        <span>Alto</span>
    </label>

    <label>
        <input type="radio" name="flujo_area" value="Excesivo">
        <span>Excesivo</span>
    </label>
</div>
</div>

<div class="botones">

    <button
        type="button"
        class="secundario"
        onclick="anterior(3)"
    >
        REGRESAR
    </button>

    <button type="submit">
        FINALIZAR
    </button>

</div>

</section>

</form>
</div>


<script>

// CAMBIO ENTRE LAS CUATRO FASES

function mostrarFase(numero) {

    for (let i = 1; i <= 4; i++) {
        document.getElementById("fase" + i).classList.add("oculto");
    }

    document.getElementById("fase" + numero).classList.remove("oculto");

    const barra = document.getElementById("barra");

    barra.style.width = (numero * 25) + "%";

    window.scrollTo(0, 0);
}


// VALIDAR UNA FASE ANTES DE CONTINUAR

function validarFase(numero) {

    const fase = document.getElementById("fase" + numero);

    const campos = fase.querySelectorAll(
        "input[required], select[required], textarea[required]"
    );

    for (const campo of campos) {

        if (!campo.checkValidity()) {
            campo.reportValidity();
            return false;
        }
    }

    return true;
}


function siguiente(numero) {

    const faseActual = numero - 1;

    if (validarFase(faseActual)) {
        mostrarFase(numero);
    }
}


function anterior(numero) {
    mostrarFase(numero);
}


// VALIDACIÓN NUMÉRICA

document.querySelectorAll(".numero").forEach(campo => {

    campo.addEventListener("input", function() {

        const valor = this.value;
        const aviso = this.parentElement.querySelector(".aviso");

        if (/^\d*(\.\d*)?$/.test(valor)) {

            aviso.style.display = "none";

        } else {

            aviso.style.display = "block";

            this.value = valor.replace(/[^0-9.]/g, "");

            const partes = this.value.split(".");

            if (partes.length > 2) {
                this.value = partes[0] + "." +
                    partes.slice(1).join("");
            }
        }
    });

});


// COMBUSTIBLE EN CENTÍMETROS

const combustible = document.getElementById("combustible");

combustible.addEventListener("blur", function() {

    if (this.value.trim() !== "") {
        this.value = this.value.replace(/\s*centímetros$/i, "");
        this.value = this.value + " centímetros";
    }

});

combustible.addEventListener("focus", function() {

    this.value = this.value.replace(/\s*centímetros$/i, "");

});


// DESCRIPCIÓN DE FUGAS

function mostrarDescripcion() {

    const seleccion = document.querySelector(
        'input[name="fugas"]:checked'
    );

    const bloque = document.getElementById("descripcionFuga");
    const detalle = document.getElementById("detalleFuga");

    if (seleccion && seleccion.value === "Sí") {

        bloque.classList.remove("oculto");
        detalle.required = true;

    } else {

        bloque.classList.add("oculto");
        detalle.required = false;
        detalle.value = "";
    }
}

</script>

</body>
</html>
"""


# RECIBIR Y VALIDAR EL FORMULARIO

@app.route("/", methods=["GET", "POST"])
def inicio():

    if request.method == "POST":

        datos = request.form.to_dict()

        campos_obligatorios = [
            # FASE 1
            "fecha",
            "turno",
            "operador",
            "maquina",
            "horometro",

            # FASE 2
            "aceite_motor",
            "refrigerante",
            "hidraulico",
            "combustible",
            "motor_giro",
            "servotransmision",
            "liquido_frenos",
            "pastillas",
            "llantas_orugas",
            "engrase",
            "fugas",

            # FASE 3
            "luces",
            "limpiaparabrisas",
            "aire_acondicionado",
            "espejos",
            "pito",
            "silla",
            "cinturon",
            "extintor",
            "kit_antiderrames",

            # FASE 4
            "condiciones_operador",
            "sueno_fatiga",
            "concentracion",
            "malestar_fisico",
            "estres",
            "area_segura",
            "flujo_area"
        ]

        for campo in campos_obligatorios:
            if not datos.get(campo):
                return f"Falta completar: {campo}", 400

        # VALIDAR HORÓMETRO Y COMBUSTIBLE

        for campo in ["horometro", "combustible"]:

            valor = datos[campo].replace(
                " centímetros", ""
            ).strip()

            if not re.fullmatch(r"\d+(\.\d+)?", valor):
                return f"El campo {campo} debe contener números.", 400

        # VALIDAR DESCRIPCIÓN DE FUGA

        if datos["fugas"] == "Sí":
            if not datos.get("detalle_fuga", "").strip():
                return "Debes describir la fuga.", 400

        # CONFIRMACIÓN

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Datos recibidos</title>

        <style>
        body {
            background: #eef2f6;
            font-family: Arial;
            padding: 20px;
        }

        .caja {
            max-width: 500px;
            margin: 30px auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
            line-height: 1.8;
        }

        h2 {
            color: #168aad;
        }

        a {
            color: #168aad;
        }
        </style>
        </head>

        <body>
        <div class="caja">
            <h2>¡Datos recibidos correctamente!</h2>
            <p>El formulario preoperacional se completó correctamente.</p>
            <a href="/">Volver al formulario</a>
        </div>
        </body>
        </html>
        """)

    return render_template_string(
        PAGINA,
        hoy=date.today().isoformat()
    )


# INICIAR SERVIDOR Y ABRIR NAVEGADOR

threading.Timer(
    1.5,
    lambda: webbrowser.open("http://127.0.0.1:5000")
).start()

app.run(
    host="127.0.0.1",
    port=5000,
    debug=False,
    use_reloader=False
)