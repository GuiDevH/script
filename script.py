import time
from PIL import ImageGrab
import easyocr
import numpy as np
import pyautogui

# Inicializa o OCR uma vez
reader = easyocr.Reader(['en'])


# --- Função para detectar se algo apareceu sobre o fundo azul ---
def detectar_objeto_sobre_fundo(x, y, cor_fundo=(207, 255, 255), limite=80):
    imagem = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
    pixel = imagem.getpixel((0, 0))
    diferenca = sum(abs(pixel[i] - cor_fundo[i]) for i in range(3)) / 3

    if diferenca > limite:
        print(f"[OBJETO DETECTADO] Pixel mudou bastante ({pixel}), Δ≈{diferenca:.1f}")
        return True
    else:
        return False


# --- CONFIGURAÇÕES DO PIXEL ---
pixel_pos = (572, 548)
cor_fundo = (207, 255, 255)
pixel_limite = 80

# --- CONTADOR DE CICLOS ---
contador_ciclos = 0


# --- LOOP PRINCIPAL ---
while True:
    print("Executando cliques iniciais do bloco...")
    time.sleep(1)
    pyautogui.click(1050, 970)
    time.sleep(0.5)
    pyautogui.click(139, 863)
    time.sleep(0.5)

    # Loop de 3 execuções
    for i in range(3):
        print(f"Execução {i + 1}/3: Prepare a tela. Captura ocorrerá em 5 segundos...")
        time.sleep(4)

        pyautogui.click(1050, 970)
        time.sleep(0.5)
        pyautogui.click(139, 863)
        time.sleep(2)

        # --- Captura da tela e OCR ---
        regiao_numeros = (192, 34, 1438, 289)
        imagem = ImageGrab.grab(bbox=regiao_numeros)
        imagem_np = np.array(imagem.convert('RGB'))
        resultados = reader.readtext(imagem_np)

        numeros_encontrados = []
        for (_, texto, _) in resultados:
            for char in texto:
                if char in '1234':
                    numeros_encontrados.append(int(char))
        numeros_encontrados = numeros_encontrados[:2]

        # --- Verifica o pixel ---
        tem_objeto = detectar_objeto_sobre_fundo(*pixel_pos, cor_fundo=cor_fundo, limite=pixel_limite)

        # --- Lógica combinando OCR + Pixel ---
        if tem_objeto:
            if len(numeros_encontrados) == 0:
                # <<< AQUI ESTÁ A MUDANÇA >>>
                print("Pixel alterado, mas nenhum número detectado — operação é igual a 5.")
                numeros_encontrados = [2, 3]  # (ou qualquer combinação que some 5)
            elif len(numeros_encontrados) == 1:
                num = numeros_encontrados[0]
                if num != 1:
                    print(f"Pixel alterado — OCR detectou {num}, adicionando 1.")
                    numeros_encontrados.append(1)
                else:
                    print("Pixel alterado — operação é 1 + 1.")
                    numeros_encontrados = [1, 1]
            elif len(numeros_encontrados) == 2:
                print("Pixel alterado, mas dois números já detectados — sem alteração.")

        elif len(numeros_encontrados) == 0:
            # Nenhum número e pixel não mudou
            numeros_encontrados = [1, 4]
            print("Nenhum número detectado e pixel sem mudança — assumindo [1, 4].")

        elif len(numeros_encontrados) == 1 and not tem_objeto:
            num = numeros_encontrados[0]
            if num == 3:
                numeros_encontrados.append(1)
            elif num == 4:
                numeros_encontrados.append(1)
            elif num == 1:
                numeros_encontrados.append(4)
            else:
                numeros_encontrados.append(1)
            print(f"Apenas um número detectado ({num}) — previsão automática aplicada: {numeros_encontrados}")

        else:
            print("Dois números detectados normalmente.")

        # --- Calcula e digita ---
        soma_total = sum(numeros_encontrados)
        print("Números encontrados:", numeros_encontrados)
        print("Soma total:", soma_total)

        pyautogui.click(1050, 970)
        time.sleep(0.5)
        pyautogui.press(str(soma_total))
        print(f"Pressionada a tecla: {soma_total}")
        pyautogui.press('enter')
        time.sleep(3)

    # --- Incrementa e mostra o contador após as 3 execuções ---
    contador_ciclos += 1
    print(f"✅ Ciclo completo nº {contador_ciclos}")

    # --- Ação final após 3 execuções ---
    time.sleep(6)
    print("Executando ação final após 3 repetições...")
    pyautogui.click(1104, 638)
    time.sleep(0.5)
    pyautogui.click(1104, 638)
    time.sleep(3)
    pyautogui.click(965, 430)
    time.sleep(0.5)
    pyautogui.click(965, 430)
    time.sleep(12)
    print("-" * 40)
    time.sleep(1)
