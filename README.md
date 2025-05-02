# Simulador de Riesgos en Sprints Ágiles

## Descripción

Este proyecto es un simulador de riesgos para metodologías ágiles que genera escenarios aleatorios de riesgos durante sprints, calcula su prioridad y sugiere estrategias de mitigación.

## Características principales

- Generación automática de riesgos aleatorios
- Cálculo de prioridad (probabilidad × impacto)
- Categorización de riesgos (bajo, medio, alto)
- Sugerencias de estrategias de mitigación
- Interfaz gráfica intuitiva
- Sistema de pruebas unitarias

## Requisitos del sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/desarrollo-simulador.git
cd desarrollo-simulador
```

2. Crea y activa un entorno virtual (recomendado):
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución del programa

Para iniciar el simulador con interfaz gráfica:
```bash
python src/main.py
```

## Estructura del proyecto

```
desarrollo-simulador/
├── src/                  # Código fuente principal
│   ├── main.py           # Clase principal RiskSimulator
├── tests/                # Pruebas automatizadas
│   └── test_*.py         # Archivos de pruebas
└── README.md             # Este archivo
```

## Configuración de pruebas

### Dependencias para testing

Instala las dependencias de desarrollo:
```bash
python -m pip install --user pytest pytest-cov
```

### Ejecución de pruebas

Para ejecutar todas las pruebas:
```bash
pytest tests/
```

Para ejecutar pruebas con reporte de cobertura:
```bash
pytest --cov=src --cov-report=term-missing tests/
```

### Tipos de pruebas implementadas

1. **Pruebas unitarias**:
   - Cálculo de prioridad
   - Categorización de riesgos
   - Generación de riesgos

2. **Pruebas de integración**:
   - Flujo completo del simulador
   - Interacción entre componentes

## Ejemplo de salida del simulador

```
=== Simulación de Sprint ===
Riesgos generados: 5
- Alto: 1 (20%)
- Medio: 2 (40%)
- Bajo: 2 (40%)

Prioridad promedio: 45.2

Riesgo más crítico:
Descripción: Problemas de integración
Prioridad: 80 (ALTO)
Mitigación: Acción inmediata requerida
```

## Contribución

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Video

[Ver video explicativo en YT](https://youtu.be/s7upWVPwXd8)

## Autores
* José Fernando Usui
* Luciana Rojas
* Ezequiel Neyen Troche