import cv2
import numpy as np

# El 0 puede cambiar dependiendo de la cámara a utilizar
cap = cv2.VideoCapture(0)

# Crear una ventana para mostrar los resultados
cv2.namedWindow('Detención de Rectángulos', cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if ret:
        # ENCONTRANDO CONTORNOS DE LA IMAGEN

        # Cambiar imagen de color a gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Volver la imagen gris a una binaria
        _, th = cv2.threshold(gray, 140, 240, cv2.THRESH_BINARY)  # Los números cambian (menor el número es más blanco, mayor el número más oscuro)

        # Encontrar los contornos de la imagen binaria (solo encuentra en imágenes binarias)
        contornos, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # CONTANDO OBJETOS
        total = 0
        for c in contornos:
            area = cv2.contourArea(c)
            if area > 1700:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                if len(approx) == 4:
                    # Dibujar un contorno de un rectángulo alrededor del objeto
                    cv2.drawContours(frame, [approx], -1, (255, 0, 0), 2, cv2.LINE_AA)
                    total += 1

        rectangulo = 'Rectangulos: ' + str(total)
        # Mostrar el contador de rectangulos en la esquina superior izquierda
        cv2.putText(frame, rectangulo, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Mostrar la imagen con los contornos en la ventana llamada 'Detención de Rectángulos'
        cv2.imshow('Deteccion de Rectangulos', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
