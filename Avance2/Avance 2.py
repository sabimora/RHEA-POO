# =====================================================================
# Avance 2: Herencia, Encapsulamiento y Diagrama UML
# Proyecto: RHEA - Tecnología para la salud hormonal femenina
#
# Descripción del sistema:
# Este sistema modela los perfiles de las usuarias de RHEA. Cada perfil
# guarda los datos de la usuaria, el nivel hormonal que entrega el
# biosensor y su historial de síntomas. Existe un perfil base
# (PerfilHormonalRHEA) y un perfil con seguimiento médico
# (PerfilHormonalConSeguimiento) que hereda del base y agrega un
# especialista asignado, un historial de mediciones y una tendencia.
# Nota: los niveles hormonales son valores de referencia en unidades
# arbitrarias, solo para fines demostrativos.
# =====================================================================


# ---------------------------------------------------------------------
# Creación de la clase base (Superclase)
# ---------------------------------------------------------------------
class PerfilHormonalRHEA:
    def __init__(self, nombre, edad, nivel_hormonal, diagnostico_previo=None):
        # Atributos públicos
        self.nombre = nombre
        self.edad = edad
        self.diagnostico_previo = diagnostico_previo

        # Aplicación de Encapsulamiento: atributo protegido (un guion bajo)
        self._historial_sintomas = []

        # Aplicación de Encapsulamiento: atributo privado (doble guion bajo)
        self.__nivel_hormonal = None
        # Al asignar con self.nivel_hormonal se ejecuta el setter (con validación)
        self.nivel_hormonal = nivel_hormonal

    # Getter con @property: consulta segura del atributo privado
    @property
    def nivel_hormonal(self):
        return self.__nivel_hormonal

    # Setter con @property: modificación controlada con validaciones
    @nivel_hormonal.setter
    def nivel_hormonal(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(f"El nivel hormonal debe ser numérico, se recibió: {valor!r}")
        if valor < 0:
            raise ValueError(f"El nivel hormonal no puede ser negativo, se recibió: {valor}")
        self.__nivel_hormonal = valor

    # Getter de solo lectura para el historial protegido (devuelve una copia)
    @property
    def historial_sintomas(self):
        return list(self._historial_sintomas)

    # Método 1: registrar un síntoma (valida que no venga vacío)
    def registrar_sintoma(self, sintoma):
        if not sintoma or not sintoma.strip():
            raise ValueError("El síntoma no puede estar vacío.")
        self._historial_sintomas.append(sintoma.strip())
        return (f"[{self.nombre}] Síntoma registrado: '{sintoma.strip()}'. "
                f"Total en historial: {len(self._historial_sintomas)}.")

    # Método 2: actualizar el nivel hormonal (pasa por el setter)
    def actualizar_nivel_hormonal(self, nuevo_nivel):
        nivel_anterior = self.nivel_hormonal
        self.nivel_hormonal = nuevo_nivel
        return (f"[{self.nombre}] Nivel hormonal actualizado por el biosensor: "
                f"{nivel_anterior} -> {self.nivel_hormonal}.")

    # Método 3: generar una alerta según un umbral (este será extendido en la hija)
    def generar_alerta(self, umbral=70):
        if self.nivel_hormonal > umbral:
            return (f"ALERTA [{self.nombre}]: nivel hormonal de {self.nivel_hormonal} "
                    f"supera el umbral de {umbral}. Se recomienda consultar a un especialista.")
        return f"[{self.nombre}] Nivel hormonal ({self.nivel_hormonal}) dentro del rango normal."

    # Método 4: mostrar el perfil (este será sobrescrito en la hija)
    def mostrar_perfil(self):
        return (f"--- Perfil RHEA: {self.nombre} ---\n"
                f"Edad: {self.edad} años\n"
                f"Nivel hormonal: {self.nivel_hormonal}\n"
                f"Diagnóstico previo: {self.diagnostico_previo or 'Ninguno'}\n"
                f"Síntomas: {self._historial_sintomas or 'Sin síntomas registrados'}")


# ---------------------------------------------------------------------
# Uso de super() y Herencia (Subclase)
# ---------------------------------------------------------------------
class PerfilHormonalConSeguimiento(PerfilHormonalRHEA):
    def __init__(self, nombre, edad, nivel_hormonal, especialista,
                 frecuencia_medicion_dias, diagnostico_previo=None):
        # super() reutiliza el constructor de la superclase
        super().__init__(nombre, edad, nivel_hormonal, diagnostico_previo)

        # Atributos nuevos propios de la subclase
        self.especialista = especialista
        self.frecuencia_medicion_dias = frecuencia_medicion_dias
        # Atributo protegido: historial de mediciones (inicia con la lectura inicial)
        self._historial_mediciones = [nivel_hormonal]

    # Método 5 (propio de la subclase): calcular la tendencia de las mediciones
    def calcular_tendencia(self):
        if len(self._historial_mediciones) < 2:
            return f"[{self.nombre}] Aún no hay suficientes mediciones para calcular tendencia."
        anterior, actual = self._historial_mediciones[-2], self._historial_mediciones[-1]
        if actual > anterior:
            direccion = "al alza"
        elif actual < anterior:
            direccion = "a la baja"
        else:
            direccion = "estable"
        return (f"[{self.nombre}] Tendencia {direccion}: {anterior} -> {actual} "
                f"({len(self._historial_mediciones)} mediciones guardadas).")

    # Método 6 (propio de la subclase): agendar consulta con el especialista
    def agendar_consulta(self, fecha):
        return (f"[{self.nombre}] Consulta agendada con {self.especialista} "
                f"para el {fecha}. Mediciones sugeridas cada {self.frecuencia_medicion_dias} días.")

    # -----------------------------------------------------------------
    # Sobrescritura de métodos (Polimorfismo)
    # -----------------------------------------------------------------
    # Override 1: además de actualizar el nivel, guarda la medición en el historial
    def actualizar_nivel_hormonal(self, nuevo_nivel):
        mensaje = super().actualizar_nivel_hormonal(nuevo_nivel)
        self._historial_mediciones.append(nuevo_nivel)
        return f"{mensaje} Medición #{len(self._historial_mediciones)} guardada."

    # Override 2: extiende la alerta avisando al especialista asignado
    def generar_alerta(self, umbral=70):
        mensaje = super().generar_alerta(umbral)
        if self.nivel_hormonal > umbral:
            mensaje += f" Aviso enviado a {self.especialista}."
        return mensaje

    # Override 3: extiende el perfil con los datos de seguimiento
    def mostrar_perfil(self):
        return (f"{super().mostrar_perfil()}\n"
                f"Especialista asignado: {self.especialista}\n"
                f"Frecuencia de medición: cada {self.frecuencia_medicion_dias} días\n"
                f"Historial de mediciones: {self._historial_mediciones}")


# ---------------------------------------------------------------------
# Instanciación y pruebas
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # 1 objeto de la clase base y 2 de la subclase
    usuaria_base = PerfilHormonalRHEA("María", 24, 55)
    usuaria_seg1 = PerfilHormonalConSeguimiento(
        "Ana", 29, 62, "Dra. Ramírez", 7, diagnostico_previo="SOMP")
    usuaria_seg2 = PerfilHormonalConSeguimiento(
        "Lucía", 21, 48, "Dr. Hernández", 14)

    print("=== 1. Uso básico de la clase base ===")
    print(usuaria_base.registrar_sintoma("dolor abdominal"))
    print(usuaria_base.actualizar_nivel_hormonal(58))
    print(usuaria_base.generar_alerta())
    print()

    print("=== 2. Herencia y métodos sobrescritos (polimorfismo) ===")
    print(usuaria_seg1.registrar_sintoma("fatiga"))  # método heredado sin cambios
    print(usuaria_seg1.actualizar_nivel_hormonal(75))  # sobrescrito: guarda medición
    print(usuaria_seg1.generar_alerta())  # sobrescrito: avisa al especialista
    print(usuaria_seg1.calcular_tendencia())  # método propio de la subclase
    print(usuaria_seg1.agendar_consulta("25/10/2026"))  # método propio de la subclase
    print()

    print("=== 3. Encapsulamiento (getter/setter y validaciones) ===")
    print(f"Nivel hormonal de {usuaria_base.nombre} (vía getter): {usuaria_base.nivel_hormonal}")
    usuaria_base.nivel_hormonal = 60  # el setter acepta valores válidos
    print(f"Nuevo nivel (vía setter): {usuaria_base.nivel_hormonal}")

    try:
        usuaria_base.nivel_hormonal = -10  # el setter debe rechazar negativos
    except ValueError as error:
        print(f"Restricción del setter funcionando -> {error}")

    try:
        usuaria_base.registrar_sintoma("   ")  # no se aceptan síntomas vacíos
    except ValueError as error:
        print(f"Validación de síntoma vacío -> {error}")

    try:
        print(usuaria_base.__nivel_hormonal)  # el atributo privado no es accesible directo
    except AttributeError:
        print("Acceso directo a '__nivel_hormonal' bloqueado: el atributo es privado.")
    print()

    print("=== 4. Independencia de datos entre instancias (cada una con su self) ===")
    print(usuaria_seg2.actualizar_nivel_hormonal(52))
    print(usuaria_seg2.actualizar_nivel_hormonal(49))
    print(usuaria_seg2.calcular_tendencia())
    print()

    # Polimorfismo: el mismo método mostrar_perfil() se comporta distinto según el objeto
    for perfil in (usuaria_base, usuaria_seg1, usuaria_seg2):
        print(perfil.mostrar_perfil())
        print("-" * 45)
