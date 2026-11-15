class PerfilHormonalRHEA:
  def __init__(self, nombre, edad, nivel_hormonal, diagnostico_previo=None):
    self.nombre = nombre
    self.edad = edad
    self.nivel_hormonal = nivel_hormonal
    self. diagnostico_previo = diagnostico_previo
    self.historial_sintomas = []

  def registrar_sintomas(self, sintoma):
    self.historial_sintomas.append(sintoma)
    print(f"[{self.nombre}] Síntoma registrado: {sintoma}.\n[{self.nombre}] Total de síntomas en el historial: {len(self.historial_sintomas)}.")

  def actualivar_hormonas(self, nuevo_nivel):
    nivel_anterior = self.nivel_hormonal
    self.nivel_hormonal = nuevo_nivel
    print(f"[{self.nombre}] Nivel hormonal actualizado: {nivel_anterior} -> {self.nivel_hormonal}")

  def generar_alerta(self, umbral=70):
    if self.nivel_hormonal > umbral:
      print(f"[{self.nombre}] ALERTA: nivel hormonal de {self.nivel_hormonal} supera el umbral de {umbral}. Se recomienda acudir con el especialista.")
    else:
      print(f"[{self.nombre}] Nivel hormonal de {self.nivel_hormonal} dentro del rango normal.")

  def mostrar_perfil(self):
    print(f"Perfil RHEA de {self.nombre}\n Edad: {self.edad}\n Nivel hormonal actual: {self.nivel_hormonal}\n Diagnóstico previo: {self.diagnostico_previo or 'Ninguno'}\n Síntomas registrados: {self.historial_sintomas or 'Sin síntomas registrados'}")
    print("-" * 40)

usuaria1 = PerfilHormonalRHEA("Maria", 24, 55)
usuaria2 = PerfilHormonalRHEA("Ana", 29, 62, diagnostico_previo = "SOMP")
usuaria3 = PerfilHormonalRHEA("Lucia", 21, 48)

usuaria1.registrar_sintomas("dolor abdominal")
usuaria1.actualivar_hormonas(78)
usuaria1.generar_alerta()

usuaria2.registrar_sintomas("fatiga")
usuaria2.registrar_sintomas("cambios de humor")
usuaria2.generar_alerta()

usuaria3.actualivar_hormonas(50)
usuaria3.generar_alerta()

print("Resumen final:")
usuaria1.mostrar_perfil()
usuaria2.mostrar_perfil()
usuaria3.mostrar_perfil()
