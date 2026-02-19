#Este archivo contiene errores PEP 8 intencionales para practicar corrección

import os,sys,json
def calcular_suma(lista_numeros):
    resultado=0
    for num in lista_numeros:
        resultado+=num
    return resultado

def procesar_datos(datos):
    if len(datos)>0:
        print("Procesando",len(datos),"elementos")
        datos_procesados=[]
        for item in datos:
            if item%2==0:
                datos_procesados.append(item*2)
            else:
                datos_procesados.append(item+1)
        return datos_procesados
    else:
        return []

class CalculadoraAvanzada:
    def __init__(self,precision=2):
        self.precision=precision
        self.historial=[]
    
    def sumar(self,a,b):
        resultado=round(a+b,self.precision)
        self.historial.append(f"{a}+{b}={resultado}")
        return resultado
    
    def multiplicar(self,a,b):
        resultado=round(a*b,self.precision)
        self.historial.append(f"{a}*{b}={resultado}")
        return resultado
        
    def obtener_historial(self):
        return self.historial

# Función principal con múltiples problemas de estilo
def main():
    numeros=[1,2,3,4,5,6,7,8,9,10]
    suma_total=calcular_suma(numeros)
    print(f"La suma total es: {suma_total}")
    
    datos_procesados=procesar_datos(numeros)
    print(f"Datos procesados: {datos_procesados}")
    
    calc=CalculadoraAvanzada()
    print(calc.sumar(5,3))
    print(calc.multiplicar(4,2.5))
    print(calc.obtener_historial())

if __name__=="__main__":
    main()
