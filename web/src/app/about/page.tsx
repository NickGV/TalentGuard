import { Card, CardContent } from "@/components/ui/card";

export default function AboutPage() {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-[#2D3436]">
        📋 Acerca del proyecto
      </h1>

      {/* Proyecto */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-semibold text-[#2D3436]">
            🏢 El proyecto
          </h2>
          <p className="text-muted-foreground leading-relaxed">
            <strong>TalentGuard</strong> es una aplicación de Machine Learning
            diseñada para predecir el riesgo de rotación de empleados. Utiliza
            un modelo de <strong>Regresión Logística</strong> entrenado sobre el
            dataset <strong>IBM HR Analytics Employee Attrition &amp;
            Performance</strong>, que contiene información de 1,470 empleados y
            43 variables.
          </p>
          <p className="text-muted-foreground leading-relaxed">
            El objetivo es proporcionar a los equipos de Recursos Humanos una
            herramienta basada en datos para identificar talento en riesgo y
            tomar acciones de retención tempranas.
          </p>
        </CardContent>
      </Card>

      {/* Hallazgos clave */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-semibold text-[#2D3436]">
            🔍 Hallazgos clave
          </h2>
          <ul className="space-y-3 text-muted-foreground">
            <li className="flex gap-2">
              <span className="text-[#E17055] font-bold">•</span>
              <span>
                <strong>Las horas extra son el factor más influyente:</strong>{" "}
                los empleados que hacen horas extra tienen ~3 veces más
                probabilidad de abandono.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-[#E17055] font-bold">•</span>
              <span>
                <strong>Los primeros 3 años son críticos:</strong> el 61% de los
                abandonos ocurren en este período, lo que sugiere que las
                estrategias de retención deben empezar temprano.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-[#E17055] font-bold">•</span>
              <span>
                <strong>La satisfacción laboral importa:</strong> a menor
                satisfacción, mayor tasa de abandono. Los empleados con
                satisfacción "baja" abandonan al doble de la tasa promedio.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-[#E17055] font-bold">•</span>
              <span>
                <strong>El ingreso también influye:</strong> los empleados que
                abandonan se concentran en rangos salariales más bajos, aunque
                no es el único factor determinante.
              </span>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Limitaciones */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-semibold text-[#2D3436]">
            ⚠️ Limitaciones
          </h2>
          <ul className="space-y-3 text-muted-foreground">
            <li className="flex gap-2">
              <span className="text-[#F39C12] font-bold">•</span>
              <span>
                <strong>Desbalance de clases:</strong> solo el 16% de los casos
                son abandonos, lo que limita la precisión en la clase
                minoritaria (F1-Yes: 0.473).
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-[#F39C12] font-bold">•</span>
              <span>
                <strong>Datos sintéticos:</strong> el dataset IBM HR Analytics
                es generado sintéticamente, no representa datos reales de una
                organización.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-[#F39C12] font-bold">•</span>
              <span>
                <strong>Sin variables temporales:</strong> el modelo no captura
                cambios en el comportamiento del empleado a lo largo del tiempo.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-[#F39C12] font-bold">•</span>
              <span>
                <strong>Modelo lineal:</strong> la Regresión Logística asume
                relaciones lineales entre las variables y la probabilidad de
                abandono.
              </span>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Próximos pasos */}
      <Card>
        <CardContent className="p-6 space-y-4">
          <h2 className="text-xl font-semibold text-[#2D3436]">
            🚀 Próximos pasos
          </h2>
          <ul className="space-y-3 text-muted-foreground">
            <li className="flex gap-2">
              <span className="text-[#00B894] font-bold">→</span>
              <span>
                Explorar modelos más complejos (Random Forest, XGBoost) para
                mejorar el F1-Yes.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-[#00B894] font-bold">→</span>
              <span>
                Incorporar técnicas de balanceo como SMOTE para mejorar la
                detección de abandonos.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-[#00B894] font-bold">→</span>
              <span>
                Agregar datos temporales y seguimiento longitudinal de
                empleados para predicciones más dinámicas.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-[#00B894] font-bold">→</span>
              <span>
                Desplegar la aplicación en la nube para acceso del equipo de RH.
              </span>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Ethical warning */}
      <Card className="border-amber-200 bg-amber-50">
        <CardContent className="p-6 space-y-3">
          <h2 className="text-lg font-semibold text-amber-800">
            ⚖️ Uso ético y responsable
          </h2>
          <div className="text-sm text-amber-700 leading-relaxed space-y-2">
            <p>
              Esta herramienta está diseñada como un <strong>apoyo a la
              decisión</strong>, no como un sustituto del juicio humano.
            </p>
            <p>
              Las predicciones del modelo deben ser interpretadas por personal
              capacitado de Recursos Humanos y nunca deben usarse como único
              criterio para:
            </p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Decisiones de despido o contratación</li>
              <li>Evaluaciones de desempeño</li>
              <li>Decisiones de compensación o promoción</li>
              <li>Juicios definitivos sobre la carrera de un empleado</li>
            </ul>
            <p>
              El modelo es una herramienta estadística que aprende de patrones
              históricos y puede contener sesgos presentes en los datos de
              entrenamiento. La responsabilidad final de las decisiones de
              personal recae siempre en las personas y la organización.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
