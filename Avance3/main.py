# =====================================================================
# main.py - Avance 3 Final: Composición y Módulos
# Proyecto: RHEA - Tecnología para la salud hormonal femenina
#
# Este archivo contiene únicamente las importaciones, la instanciación
# de objetos y las pruebas de ejecución. Las clases están en modelos.py.
# =====================================================================

# Importamos las clases desde nuestro módulo modelos.py
from modelos import Biosensor, Medicion, PerfilHormonalRHEA, PerfilHormonalConSeguimiento


# ---------------------------------------------------------------------
# Instanciación de objetos (cada perfil tiene su propio Biosensor)
# ---------------------------------------------------------------------
sensor_maria = Biosensor("BS-001", "Sensor hormonal", bateria=100)
sensor_ana = Biosensor("BS-002", "Sensor hormonal", bateria=100)
sensor_lucia = Biosensor("BS-003", "Sensor hormonal", bateria=3)  # batería baja a propósito

usuaria_base = PerfilHormonalRHEA("María", 24, 55, sensor_maria)
usuaria_seg1 = PerfilHormonalConSeguimiento(
    "Ana", 29, 62, sensor_ana, "Dra. Ramírez", 7, diagnostico_previo="SOMP")
usuaria_seg2 = PerfilHormonalConSeguimiento(
    "Lucía", 21, 48, sensor_lucia, "Dr. Hernández", 14)


# ---------------------------------------------------------------------
# Prueba 1: Composición (la clase contenedora delega en el objeto contenido)
# ---------------------------------------------------------------------
print("=== 1. COMPOSICIÓN: el perfil 'tiene-un' Biosensor ===")
print(usuaria_base.biosensor.estado())  # acceso al objeto contenido
print(usuaria_base.actualizar_nivel_hormonal(58))  # el perfil delega la lectura al biosensor
print(usuaria_base.biosensor.estado())  # la batería bajó por la lectura delegada
print(usuaria_base.mostrar_perfil())  # el perfil delega la descripción del sensor
print()

print("=== 1.1 COMPOSICIÓN con colección: la subclase 'tiene' una lista de Medicion ===")
print(usuaria_seg1.actualizar_nivel_hormonal(75))
print(usuaria_seg1.actualizar_nivel_hormonal(80))
print(usuaria_seg1.resumen_mediciones())  # cada Medicion se describe a sí misma
print(usuaria_seg1.calcular_tendencia())
print()


# ---------------------------------------------------------------------
# Prueba 2: Herencia y Polimorfismo
# ---------------------------------------------------------------------
print("=== 2. HERENCIA Y POLIMORFISMO ===")
print(usuaria_seg1.registrar_sintoma("fatiga"))  # método heredado
print(usuaria_seg1.generar_alerta())  # sobrescrito: avisa al especialista
print(usuaria_base.generar_alerta())  # versión original de la base
print(usuaria_seg1.agendar_consulta("25/11/2026"))  # método propio de la subclase
print(f"¿usuaria_seg1 es PerfilHormonalRHEA? {isinstance(usuaria_seg1, PerfilHormonalRHEA)}")
print()


# ---------------------------------------------------------------------
# Prueba 3: Encapsulamiento
# ---------------------------------------------------------------------
print("=== 3. ENCAPSULAMIENTO ===")
print(f"Nivel hormonal de {usuaria_base.nombre} (getter): {usuaria_base.nivel_hormonal}")
usuaria_base.nivel_hormonal = 60  # setter con valor válido
print(f"Nuevo nivel (setter): {usuaria_base.nivel_hormonal}")

try:
    usuaria_base.nivel_hormonal = -10  # el setter rechaza negativos
except ValueError as error:
    print(f"Restricción del setter -> {error}")

try:
    usuaria_base.registrar_sintoma("   ")  # no se aceptan síntomas vacíos
except ValueError as error:
    print(f"Validación de síntoma vacío -> {error}")

try:
    print(usuaria_base.__nivel_hormonal)  # atributo privado inaccesible
except AttributeError:
    print("Acceso directo a '__nivel_hormonal' bloqueado: atributo privado.")

try:
    usuaria_base.biosensor.bateria = 100  # la batería del sensor es de solo lectura
except AttributeError:
    print("No se puede modificar la batería del biosensor desde fuera (solo lectura).")
print()


# ---------------------------------------------------------------------
# Prueba 4: Independencia de datos entre instancias (cada una con su self)
# ---------------------------------------------------------------------
print("=== 4. INDEPENDENCIA ENTRE OBJETOS (cada uno con su propio self y su propio Biosensor) ===")
print(f"Batería de {usuaria_base.nombre}: {usuaria_base.biosensor.bateria}%")
print(f"Batería de {usuaria_seg1.nombre}: {usuaria_seg1.biosensor.bateria}%")
print(f"Batería de {usuaria_seg2.nombre}: {usuaria_seg2.biosensor.bateria}%")
print(usuaria_seg2.actualizar_nivel_hormonal(52))
print(usuaria_seg2.actualizar_nivel_hormonal(49))
print(usuaria_seg2.calcular_tendencia())
print()

print("=== 4.1 Manejo de errores del componente: batería agotada ===")
try:
    usuaria_seg2.actualizar_nivel_hormonal(50)  # tercera lectura: se agota la batería
    usuaria_seg2.actualizar_nivel_hormonal(51)  # el sensor ya no puede leer
except RuntimeError as error:
    print(f"Error controlado -> {error}")
print(usuaria_seg2.biosensor.recargar())  # método del objeto contenido
print()


# ---------------------------------------------------------------------
# Resumen final: mismo método, comportamiento distinto según el objeto
# ---------------------------------------------------------------------
print("=== 5. RESUMEN FINAL (polimorfismo con mostrar_perfil) ===")
for perfil in (usuaria_base, usuaria_seg1, usuaria_seg2):
    print(perfil.mostrar_perfil())
    print("-" * 50)
