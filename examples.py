"""
Exemplos de uso - A.R.G.U.S.
Demonstra como usar os módulos individualmente
"""

# ============================================
# Exemplo 1: Usar o Monitor de Sistema
# ============================================

from monitor import monitor

# Obter dados do sistema
print("=== MONITORAMENTO DO SISTEMA ===")
cpu = monitor.get_cpu_usage()
ram = monitor.get_ram_usage()
gpu = monitor.get_gpu_usage()
disk = monitor.get_disk_usage()
temp = monitor.get_temperature()

print(f"CPU: {cpu}%")
print(f"RAM: {ram}%")
print(f"GPU: {gpu}%")
print(f"Disco: {disk}%")
print(f"Temperatura: {temp}°C")

# Obter processos suspeitos
suspicious = monitor.get_suspicious_processes()
print(f"\nProcessos com alto consumo: {len(suspicious)}")
for proc in suspicious:
    print(f"  - {proc['name']}: CPU {proc['cpu']}%")

# Verificar alertas
alerts = monitor.check_alerts()
if alerts:
    print(f"\nAlertas gerados:")
    for alert_type, message in alerts:
        print(f"  - {alert_type}: {message}")


# ============================================
# Exemplo 2: Monitorar Rede
# ============================================

from network import network

print("\n=== INFORMAÇÕES DE REDE ===")
net_info = network.get_all_network_info()
print(f"IP Público: {net_info['public_ip']}")
print(f"Localização: {net_info['city']}, {net_info['country']}")
print(f"Coordenadas: {net_info['latitude']}, {net_info['longitude']}")
print(f"Conectado: {net_info['is_online']}")
print(f"Hostname: {net_info['hostname']}")
print(f"MAC Address: {net_info['mac_address']}")


# ============================================
# Exemplo 3: Usar Banco de Dados
# ============================================

from database import db

print("\n=== BANCO DE DADOS ===")

# Log de estatísticas
db.log_system_stats(
    cpu_usage=45.2,
    ram_usage=60.5,
    gpu_usage=30.0,
    disk_usage=55.0,
    temperature=56.3,
    internet_speed_down=523.5,
    internet_speed_up=211.3,
    processes_count=198
)
print("✓ Estatísticas registradas")

# Log de alerta
db.log_alert('CPU_ALTA', 'CPU excedeu 80%', 'HIGH')
print("✓ Alerta registrado")

# Recuperar histórico
latest_stats = db.get_latest_stats(limit=10)
print(f"✓ {len(latest_stats)} registros no histórico")

recent_alerts = db.get_recent_alerts(limit=5)
print(f"✓ {len(recent_alerts)} alertas recentes")


# ============================================
# Exemplo 4: Usar IA Conversacional
# ============================================

from ai import ai

print("\n=== ASSISTENTE IA ===")

# Saudação
greeting = ai.get_greeting()
print(f"A.R.G.U.S.: {greeting}")

# Análise do sistema
stats = monitor.get_all_stats()
analysis = ai.analyze_system(stats)
print(f"\nAnálise:\n{analysis}")

# Conversar
messages = [
    "Olá",
    "Como está meu sistema?",
    "Tudo bem?",
    "Obrigado",
]

print("\nConversa:")
for msg in messages:
    response = ai.get_response(msg)
    print(f"Você: {msg}")
    print(f"A.R.G.U.S.: {response}\n")


# ============================================
# Exemplo 5: Usar Gráficos
# ============================================

from graphs import graph_manager
import time

print("\n=== GRÁFICOS ===")

# Adicionar pontos de dados
for i in range(10):
    stats = monitor.get_all_stats()
    graph_manager.add_data_point(
        stats['cpu'],
        stats['ram'],
        stats['gpu'],
        stats['temperature']
    )
    time.sleep(1)

print(f"✓ {len(graph_manager.cpu_data)} pontos coletados")

# Criar gráficos (comentado porque requer GUI)
# fig = graph_manager.create_combined_graph()
# fig.show()


# ============================================
# Exemplo 6: Monitoramento Contínuo
# ============================================

import threading

def monitoring_loop_example():
    """Exemplo de loop de monitoramento"""
    print("\n=== MONITORAMENTO CONTÍNUO (5 segundos) ===")
    
    for i in range(5):
        stats = monitor.get_all_stats()
        print(f"\n[{i+1}/5] CPU: {stats['cpu']:.1f}% | RAM: {stats['ram']:.1f}% | Temp: {stats['temperature']:.1f}°C")
        
        # Log no banco
        db.log_system_stats(
            stats['cpu'], stats['ram'], stats['gpu'], stats['disk'],
            stats['temperature'], 0, 0, stats['processes']
        )
        
        time.sleep(1)

# Descomentar para testar
# monitoring_loop_example()


# ============================================
# Exemplo 7: Teste de Velocidade (Async)
# ============================================

def speed_test_example():
    """Exemplo de teste de velocidade em thread separada"""
    print("\n=== TESTE DE VELOCIDADE ===")
    print("Iniciando... (pode levar alguns minutos)")
    
    def on_complete(result):
        if result:
            print(f"✓ Download: {result['download']:.2f} Mbps")
            print(f"✓ Upload: {result['upload']:.2f} Mbps")
        else:
            print("✗ Erro no teste")
    
    network.test_speed_async(on_complete)

# Descomentar para testar
# speed_test_example()
# time.sleep(300)  # Aguardar resultado


print("\n✓ Exemplos concluídos!")
