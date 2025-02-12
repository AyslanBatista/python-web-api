import time
import concurrent.futures

def consulta_dados():  # I/O bound
    print("Consultando dados...")
    time.sleep(2)  # Fazendo select no BD
    return "dados"


def processa_dados(dados):  # CPU bound
    print("Processando dados...")
    time.sleep(2)  # calculando alguma coisa com os dados


def grava_log():  # I/O bound
    print("Gravando log...")
    time.sleep(2)


def main():
    start = time.perf_counter()
    print("Inicio")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(consulta_dados) # 2 segundos esperando
        dados = future.result() # Espera o future termina de executar
        executor.submit(processa_dados, dados)
        
        
        executor.submit(grava_log)
        executor.submit(grava_log)
        executor.submit(grava_log)
        executor.submit(grava_log)
        executor.submit(grava_log)
        executor.submit(grava_log)
        executor.submit(grava_log)
    # executor.run
    
    print("Fim")
    finish = time.perf_counter()
    print(f"Finished in {round(finish-start, 2)} seconds")

main()
