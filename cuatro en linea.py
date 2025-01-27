import numpy as np
import time
from sympy import init_printing, matrix
import os 
init_printing()


#mostrara lo que el usuario va querer hacer 
class cuatro_en_linea():
    def __init__(self):
        print("1. jugador 1 vs npc ")
        print("2. juagdor 1  vs  jugador 2")
        seleccion = input("modo de juego")  
        seleccion = self.comprobar_seleccion(seleccion)
        self.modo = seleccion+1
        self.tablero = np.zero((6,7)).astype(int)
        self.optiones = [0,1,2,3,4,5,6]
        self.columnas_llenas = set()


#comprobara la seleciiones antes hechas 
    def comprobar_seleccion(self, seleccion, columnas_llenas=set()):
        while True:
            if not seleccion.isdigit():
                seleccion = input("no valido, debes ingresar un numero: ")
            elif int(seleccion) - 1 < 0 or int(seleccion) -1 > 6 or int(seleccion) - 1 in columnas_llenas:
                seleccion = input(f"Seleccion no valida, elige otra: ")
            else:
                break
        return int(seleccion) - 1


#
    def comprobar_ganar(self,booleano,cadena):
        #comprobar las filas
         for fila in booleano:
            #solo si hay 4 
            if sum(fila) >= 4:
                # 4 en linea
                if sum(fila[:4]) >= 4 or sum(fila[1:5]) >= 4 or sum(fila[2:6]) >= 4 or sum(fila[3:]) >= 4:
                    return True, f'!{cadena} gano! 4 en fila'


         for fila in booleano.T:
            #menos de 4
            if sum(fila) >= 4:
                # 4 en fila
                if sum(fila[:4]) >= 4 or sum(fila[1:5]) >= 4 or sum(fila[2:6]) >= 4 or sum(fila[3:]) >= 4:
                    return True, f'!{cadena} gano en una columna!'

         for k in range(-2,4):
            if sum(np.diag(booleano,k)) >= 4:
                if sum(np.diag(booleano,k)[:4]) >= 4 or sum(np.diag(booleano,k)[::-1][:4]) >=4:
                    return True, f'!{cadena} gano! 4 en una diagonal'

            if sum(np.diag(np.rot90(booleano),k-1)) >= 4:
                if sum(np.diag(np.rot90(booleano),k-1)[:4]) >= 4 or sum(np.diag(np.rot90(booleano),k-1)[::-1][:4]) >=4:
                    return True, f'!{cadena} gano! 4 en una diagonal'

         return False, ''

    def turno(self, jugador, computadora, seleccion=''):
        os.system('clear')
        display(matrix(self.tablero))
        if not computadora:
            seleccion = input(f"jugador {jugador}, seleccione una columna")
            seleccion = self.comprobar_seleccion(seleccion)

        #comprobara si la columna esta llena
        if np.prod(self.tablero[:,seleccion]) != 0:
            #cuando el npc escoga ena columna llena
            self.columnas_llenas.add(seleccion)
            if computadora:
                self.opciones.remove(seleccion)
                seleccion=np.random.choice(self.opciones)
            else:
                s = input("esta columna esta llena")
                seleccion = self.comprobar_seleccion(s,columnas_llenas=self.columnas_llenas)

            if sum(self.tablero[:,seleccion]) != 0:
                fila =np.argmax((self.tablero>0)[:,seleccion])-1
            else:
                fila = -1 
            if not computadora:
                self.tablero[fila,seleccion] = int(jugador)
            else:
                self.tablero[fila,seleccion] = 33

    def jugar(self):
        while True:

            time.sleep(.3)
            self.turno('1',computadora=False,seleccion='')
            win, cadena = self.comprobar_ganar(self.tablero==1, 'jugador 1')
            if win:
                time.sleep(.3)
                os.system('clear')
                display(Matrix(self.tablero))
                print(cadena)
                break

            if self.modo == 1:
                time.sleep(.3)
                self.turno('npc',computadora=True,seleccion=np.random.choice(self.optiones))
                cadena = 'computadora'
                win, cadena = self.comprobar_ganar(self.tablero==3,cadena)

            else:
                time.sleep(.3)
                self.turno('2',computadora=False,seleccion='')
                cadena = 'jugador 2'
                win, cadena =self.comprobar_ganar(self.tablero==2,cadena)

            if win:
                time.sleep(.3)
                os.system('clear')
                display(Matrix(self.tablero))
                print(cadena)
                break


    if __name__ == '_main_':
        cuatro_en_linea().jugar()