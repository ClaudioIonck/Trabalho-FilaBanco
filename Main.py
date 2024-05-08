# fila de clientes
def monitorar_fila():
    while time.time() - inicio_tempo < TEMPO_DE_SIMULACAO / TEMPO_FATOR:
        if not fila_de_clientes.empty():
            fila_snapshot = list(fila_de_clientes.queue)  # Cria uma cópia da fila atual
            clientes_ids = [cliente.id for cliente in fila_snapshot]
            print(f"Clientes na fila: {len(clientes_ids)} - IDs: {clientes_ids}")
        time.sleep(1)  # Intervalo de 1 segundo para a atualização


import threading
import time
import random
import queue
from statistics import mean

# Definindo os parâmetros
INTERVALO_CHEGADA_MIN = 5           # segundos
INTERVALO_CHEGADA_MAX = 50          # segundos
TEMPO_ATENDIMENTO_MIN = 30          # segundos
TEMPO_ATENDIMENTO_MAX = 120         # segundos
TEMPO_DE_SIMULACAO = 2 * 60 * 60    # 2 horas simuladas em segundos = 2min de simulação em vez de 2h
TEMPO_FATOR = 60                    # fator de redução de tempo para a simulação 1/60

NUM_CAIXAS = 2                      # número inicial de caixas = threads

# Threads e filas
fila_de_clientes = queue.Queue()
estatisticas = []
tempo_de_trabalho_caixa = [0] * NUM_CAIXAS  # Tempo de trabalho do caixa

class Cliente:
    next_id = 1  # ID cliente

    def __init__(self):
        self.id = Cliente.next_id
        Cliente.next_id += 1
        self.tempo_chegada = time.time()
        self.tempo_atendimento = random.randint(TEMPO_ATENDIMENTO_MIN, TEMPO_ATENDIMENTO_MAX) / TEMPO_FATOR
        self.tempo_inicio_atendimento = None
        self.tempo_fim_atendimento = None
        print(f"Cliente {self.id} entrou no banco.")

    def iniciar_atendimento(self):
        self.tempo_inicio_atendimento = time.time()
        espera = self.tempo_inicio_atendimento - self.tempo_chegada
        print(f"Cliente {self.id} começou a ser atendido após {espera:.2f} segundos de espera.")

    def finalizar_atendimento(self):
        self.tempo_fim_atendimento = time.time()
        duracao = self.tempo_fim_atendimento - self.tempo_inicio_atendimento
        print(f"Cliente {self.id} foi atendido por {duracao:.2f} segundos e está saindo do banco.")

def cliente_chegando():
    while True:
        time.sleep(random.randint(INTERVALO_CHEGADA_MIN, INTERVALO_CHEGADA_MAX) / TEMPO_FATOR)
        novo_cliente = Cliente()
        fila_de_clientes.put(novo_cliente)
        if time.time() - inicio_tempo > TEMPO_DE_SIMULACAO / TEMPO_FATOR:
            break

def caixa(index):
    while time.time() - inicio_tempo < TEMPO_DE_SIMULACAO / TEMPO_FATOR:
        try:
            cliente = fila_de_clientes.get(timeout=1)
            cliente.iniciar_atendimento()
            start_time = time.time()
            time.sleep(cliente.tempo_atendimento)
            cliente.finalizar_atendimento()
            end_time = time.time()
            fila_de_clientes.task_done()
            tempo_de_trabalho_caixa[index] += (end_time - start_time)
            estatisticas.append((cliente.tempo_inicio_atendimento - cliente.tempo_chegada,
                                 cliente.tempo_fim_atendimento - cliente.tempo_inicio_atendimento,
                                 cliente.tempo_fim_atendimento - cliente.tempo_chegada))
        except queue.Empty:
            continue

def format_time_minutes_real(seconds):
    # Converte segundos fatorados
    real_seconds = seconds * TEMPO_FATOR
    minutes = real_seconds / 60
    return f"{minutes:.2f} min"

inicio_tempo = time.time()

# Iniciar thread de chegada de clientes
thread_cliente = threading.Thread(target=cliente_chegando)
thread_cliente.start()

# Iniciar a thread de monitoramento da fila
thread_monitor_fila = threading.Thread(target=monitorar_fila)
thread_monitor_fila.start()

# Iniciar threads dos caixas
threads_caixas = []
for i in range(NUM_CAIXAS):
    thread = threading.Thread(target=caixa, args=(i,))
    thread.start()
    threads_caixas.append(thread)

# Esperar a thread de clientes terminar
thread_cliente.join()

# Esperar a thread de monitoramento da fila terminar
thread_monitor_fila.join()

# Esperar todas as threads de caixa terminarem
for thread in threads_caixas:
    thread.join()

# Processando as estatísticas e utilização
tempos_de_espera = [s[0] for s in estatisticas]
tempos_de_atendimento = [s[1] for s in estatisticas]
tempos_totais = [s[2] for s in estatisticas]

tempo_simulado = TEMPO_DE_SIMULACAO / TEMPO_FATOR
utilizacao_caixas = [(100 * t / tempo_simulado) for t in tempo_de_trabalho_caixa]

print("\n\n\n")

print("Quantos clientes foram atendidos:", len(estatisticas))
print("Tempo máximo de espera:", format_time_minutes_real(max(tempos_de_espera)))
print("Tempo máximo de atendimento:", format_time_minutes_real(max(tempos_de_atendimento)))
print("Tempo médio dentro do banco:", format_time_minutes_real(mean(tempos_totais)))
print("Tempo médio de espera na fila:", format_time_minutes_real(mean(tempos_de_espera)))
print("Objetivo de 2 minutos de espera alcançado:", max(tempos_de_espera) <= 120 / TEMPO_FATOR)

for i, uso in enumerate(utilizacao_caixas):
    print(f"Utilização do caixa {i+1}: {uso:.2f}%")


print("FIM")