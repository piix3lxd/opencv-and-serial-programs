#Título
print("                                 ## CALCULADORA ##")
print("A continuación, ingrese las variables para calcular su suma, resta y multiplicación...")
# Calculadora, primero empezaremos pidiendo el primer numero
print("\nIngrese el primer numero:")
#Guardaremos este numero en la variable que llamaremos "a"
a = int(input())
# Pediremos el segundo numero
print("Ingrese el segundo numero:")
# Guardaremos el nuevo numero en la variable que llamaremos "b" 
b = int(input())
# Ahora sumaremos estos dos numero de la siguiente forma
# Utilizaremos una nueva variable "s" para guardar el resultado de esta
s = a + b
# Mostramos el resultado por pantalla
print(f"valor de la suma es: {s}")
# La resta queda parecida a la de la suma
r = a - b
# Muestra la resta
print(f"valor de la resta es: {r}")
# Por ultimo haremos lo mismo con la multiplicacion
m = a * b
# Mostramos la multiplicacion
print(f"valor de la multiplicacion es: {m}")

print("\n                     ## División ##")
# Pedimos dos numeros nuevamente
print("\nIngrese el primer valor a dividir")
x = int(input())
print("Ingrese el segundo valior de la division (este valor no puede ser 0 >:c )")
y = int(input())

division = x / y
print(f"Valor de la division es: {division}")