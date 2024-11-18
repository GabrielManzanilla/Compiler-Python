from itertools import product

def generate_all_combinations(civilizations, states_by_civilization, geography, structures, filename="combinaciones-sitios-arqueologicos.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for civ in civilizations:
            states = states_by_civilization[civ]
            # Create all combinations for each state, geography, and structure
            for state, geo, structure in product(states, geography, structures):
                file.write(f"Civilización: {civ} | Estado: {state} | Geografía: {geo} | Estructura: {structure}\n")

# Listas de criterios
civilizations = ["Olmeca", "Maya", "Teotihuacana", "Azteca o Mexica", "Tolteca", "Zapoteca"]
states_by_civilization = {
    "Olmeca": ["Veracruz", "Tabasco"],
    "Maya": ["Yucatán", "Quintana Roo", "Campeche", "Chiapas"],
    "Teotihuacana": ["Hidalgo"],
    "Azteca o Mexica": ["Ciudad de México", "Morelos", "Guerrero"],
    "Tolteca": ["Hidalgo", "Morelos", "Tlaxcala"],
    "Zapoteca": ["Oaxaca"]
}
geography = ["Montañas", "Meseta", "Valle", "Cavernas-Cuevas"]
structures = ["Pirámides", "Observatorios", "Templos", "Plazas ceremoniales"]

# Generar todas las combinaciones y guardarlas en el archivo
generate_all_combinations(civilizations, states_by_civilization, geography, structures)
