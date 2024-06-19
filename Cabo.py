import tkinter as tk
from tkinter import font
import serial
import json

# Inicializando a conexão serial e definindo o estado inicial dos dispositivos
arduino = None
cooler_state = False
humidifier_state = False
auto_mode_state = False  # Estado inicial do modo automático

# Função para ler os dados do Arduino


def read_data():
    global arduino
    try:
        if arduino and arduino.in_waiting > 0:
            data = arduino.readline()
            return data.strip()  # Remove espaços em branco no início e no fim
        else:
            return None
    except serial.SerialException as se:
        print(f"Serial exception while reading data: {se}")
    except Exception as e:
        print(f"Error reading data: {e}")
    return None

# Função para atualizar os dados dos sensores na interface


def update_data():
    data = read_data()
    if data:
        try:
            # Decodifica os dados recebidos como UTF-8
            data_str = data.decode('utf-8')
            sensor_data = json.loads(data_str)

            # Verifica se os dados recebidos são um dicionário com as chaves esperadas
            if 'SensorInt' in sensor_data and 'SensorExt' in sensor_data:
                temp_int = sensor_data['SensorInt'].get('Temperatura', '--')
                humid_int = sensor_data['SensorInt'].get('Umidade', '--')
                temp_ext = sensor_data['SensorExt'].get('Temperatura', '--')
                humid_ext = sensor_data['SensorExt'].get('Umidade', '--')

                # Atualiza os rótulos na interface com os dados do sensor
                temp_label_1.config(
                    text=f"Sensor Interno - Temperatura: {temp_int} °C")
                humidity_label_1.config(
                    text=f"Sensor Interno - Umidade: {humid_int} %")
                temp_label_2.config(
                    text=f"Sensor Externo - Temperatura: {temp_ext} °C")
                humidity_label_2.config(
                    text=f"Sensor Externo - Umidade: {humid_ext} %")
            else:
                print("Dados recebidos incompletos ou inválidos")
                # Lidar com dados recebidos incorretos
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            # Lidar com erro de decodificação JSON
            temp_label_1.config(text="Erro: Dados incorretos",
                                font=label_font, fg="red")
            humidity_label_1.config(text="", font=label_font)
            temp_label_2.config(text="", font=label_font)
            humidity_label_2.config(text="", font=label_font)
        except UnicodeDecodeError as ud:
            print(f"Unicode decode error: {ud}")
            # Lidar com erro de decodificação Unicode
    root.after(1000, update_data)

# Função para ligar e desligar o cooler


def toggle_cooler():
    global cooler_state
    cooler_state = not cooler_state
    try:
        if cooler_state:
            print("Enviando comando para ligar o cooler")
            arduino.write(b'L')  # Envia 'L' para ligar o cooler
            cooler_button.config(text="Cooler Ligado", bg="green", width=15)
        else:
            print("Enviando comando para desligar o cooler")
            arduino.write(b'K')  # Envia 'K' para desligar o cooler
            cooler_button.config(text="Cooler Desligado", bg="red", width=15)
    except Exception as e:
        print(f"Error sending command: {e}")

# Função para alternar o estado do umidificador


def toggle_humidifier():
    global humidifier_state
    try:
        humidifier_state = not humidifier_state
        if humidifier_state:
            print("Enviando comando para ligar o umidificador")
            arduino.write(b'U')  # Envia 'U' para ligar o umidificador
            humidifier_button.config(
                text="Umidificador Ligado", bg="green", width=20)
        else:
            print("Enviando comando para desligar o umidificador")
            arduino.write(b'V')  # Envia 'V' para desligar o umidificador
            humidifier_button.config(
                text="Umidificador Desligado", bg="red", width=20)
    except Exception as e:
        print(f"Error sending command: {e}")

# Função para alternar o modo automático


def toggle_auto_mode():
    global auto_mode_state
    auto_mode_state = not auto_mode_state
    try:
        if auto_mode_state:
            print("Enviando comando para ativar o modo automático")
            arduino.write(b'A')  # Envia 'A' para ativar o modo automático
            auto_mode_button.config(
                text="Modo Automático Ativado", bg="blue", width=25)
        else:
            print("Enviando comando para desativar o modo automático")
            arduino.write(b'M')  # Envia 'M' para desativar o modo automático
            auto_mode_button.config(
                text="Modo Automático Desativado", bg="orange", width=25)
    except Exception as e:
        print(f"Error sending command: {e}")


# Inicializando a conexão serial com o Arduino
try:
    arduino = serial.Serial('COM6', 9600, timeout=1)
    print("Conexão com o Arduino estabelecida")
except Exception as e:
    print(f"Erro ao abrir porta serial: {e}")

# Configurações da interface gráfica
root = tk.Tk()
root.title("Controle de Ambiente")
root.geometry("800x600")  # Ajustando o tamanho da janela
root.configure(bg="#f0f0f0")  # Alterando a cor de fundo da janela

# Configurações de fonte
title_font = font.Font(family="Helvetica", size=24, weight="bold")
label_font = font.Font(family="Helvetica", size=24)
# Reduzindo o tamanho da fonte dos botões
button_font = font.Font(family="Helvetica", size=20)

# Título
title_label = tk.Label(root, text="Controle de Ambiente",
                       font=title_font, bg="#f0f0f0")
title_label.pack(pady=20)

# Adicionando cor de fundo ao frame
frame = tk.Frame(root, padx=20, pady=20, bg="#e0e0e0", relief=tk.RIDGE, bd=2)
frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Layout dos sensores
sensor_frame = tk.Frame(frame, bg="#e0e0e0")
sensor_frame.pack(pady=10)

temp_label_1 = tk.Label(sensor_frame, text="Sensor Interno - Temperatura: --",
                        font=label_font, bg="#e0e0e0")
temp_label_1.grid(row=0, column=0, padx=20, pady=5)

humidity_label_1 = tk.Label(sensor_frame, text="Sensor Interno - Umidade: --",
                            font=label_font, bg="#e0e0e0")
humidity_label_1.grid(row=1, column=0, padx=20, pady=5)

temp_label_2 = tk.Label(sensor_frame, text="Sensor Externo - Temperatura: --",
                        font=label_font, bg="#e0e0e0")
temp_label_2.grid(row=0, column=1, padx=20, pady=5)

humidity_label_2 = tk.Label(sensor_frame, text="Sensor Externo - Umidade: --",
                            font=label_font, bg="#e0e0e0")
humidity_label_2.grid(row=1, column=1, padx=20, pady=5)

# Botões para ligar/desligar o cooler e o umidificador
button_frame = tk.Frame(frame, bg="#e0e0e0")
button_frame.pack(side=tk.BOTTOM, pady=10)

cooler_button = tk.Button(button_frame, text="Ligar Cooler", font=button_font, command=toggle_cooler,
                          bg="#007acc", fg="white", activebackground="#005f99", activeforeground="white", width=15)
cooler_button.pack(side=tk.LEFT, padx=10, pady=10)

humidifier_button = tk.Button(button_frame, text="Ligar Umidificador", font=button_font,
                              command=toggle_humidifier, bg="#007acc", fg="white", activebackground="#005f99", activeforeground="white", width=20)
humidifier_button.pack(side=tk.LEFT, padx=10, pady=10)

# Botão para alternar o modo automático
auto_mode_button = tk.Button(button_frame, text="Modo Automático", font=button_font,
                             command=toggle_auto_mode, bg="orange", fg="white", activebackground="#ff6600", activeforeground="white", width=15)
auto_mode_button.pack(side=tk.TOP, pady=10)

# Função principal para manter a interface em execução


def main():
    # Atualiza os dados periodicamente
    update_data()
    root.after(1000, main)


# Inicializa a função principal
main()

# Inicia o loop principal da interface gráfica
root.mainloop()

# Fecha a conexão serial quando a interface for fechada
if arduino:
    arduino.close()
    print("Conexão com o Arduino fechada")
