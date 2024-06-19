import tkinter as tk
from tkinter import font
import serial
import json
import time

# Inicializando a conexão serial e definindo o estado inicial dos dispositivos
bluetooth = None
cooler_state = False
humidifier_state = False

# Função para ler os dados do dispositivo conectado


def read_data():
    try:
        if bluetooth.in_waiting > 0:
            data = bluetooth.readline().decode().strip()
            print(f"Received data: {data}")  # Debugging statement
            return data
        else:
            return None
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

# Função para atualizar os dados dos sensores na interface


def update_data():
    data = read_data()
    if data:
        try:
            # Parse the received JSON data
            sensor_data = json.loads(data)
            # Update the labels with the sensor data
            temp_label_1.config(
                text="Sensor 1 - Temperatura: {} °C".format(sensor_data['Sensor1']['Temperatura']))
            humidity_label_1.config(
                text="Sensor 1 - Umidade: {} %".format(sensor_data['Sensor1']['Umidade']))
            temp_label_2.config(
                text="Sensor 2 - Temperatura: {} °C".format(sensor_data['Sensor2']['Temperatura']))
            humidity_label_2.config(
                text="Sensor 2 - Umidade: {} %".format(sensor_data['Sensor2']['Umidade']))
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            # Handle the JSON decoding error
            temp_label_1.config(text="Erro: Dados incorretos",
                                font=label_font, fg="red")
            humidity_label_1.config(text="", font=label_font)
            temp_label_2.config(text="", font=label_font)
            humidity_label_2.config(text="", font=label_font)
    root.after(1000, update_data)

# Função para ligar e desligar o cooler


def toggle_cooler():
    global cooler_state
    cooler_state = not cooler_state
    try:
        if cooler_state:
            print("Enviando comando para ligar o cooler")
            bluetooth.write(b'L')  # Envia 'L' para ligar o cooler
            cooler_button.config(text="Cooler Ligado", bg="green", width=15)
        else:
            print("Enviando comando para desligar o cooler")
            bluetooth.write(b'K')  # Envia 'K' para desligar o cooler
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
            # Envia 'U' e 'V' rapidamente para simular um clique
            bluetooth.write(b'U')
            humidifier_button.config(
                text="Umidificador Ligado", bg="green", width=20)
        else:
            print("Enviando comando para desligar o umidificador")
            bluetooth.write(b'V')  # Envia 'V' para desligar o umidificador
            humidifier_button.config(
                text="Umidificador Desligado", bg="red", width=20)
    except Exception as e:
        print(f"Error sending command: {e}")


# Inicializando a conexão serial
try:
    bluetooth = serial.Serial('COM9', 9600, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")

# Configurações da interface gráfica
root = tk.Tk()
root.title("Controle de Ambiente")
root.geometry("800x600")  # Ajustando o tamanho da janela
root.configure(bg="#f0f0f0")  # Alterando a cor de fundo da janela

# Configurações de fonte
title_font = font.Font(family="Helvetica", size=24, weight="bold")
label_font = font.Font(family="Helvetica", size=25)
button_font = font.Font(family="Helvetica", size=30)

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

temp_label_1 = tk.Label(sensor_frame, text="Sensor 1 - Temperatura: --",
                        font=label_font, bg="#e0e0e0")
temp_label_1.grid(row=0, column=0, padx=20, pady=5)

humidity_label_1 = tk.Label(sensor_frame, text="Sensor 1 - Umidade: --",
                            font=label_font, bg="#e0e0e0")
humidity_label_1.grid(row=1, column=0, padx=20, pady=5)

temp_label_2 = tk.Label(sensor_frame, text="Sensor 2 - Temperatura: --",
                        font=label_font, bg="#e0e0e0")
temp_label_2.grid(row=0, column=1, padx=20, pady=5)

humidity_label_2 = tk.Label(sensor_frame, text="Sensor 2 - Umidade: --",
                            font=label_font, bg="#e0e0e0")
humidity_label_2.grid(row=1, column=1, padx=20, pady=5)

# Botões para ligar/desligar o cooler e o umidificador
button_frame = tk.Frame(frame, bg="#e0e0e0")
button_frame.pack(pady=10)

cooler_button = tk.Button(button_frame, text="Ligar Cooler", font=button_font, command=toggle_cooler,
                          bg="#007acc", fg="white", activebackground="#005f99", activeforeground="white")
cooler_button.grid(row=0, column=0, padx=10, pady=10)

humidifier_button = tk.Button(button_frame, text="Ligar Umidificador", font=button_font,
                              command=toggle_humidifier, bg="#007acc", fg="white", activebackground="#005f99", activeforeground="white")
humidifier_button.grid(row=0, column=1, padx=10, pady=10)

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
bluetooth.close()
