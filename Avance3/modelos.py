# =====================================================================
# modelos.py - Avance 3 Final: Composición y Módulos
# Proyecto: RHEA - Tecnología para la salud hormonal femenina
#
# Este módulo contiene TODAS las clases del sistema:
#   - Biosensor (clase auxiliar para Composición)
#   - Medicion (clase auxiliar para Composición con colección de objetos)
#   - PerfilHormonalRHEA (clase base)
#   - PerfilHormonalConSeguimiento (subclase)
#
# Nota: los niveles hormonales son valores de referencia en unidades
# arbitrarias, solo para fines demostrativos.
# =====================================================================


# ---------------------------------------------------------------------
# CLASE AUXILIAR PARA COMPOSICIÓN: Biosensor
# Un perfil "tiene-un" Biosensor que le entrega las lecturas.
# ---------------------------------------------------------------------
class Biosensor:
    def __init__(self, id_sensor, tipo, bateria=100):
        self.id_sensor = id_sensor
        self.tipo = tipo
        self.activo = True
        # Encapsulamiento: la batería es privada y se valida en su setter
        self.__bateria = None
        self.__asignar_bateria(bateria)

    # Método privado de validación (Encapsulamiento)
    def __asignar_bateria(self, valor):
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise ValueError(f"La batería debe ser numérica, se recibió: {valor!r}")
        if not 0 <= valor <= 100:
            raise ValueError(f"La batería debe estar entre 0 y 100, se recibió: {valor}")
        self.__bateria = valor

    # Getter de solo lectura: nadie de fuera puede modificar la batería directamente
    @property
    def bateria(self):
        return self.__bateria

    # Método 1: tomar una lectura (consume 1% de batería)
    def leer_nivel(self, valor_medido):
        if not self.activo:
            raise RuntimeError(f"El biosensor {self.id_sensor} está apagado.")
        if self.__bateria <= 0:
            raise RuntimeError(f"El biosensor {self.id_sensor} no tiene batería.")
        if valor_medido < 0:
            raise ValueError("El biosensor no puede reportar lecturas negativas.")
        self.__bateria -= 1
        return valor_medido

    # Método 2: recargar la batería
    def recargar(self):
        self.__bateria = 100
        return f"Biosensor {self.id_sensor} recargado al 100%."

    # Método 3: describir el estado del sensor
    def estado(self):
        encendido = "activo" if self.activo else "apagado"
        return f"Biosensor {self.id_sensor} ({self.tipo}) | {encendido} | batería {self.__bateria}%"


# ---------------------------------------------------------------------
# CLASE AUXILIAR PARA COMPOSICIÓN: Medicion
# Un perfil con seguimiento "tiene" una colección de objetos Medicion.
# ---------------------------------------------------------------------
class Medicion:
    def __init__(self, valor, etiqueta="lectura"):
        self.valor = valor
        self.etiqueta = etiqueta

    def describir(self):
        return f"{self.etiqueta}: {self.valor}"


# ---------------------------------------------------------------------
# CLASE BASE (Superclase) - ahora con Composición
# ---------------------------------------------------------------------
class PerfilHormonalRHEA:
    def __init__(self, nombre, edad, nivel_hormonal, biosensor, diagnostico_previo=None):
        self.nombre = nombre
        self.edad = edad
        self.diagnostico_previo = diagnostico_previo

        # COMPOSICIÓN: un perfil "tiene-un" Biosensor
        self.biosensor = biosensor

        # Encapsulamiento: atributo protegido
        self._historial_sintomas = []

        # Encapsulamiento: atributo privado (se asigna mediante el setter)
        self.__nivel_hormonal = None
        self.nivel_hormonal = nivel_hormonal

    # Getter con @property
    @property
    def nivel_hormonal(self):
        return self.__nivel_hormonal

    # Setter con validaciones
    @nivel_hormonal.setter
    def nivel_hormonal(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(f"El nivel hormonal debe ser numérico, se recibió: {valor!r}")
        if valor < 0:
            raise ValueError(f"El nivel hormonal no puede ser negativo, se recibió: {valor}")
        self.__nivel_hormonal = valor

    @property
    def historial_sintomas(self):
        return list(self._historial_sintomas)

    # Método 1: registrar síntoma
    def registrar_sintoma(self, sintoma):
        if not sintoma or not sintoma.strip():
            raise ValueError("El síntoma no puede estar vacío.")
        self._historial_sintomas.append(sintoma.strip())
        return (f"[{self.nombre}] Síntoma registrado: '{sintoma.strip()}'. "
                f"Total en historial: {len(self._historial_sintomas)}.")

    # Método 2: actualizar nivel hormonal.
    # DELEGACIÓN: la lectura la realiza el objeto Biosensor contenido.
    def actualizar_nivel_hormonal(self, nuevo_nivel):
        nivel_anterior = self.nivel_hormonal
        lectura = self.biosensor.leer_nivel(nuevo_nivel)  # delegación al componente
        self.nivel_hormonal = lectura
        return (f"[{self.nombre}] Nivel hormonal actualizado por el biosensor "
                f"{self.biosensor.id_sensor}: {nivel_anterior} -> {self.nivel_hormonal}.")

    # Método 3: generar alerta (será extendido en la subclase)
    def generar_alerta(self, umbral=70):
        if self.nivel_hormonal > umbral:
            return (f"ALERTA [{self.nombre}]: nivel hormonal de {self.nivel_hormonal} "
                    f"supera el umbral de {umbral}. Se recomienda consultar a un especialista.")
        return f"[{self.nombre}] Nivel hormonal ({self.nivel_hormonal}) dentro del rango normal."

    # Método 4: mostrar perfil (será sobrescrito en la subclase)
    def mostrar_perfil(self):
        return (f"--- Perfil RHEA: {self.nombre} ---\n"
                f"Edad: {self.edad} años\n"
                f"Nivel hormonal: {self.nivel_hormonal}\n"
                f"Diagnóstico previo: {self.diagnostico_previo or 'Ninguno'}\n"
                f"Síntomas: {self._historial_sintomas or 'Sin síntomas registrados'}\n"
                f"{self.biosensor.estado()}")  # delegación: el sensor describe su estado


# ---------------------------------------------------------------------
# SUBCLASE (Herencia) - con una colección de objetos Medicion (Composición)
# ---------------------------------------------------------------------
class PerfilHormonalConSeguimiento(PerfilHormonalRHEA):
    def __init__(self, nombre, edad, nivel_hormonal, biosensor, especialista,
                 frecuencia_medicion_dias, diagnostico_previo=None):
        # super() reutiliza el constructor de la superclase
        super().__init__(nombre, edad, nivel_hormonal, biosensor, diagnostico_previo)

        self.especialista = especialista
        self.frecuencia_medicion_dias = frecuencia_medicion_dias

        # COMPOSICIÓN: la subclase "tiene" una lista de objetos Medicion
        self._historial_mediciones = [Medicion(nivel_hormonal, "Lectura inicial")]

    # Método propio: tendencia (usa el atributo valor de los objetos Medicion)
    def calcular_tendencia(self):
        if len(self._historial_mediciones) < 2:
            return f"[{self.nombre}] Aún no hay suficientes mediciones para calcular tendencia."
        anterior = self._historial_mediciones[-2].valor
        actual = self._historial_mediciones[-1].valor
        if actual > anterior:
            direccion = "al alza"
        elif actual < anterior:
            direccion = "a la baja"
        else:
            direccion = "estable"
        return (f"[{self.nombre}] Tendencia {direccion}: {anterior} -> {actual} "
                f"({len(self._historial_mediciones)} mediciones guardadas).")

    # Método propio: agendar consulta
    def agendar_consulta(self, fecha):
        return (f"[{self.nombre}] Consulta agendada con {self.especialista} "
                f"para el {fecha}. Mediciones sugeridas cada {self.frecuencia_medicion_dias} días.")

    # Método propio: resumen del historial (delegación a cada Medicion)
    def resumen_mediciones(self):
        detalle = " | ".join(m.describir() for m in self._historial_mediciones)
        return f"[{self.nombre}] Historial de mediciones -> {detalle}"

    # Sobrescritura (Polimorfismo): guarda además la medición como objeto Medicion
    def actualizar_nivel_hormonal(self, nuevo_nivel):
        mensaje = super().actualizar_nivel_hormonal(nuevo_nivel)
        numero = len(self._historial_mediciones) + 1
        self._historial_mediciones.append(Medicion(nuevo_nivel, f"Medición #{numero}"))
        return f"{mensaje} Medición #{numero} guardada."

    # Sobrescritura (Polimorfismo): avisa al especialista
    def generar_alerta(self, umbral=70):
        mensaje = super().generar_alerta(umbral)
        if self.nivel_hormonal > umbral:
            mensaje += f" Aviso enviado a {self.especialista}."
        return mensaje

    # Sobrescritura (Polimorfismo): extiende el perfil
    def mostrar_perfil(self):
        return (f"{super().mostrar_perfil()}\n"
                f"Especialista asignado: {self.especialista}\n"
                f"Frecuencia de medición: cada {self.frecuencia_medicion_dias} días\n"
                f"Mediciones guardadas: {len(self._historial_mediciones)}")
