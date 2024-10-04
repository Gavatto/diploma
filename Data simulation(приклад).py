import random
import time
from datetime import datetime

def generate_solar_data(panel_id):
    # Симуляція виробленої і спожитої потужності (в кВт)
    produced_energy = round(random.uniform(1.5, 3.5), 2)  # Виробництво енергії
    consumed_energy = round(random.uniform(1.0, 2.0), 2)  # Споживання енергії
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Мітка часу
    return {
        "panel_id": panel_id,
        "produced_energy": produced_energy,
        "consumed_energy": consumed_energy,
        "timestamp": timestamp
    }

# Пример генерации данных
for i in range(5):
    data = generate_solar_data(panel_id="SP-001")
    print(data)
    time.sleep(1)
