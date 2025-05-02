import pytest
from src.main import RiskSimulator  # Asegúrate de que esta importación sea correcta según tu estructura

class TestPriorityCalculation:
    """Pruebas unitarias para el cálculo de prioridad de riesgos."""
    
    @pytest.fixture
    def simulator(self):
        """Fixture que proporciona una instancia del simulador para las pruebas."""
        return RiskSimulator()
    
    # Pruebas para el cálculo correcto del producto probabilidad × impacto
    @pytest.mark.parametrize("probability, impact, expected", [
        (1, 1, 1),    # Valor mínimo
        (5, 5, 25),    # Valores medios
        (10, 10, 100), # Valor máximo
        (3, 7, 21),    # Valores asimétricos
        (7, 3, 21),    # Valores asimétricos inversos
        (10, 1, 10),   # Máxima probabilidad, mínimo impacto
        (1, 10, 10)    # Mínima probabilidad, máximo impacto
    ])
    def test_priority_value_calculation(self, simulator, probability, impact, expected):
        """Verifica que el cálculo de prioridad devuelva el producto correcto."""
        priority_value, _ = simulator.calculate_priority(probability, impact)
        assert priority_value == expected, \
            f"Se esperaba {expected} pero se obtuvo {priority_value} para {probability}×{impact}"
    
    # Pruebas para la categorización correcta según rangos
    @pytest.mark.parametrize("probability, impact, expected_category", [
        (1, 1, "bajo"),     # 1 → bajo
        (3, 10, "bajo"),    # 30 → bajo (límite inferior)
        (5, 6, "bajo"),     # 30 → bajo (límite superior)
        (5, 7, "medio"),    # 35 → medio
        (7, 10, "medio"),   # 70 → medio (límite superior)
        (8, 9, "alto"),     # 72 → alto
        (10, 10, "alto")    # 100 → alto
    ])
    def test_priority_categorization(self, simulator, probability, impact, expected_category):
        """Verifica que la categorización de prioridad sea correcta."""
        _, priority_category = simulator.calculate_priority(probability, impact)
        assert priority_category == expected_category, \
            f"Se esperaba categoría '{expected_category}' para {probability}×{impact}={probability*impact}"
    
    # Pruebas para validar el manejo de valores fuera de rango
    @pytest.mark.parametrize("probability, impact", [
        (0, 5),   # Probabilidad demasiado baja
        (11, 5),  # Probabilidad demasiado alta
        (5, 0),   # Impacto demasiado bajo
        (5, 11)   # Impacto demasiado alto
    ])
    def test_invalid_inputs(self, simulator, probability, impact):
        """Verifica que se lance una excepción con valores fuera de rango."""
        with pytest.raises(ValueError, match="Probabilidad e impacto deben estar entre 1 y 10"):
            simulator.calculate_priority(probability, impact)
    
    # Prueba de propiedades para verificar consistencia
    @pytest.mark.parametrize("probability, impact", [
        (p, i) for p in range(1, 11) for i in range(1, 11)
    ])
    def test_priority_properties(self, simulator, probability, impact):
        """Verifica propiedades generales del cálculo de prioridad."""
        priority_value, priority_category = simulator.calculate_priority(probability, impact)
        
        # Propiedad 1: El valor debe ser el producto
        assert priority_value == probability * impact
        
        # Propiedad 2: La categoría debe corresponder al valor
        if priority_value <= 30:
            assert priority_category == "bajo"
        elif priority_value <= 70:
            assert priority_category == "medio"
        else:
            assert priority_category == "alto"