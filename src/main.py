import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Tuple
import unittest
from datetime import datetime
import csv

class RiskSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Riesgos en Sprints Ágiles")
        self.root.geometry("1000x750")
        self.setup_ui()
        
        # Inicializar el simulador
        self.simulator = RiskSimulator()
        
    def setup_ui(self):
        """Configura todos los elementos de la interfaz gráfica."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración del Sprint", padding="10")
        config_frame.pack(fill=tk.X, pady=5)
        
        # Controles de configuración
        ttk.Label(config_frame, text="Número de Riesgos:").grid(row=0, column=0, sticky=tk.W)
        self.risk_count = tk.IntVar(value=5)
        ttk.Spinbox(config_frame, from_=1, to=20, textvariable=self.risk_count, width=5).grid(row=0, column=1, sticky=tk.W)
        
        # Botones de acción
        button_frame = ttk.Frame(config_frame)
        button_frame.grid(row=0, column=2, columnspan=4, padx=(20,0), sticky=tk.E)
        
        ttk.Button(button_frame, text="Simular Sprint", command=self.run_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Pruebas Unitarias", command=self.run_unit_tests).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exportar CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        
        # Panel de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados de la Simulación", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview para mostrar los riesgos
        self.tree = ttk.Treeview(results_frame, columns=('type', 'desc', 'prob', 'impact', 'priority', 'category', 'mitigation'), 
                                show='headings', selectmode='extended')
        
        # Configurar columnas
        columns = [
            ('type', 'Tipo', 100),
            ('desc', 'Descripción', 200),
            ('prob', 'Probabilidad', 100),
            ('impact', 'Impacto', 100),
            ('priority', 'Prioridad', 100),
            ('category', 'Categoría', 120),
            ('mitigation', 'Mitigación', 250)
        ]
        
        for col_id, col_text, col_width in columns:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=col_width, anchor=tk.W if col_id in ['desc', 'mitigation'] else tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para colores
        self.tree.tag_configure('high', background='#ffdddd')
        self.tree.tag_configure('medium', background='#fff3cd')
        self.tree.tag_configure('low', background='#d4edda')
        
        # Panel de estadísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estadísticas", padding="10")
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=6, wrap=tk.WORD, font=('Arial', 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para colores en estadísticas
        self.stats_text.tag_config('high', foreground='red', font=('Arial', 10, 'bold'))
        self.stats_text.tag_config('medium', foreground='orange', font=('Arial', 10, 'bold'))
        self.stats_text.tag_config('low', foreground='green', font=('Arial', 10, 'bold'))
        self.stats_text.tag_config('highlight', foreground='blue', font=('Arial', 10, 'bold'))
        
    def run_simulation(self):
        """Ejecuta la simulación y muestra los resultados."""
        try:
            num_risks = self.risk_count.get()
            sprint_risks = self.simulator.run_sprint_simulation(num_risks)
            
            self.clear_results()
            
            # Insertar nuevos datos
            for risk in sprint_risks:
                tag = risk['categoria_prioridad']
                self.tree.insert('', tk.END, values=(
                    risk['tipo'],
                    risk['descripcion'],
                    risk['probabilidad'],
                    risk['impacto'],
                    risk['valor_prioridad'],
                    risk['categoria_prioridad'],
                    risk['mitigacion']
                ), tags=(tag,))
            
            # Calcular estadísticas
            self.show_statistics(sprint_risks)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error durante la simulación:\n{str(e)}")
    
    def show_statistics(self, risks: List[Dict]):
        """Muestra estadísticas de la simulación."""
        total_risks = len(risks)
        high_risks = sum(1 for r in risks if r['categoria_prioridad'] == 'alto')
        medium_risks = sum(1 for r in risks if r['categoria_prioridad'] == 'medio')
        low_risks = sum(1 for r in risks if r['categoria_prioridad'] == 'bajo')
        
        avg_priority = sum(r['valor_prioridad'] for r in risks) / total_risks if total_risks > 0 else 0
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        self.stats_text.insert(tk.END, "=== Resumen del Sprint ===\n", 'highlight')
        self.stats_text.insert(tk.END, f"Total de riesgos identificados: {total_risks}\n\n")
        
        self.stats_text.insert(tk.END, "Distribución de riesgos:\n")
        self.stats_text.insert(tk.END, f"• Alto: ", 'high')
        self.stats_text.insert(tk.END, f"{high_risks} ({high_risks/total_risks:.0%})\n", 'high')
        self.stats_text.insert(tk.END, f"• Medio: ", 'medium')
        self.stats_text.insert(tk.END, f"{medium_risks} ({medium_risks/total_risks:.0%})\n", 'medium')
        self.stats_text.insert(tk.END, f"• Bajo: ", 'low')
        self.stats_text.insert(tk.END, f"{low_risks} ({low_risks/total_risks:.0%})\n\n", 'low')
        
        self.stats_text.insert(tk.END, f"Prioridad promedio: {avg_priority:.1f}\n\n")
        
        # Mostrar el riesgo más crítico
        if risks:
            max_risk = max(risks, key=lambda x: x['valor_prioridad'])
            self.stats_text.insert(tk.END, "Riesgo más crítico:\n", 'highlight')
            self.stats_text.insert(tk.END, f"• Descripción: {max_risk['descripcion']}\n")
            self.stats_text.insert(tk.END, f"• Prioridad: {max_risk['valor_prioridad']} (")
            
            if max_risk['categoria_prioridad'] == 'alto':
                self.stats_text.insert(tk.END, "ALTO", 'high')
            elif max_risk['categoria_prioridad'] == 'medio':
                self.stats_text.insert(tk.END, "MEDIO", 'medium')
            else:
                self.stats_text.insert(tk.END, "BAJO", 'low')
                
            self.stats_text.insert(tk.END, ")\n")
            self.stats_text.insert(tk.END, f"• Mitigación sugerida: {max_risk['mitigacion']}\n")
        
        self.stats_text.config(state=tk.DISABLED)
    
    def run_unit_tests(self):
        """Ejecuta pruebas unitarias y muestra los resultados."""
        test_suite = unittest.TestLoader().loadTestsFromTestCase(TestRiskSimulator)
        test_result = unittest.TextTestRunner(stream=None, verbosity=2).run(test_suite)
        
        message = (
            f"Pruebas ejecutadas: {test_result.testsRun}\n"
            f"Fallidas: {len(test_result.failures)}\n"
            f"Errores: {len(test_result.errors)}"
        )
        
        if test_result.wasSuccessful():
            messagebox.showinfo("Resultado de Pruebas", f"¡Todas las pruebas pasaron!\n{message}")
        else:
            messagebox.showwarning("Resultado de Pruebas", f"Algunas pruebas fallaron:\n{message}")
    
    def export_to_csv(self):
        """Exporta los resultados a un archivo CSV."""
        if not self.tree.get_children():
            messagebox.showwarning("Sin datos", "No hay datos para exportar. Ejecute una simulación primero.")
            return
            
        try:
            filename = f"riesgos_sprint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Tipo', 'Descripción', 'Probabilidad', 'Impacto', 'Prioridad', 'Categoría', 'Mitigación'])
                
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)['values'])
            
            messagebox.showinfo("Exportación exitosa", f"Los datos se exportaron correctamente a:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Error al exportar", f"No se pudo exportar el archivo:\n{str(e)}")
    
    def clear_results(self):
        """Limpia todos los resultados y estadísticas."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "Ejecute una simulación para ver los resultados...")
        self.stats_text.config(state=tk.DISABLED)


class RiskSimulator:
    """Clase del simulador de riesgos"""
    def __init__(self):
        self.risk_types = [
            "Técnico", 
            "Organizacional", 
            "Externo", 
            "Requisitos", 
            "Planificación"
        ]
        
        self.risk_descriptions = {
            "Técnico": [
                "Dependencias obsoletas",
                "Problemas de integración",
                "Dificultades técnicas imprevistas",
                "Falta de expertise técnico",
                "Tecnología no probada"
            ],
            "Organizacional": [
                "Cambio en los recursos asignados",
                "Problemas de comunicación",
                "Falta de compromiso del equipo",
                "Conflictos internos",
                "Rotación de personal"
            ],
            "Externo": [
                "Cambios en regulaciones",
                "Problemas con proveedores",
                "Factores del mercado",
                "Condiciones económicas",
                "Problemas legales"
            ],
            "Requisitos": [
                "Cambios en los requisitos",
                "Requisitos ambiguos",
                "Sobre-ingeniería",
                "Falta de claridad en objetivos",
                "Expectativas no realistas"
            ],
            "Planificación": [
                "Estimaciones incorrectas",
                "Sobrecompromiso",
                "Falta de priorización",
                "Dependencias externas no consideradas",
                "Plazos irreales"
            ]
        }
        
        self.mitigation_strategies = {
            "bajo": [
                "Monitorear el riesgo",
                "Documentar el riesgo",
                "Revisar en siguiente sprint",
                "Asignar responsable para seguimiento",
                "Incluir en backlog para revisión futura"
            ],
            "medio": [
                "Asignar responsable",
                "Plan de acción específico",
                "Revisión semanal",
                "Asignar recursos adicionales",
                "Realizar análisis de impacto detallado"
            ],
            "alto": [
                "Acción inmediata requerida",
                "Involucrar a stakeholders",
                "Replanificar sprint si es necesario",
                "Convocar reunión de emergencia",
                "Reasignar recursos prioritariamente"
            ]
        }
    
    def generate_risk(self) -> Dict[str, str]:
        """Genera un riesgo aleatorio con probabilidad e impacto."""
        risk_type = random.choice(self.risk_types)
        description = random.choice(self.risk_descriptions[risk_type])
        probability = random.randint(1, 10)
        impact = random.randint(1, 10)
        
        return {
            "tipo": risk_type,
            "descripcion": description,
            "probabilidad": probability,
            "impacto": impact
        }
    
    def calculate_priority(self, probability: int, impact: int) -> Tuple[int, str]:
        """
        Calcula la prioridad del riesgo (probabilidad × impacto) y la categoriza.
        """
        if not (1 <= probability <= 10) or not (1 <= impact <= 10):
            raise ValueError("Probabilidad e impacto deben estar entre 1 y 10")
        
        priority_value = probability * impact
        priority_category = self._categorize_priority(priority_value)
        
        return priority_value, priority_category
    
    def _categorize_priority(self, priority_value: int) -> str:
        """Categoriza la prioridad en bajo, medio o alto."""
        if priority_value <= 30:
            return "bajo"
        elif 31 <= priority_value <= 70:
            return "medio"
        else:
            return "alto"
    
    def suggest_mitigation(self, priority_category: str) -> str:
        """Sugiere una estrategia de mitigación basada en la categoría de prioridad."""
        return random.choice(self.mitigation_strategies[priority_category])
    
    def run_sprint_simulation(self, num_risks: int = 5) -> List[Dict]:
        """Ejecuta una simulación completa de un sprint con riesgos."""
        sprint_risks = []
        
        for _ in range(num_risks):
            risk = self.generate_risk()
            priority_value, priority_category = self.calculate_priority(
                risk["probabilidad"], 
                risk["impacto"]
            )
            mitigation = self.suggest_mitigation(priority_category)
            
            risk_result = {
                **risk,
                "valor_prioridad": priority_value,
                "categoria_prioridad": priority_category,
                "mitigacion": mitigation
            }
            
            sprint_risks.append(risk_result)
        
        return sprint_risks


class TestRiskSimulator(unittest.TestCase):
    """Pruebas unitarias para el simulador de riesgos."""
    
    def setUp(self):
        self.simulator = RiskSimulator()
    
    def test_calculate_priority(self):
        """Prueba el cálculo de prioridad y categorización."""
        test_cases = [
            ((2, 3), (6, "bajo")),
            ((5, 6), (30, "bajo")),
            ((5, 7), (35, "medio")),
            ((7, 10), (70, "medio")),
            ((8, 9), (72, "alto")),
            ((10, 10), (100, "alto"))
        ]
        
        for (prob, imp), (expected_val, expected_cat) in test_cases:
            with self.subTest(prob=prob, imp=imp):
                result_val, result_cat = self.simulator.calculate_priority(prob, imp)
                self.assertEqual(result_val, expected_val)
                self.assertEqual(result_cat, expected_cat)
    
    def test_invalid_inputs(self):
        """Prueba que se levanten errores con entradas inválidas."""
        with self.assertRaises(ValueError):
            self.simulator.calculate_priority(0, 5)
        
        with self.assertRaises(ValueError):
            self.simulator.calculate_priority(11, 5)
        
        with self.assertRaises(ValueError):
            self.simulator.calculate_priority(5, 0)
        
        with self.assertRaises(ValueError):
            self.simulator.calculate_priority(5, 11)
    
    def test_integration_flow(self):
        """Prueba de integración del flujo completo."""
        sprint_results = self.simulator.run_sprint_simulation(3)
        
        self.assertEqual(len(sprint_results), 3)
        
        for risk in sprint_results:
            self.assertIn("tipo", risk)
            self.assertIn("descripcion", risk)
            self.assertIn("probabilidad", risk)
            self.assertIn("impacto", risk)
            self.assertIn("valor_prioridad", risk)
            self.assertIn("categoria_prioridad", risk)
            self.assertIn("mitigacion", risk)
            
            calculated_value = risk["probabilidad"] * risk["impacto"]
            self.assertEqual(risk["valor_prioridad"], calculated_value)
            
            if calculated_value <= 30:
                expected_category = "bajo"
            elif 31 <= calculated_value <= 70:
                expected_category = "medio"
            else:
                expected_category = "alto"
            
            self.assertEqual(risk["categoria_prioridad"], expected_category)
            self.assertIn(risk["mitigacion"], self.simulator.mitigation_strategies[expected_category])


if __name__ == "__main__":
    root = tk.Tk()
    app = RiskSimulatorGUI(root)
    root.mainloop()