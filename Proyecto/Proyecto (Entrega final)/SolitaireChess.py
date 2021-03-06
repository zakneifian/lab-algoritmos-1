#Librerias a importar
import pygame, time, sys, eztext, random
from pygame.locals import *
from operator import attrgetter

#Inicializamos pygame
pygame.init() 

#Frames per second de la ventana
FPS = 9
fpsClock = pygame.time.Clock()

#Ancho y largo de la ventana que se generara
display_width  = 760
display_height = 760
#Creamos la ventana y le damos nombre
global gameDisplay
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('USB\'s Solitaire Chess')

#Colores
white = (255,255,255)
black = (0  ,0  ,0  )
red   = (255,0  ,0  )
green = (0  ,255,0  )
blue  = (0  ,0  ,255)

#Fuente de letra
Font = pygame.font.SysFont(None, 30)
try:
	#Carga de sprites
	Cargarpartida 	   = pygame.image.load('Sprites/Cargarpartida.png'     ) 
	iconoPNG           = pygame.image.load('Sprites/icono.png'             ) 
	Dificultad         = pygame.image.load('Sprites/Dificultad.png'	       )
	CargadoTablero 	   = pygame.image.load('Sprites/CargadoTablero.png'    )
	DesafioTeclado	   = pygame.image.load('Sprites/DesafioTeclado.png'    )
	Opcionesfacil 	   = pygame.image.load('Sprites/OpcionesFacil.png'     )
	OpcionesDificil	   = pygame.image.load('Sprites/OpcionesDificil.png'   )
	OpcionesMuyDificil = pygame.image.load('Sprites/OpcionesMuyDificil.png')
	OpcionesTutorial   = pygame.image.load('Sprites/OpcionesTutorial.png'  )
	Leyenda			   = pygame.image.load('Sprites/Leyenda.png'		   )
	TableroPNG         = pygame.image.load('Sprites/Tablero.png'           )
	ReyPNG             = pygame.image.load('Sprites/Rey.png'               )
	DamaPNG            = pygame.image.load('Sprites/Reina.png'             )
	AlfilPNG           = pygame.image.load('Sprites/Alfil.png'             )
	CaballoPNG         = pygame.image.load('Sprites/Caballo.png'           )
	TorrePNG           = pygame.image.load('Sprites/Torre.png'             )
	PeonPNG            = pygame.image.load('Sprites/Peon.png'              )
	CajaPNG            = pygame.image.load('Sprites/Caja.png'              )
	MenuPrincipalPNG   = pygame.image.load('Sprites/MenuPrincipal.png'     )
	GanastePNG         = pygame.image.load('Sprites/ganaste.png'           )
	PerdistePNG        = pygame.image.load('Sprites/perdiste.png'          )
	CargarPNG          = pygame.image.load('Sprites/Cargarpartida.png'     )
	ScoreboardPNG      = pygame.image.load('Sprites/bg-pizarra.png'        )
	blurPNG = [pygame.image.load('Sprites/Blur/' + str(i) +'.png') for i in range(1,11)]
except:
	print("ERROR, FALTAN ALGUN(AS) IMAGENES DEL PROGRAMA")
	pygame.quit() 
	sys.exit()

#////////////////////////////////////////////////////////////////////////////////////

#Definiciones para el background
sentido = 'creciendo'
blur = 0

#Definiciones para el reloj
reloj = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

#Cargamos el icono y lo asignamos a la ventana
pygame.display.set_icon(iconoPNG)

#Funcion que se usa en un loop para proveer animacion de background
def AnimacionBackground():

	#Variables globales para que no me limite la asignacion local
	global sentido
	global blur

	#Crece hasta "9" para luego devolverse
	if sentido == 'creciendo':
		 gameDisplay.blit(blurPNG[blur], (0,0))
		 blur += 1
		 if blur == 9:
		 	sentido = 'decreciendo'
	elif sentido == 'decreciendo':
		 gameDisplay.blit(blurPNG[blur], (0,0))
		 blur -= 1
		 if blur == 0:
		 	sentido = 'creciendo'	

#Loop de la Pantalla inicial del juego.
def LoopIntro():
	#Almacena el nombre de usuario
	NombreUsuario = eztext.Input(maxlength=13, color=white, prompt='Nombre de usuario: ')
	NombreUsuario.set_pos(150,350)
	Inicio = True
	while Inicio:

	#Refresca los eventos a esta variable	
		eventos = pygame.event.get()
	#Variable que verifica si una tecla esta presionada
		presionada = pygame.key.get_pressed()
	#Animacion del background
		AnimacionBackground()
	#Evento para salir del juego o del loop inicial
		for event in eventos: 
			if event.type == QUIT: 
				pygame.quit() 
				sys.exit()
			if presionada[pygame.K_RETURN] and Usuario != "":
				Inicio = False
				with open("Texts/records.txt", "r+") as archivo:
					try:
						if all(linea.split()[0] != Usuario for linea in archivo): # NOMBRE NIVEL PUNTUACION
							archivo.seek(0)
							LineasDeArchivo = archivo.readlines()
							if LineasDeArchivo != []:
								archivo.write("\n" + Usuario + " " + "Tutorial" + " " + "0" + "\n" + Usuario + " " + "Facil" + " " + "0" + "\n" + Usuario + " " + "Dificil" + " " + "0" + "\n" + Usuario + " " + "Muy_Dificil" + " " + "0")
							elif LineasDeArchivo == []:
								archivo.write(Usuario + " " + "Tutorial" + " " + "0" + "\n" + Usuario + " " + "Facil" + " " + "0" + "\n" + Usuario + " " + "Dificil" + " " + "0" + "\n" + Usuario + " " + "Muy_Dificil" + " " + "0")
					except:
						archivo.write(Usuario + " " + "Tutorial" + " " + "0" + "\n" + Usuario + " " + "Facil" + " " + "0" + "\n" + Usuario + " " + "Dificil" + " " + "0" + "\n" + Usuario + " " + "Muy_Dificil" + " " + "0")
				return Usuario
	#Dibuja el input, lo actualiza y asigna a la variable 'Usuario'
		gameDisplay.blit(CajaPNG, (125,330))
		NombreUsuario.draw(gameDisplay)
		NombreUsuario.update(eventos)
		Usuario = NombreUsuario.value
	#Actualiza los dibujos de la pantalla a un determinado FPS
		pygame.display.flip()
		fpsClock.tick(FPS)

def Niveles():

	InputDificultad = eztext.Input(maxlength=1, color=white, prompt='')
	InputDificultad.set_pos(407, 422)
	pygame.display.set_caption('USB\'s Solitaire Chess - ' + Usuario)
	
	MenuNiveles = True
	while MenuNiveles:

		#Refresca los eventos a esta variable
		eventos = pygame.event.get()
		#Variable que verifica si una tecla esta presionada
		presionada = pygame.key.get_pressed()

		AnimacionBackground()

		#CAMBIAR LAS IMAGENES
		#Cargamos las imagenes con las opciones de los diferentes niveles del juego
		gameDisplay.blit(Dificultad, (180,125))
		InputDificultad.draw(gameDisplay)
		InputDificultad.update(eventos)
		Nivel = InputDificultad.value #Guardamos el valor del inputDificultad en la variable Nivel..
		

		 #Evento para salir hacia el menu Principal o para cargar el juego en su respectivo nivel
		for event in eventos:

			if event.type == pygame.locals.QUIT: 
				pygame.quit() 
				sys.exit()
			if presionada[pygame.K_RETURN] and Nivel == "0":
				return 
			if presionada[pygame.K_RETURN] and Nivel == "1":				
				MenuDesafio(Nivel)				
				
			if presionada[pygame.K_RETURN] and Nivel == "2":
				MenuDesafio(Nivel)
				
			if presionada[pygame.K_RETURN] and Nivel == "3":
				MenuDesafio(Nivel)
				
			if presionada[pygame.K_RETURN] and Nivel == "4":
				MenuDesafio(Nivel)
				

		pygame.display.update()
		fpsClock.tick(FPS)

 #en proceso, falta foto bonita de cargado en vez de solo CajaPNG

def CargarPartida():

	InputCarga = eztext.Input(maxlength=40, color=white, prompt='String de guardado: ')
	InputCarga.set_pos(177, 490)
	pygame.display.set_caption('USB\'s Solitaire Chess - ' + Usuario)
	MenuCarga = True
	while MenuCarga:
		#Refresca los eventos a esta variable
		eventos = pygame.event.get()
		#Variable que verifica si una tecla esta presionada
		presionada = pygame.key.get_pressed()

		AnimacionBackground()

		gameDisplay.blit(CajaPNG, (170,483))
		InputCarga.draw(gameDisplay)
		InputCarga.update(eventos)
		gameDisplay.blit(Cargarpartida, (130,0))
		string = InputCarga.value #Guardamos el valor del inputDificultad en la variable Nivel..

		 #Evento para salir hacia el menu Principal o para cargar el juego en su respectivo nivel
		for event in eventos:

			if event.type == pygame.locals.QUIT: 
				pygame.quit() 
				sys.exit()
			if presionada[pygame.K_RETURN] and string == "0":
				return 
			if presionada[pygame.K_RETURN] and string != "":
				try:
					string = string.split()
					numero = string[0]
					fecha = string[1]
					dificultad = string[2].lower()
					try: #Si existe un tercer elemento buscamos a ver si es "muy dificil" l asuma del segundo con el tercero
						if string[2].lower() + string[3].lower() == "muydificil":
							dificultadMD = "muydificil"
					except:
						dificultadMD = "None"
					with open("Texts/partidasguardadas.txt", "r+") as archivo:
						for linea in archivo:
							linea = linea.split()
							if len(linea) == 6: #NO MUY DIFICIL
								numeroF = linea[1]
								fechaF = linea[2]
								global contador
								contador = int(linea[3])
								DificultadF = linea[4].lower()
								PosPiezasF = linea[5]
								if numero == numeroF and fecha == fechaF and dificultad == DificultadF.lower():
									PosPiezasF = PosPiezasF.split('-')
									if DificultadF == 'tutorial':
										Tablero("Custom 4", PosPiezasF)
										return LoopPrincipal()
									elif DificultadF == 'facil':
										Tablero("Custom 1", PosPiezasF)
										return LoopPrincipal()
									elif DificultadF == 'dificil':
										Tablero("Custom 2", PosPiezasF)
										return LoopPrincipal()
							elif len(linea) == 9: #MUY DIFICIL
								numeroF = linea[1]
								fechaF = linea[2]

								global ContadorMuyDificil
								ContadorMuyDificil = int(linea[3])

								DificultadF = linea[4].lower()

								global PosActual
								PosActual = linea[5]

								PosPiezas1F = linea[6]
								PosPiezas2F = linea[7]
								PosPiezas3F = linea[8]
								if (numero == numeroF and fecha == fechaF and (dificultad == DificultadF or dificultadMD == DificultadF.lower())):
									if DificultadF == 'muydificil':
										global PosPiezas1
										global PosPiezas2
										global PosPiezas3
										PosPiezas1 = PosPiezas1F.split('-')
										PosPiezas2 = PosPiezas2F.split('-')
										PosPiezas3 = PosPiezas3F.split('-')

										if PosActual == "1":
											Tablero("3", PosPiezas1)
											PosActual = "2"
											Tablero("3", PosPiezas2)
											PosActual = "3"
											Tablero("3", PosPiezas3)
											
											with open("Texts/records.txt", "r+") as archivo:
												for linea in archivo:

													linea = linea.split()
													if linea[0] == Usuario and linea[1] == "Muy_Dificil":
														LineaVieja = ' '.join(linea)
														linea[2] = str(int(linea[2]) + 1)
														LineaNueva = ' '.join(linea)
														break
												archivo.seek(0)
												LineasOriginales = archivo.readlines()

											with open("Texts/records.txt", "w") as archivo:
												for linea in LineasOriginales:
													if linea == LineaVieja + '\n':
														archivo.write(LineaNueva + '\n')
													else:
														archivo.write(linea)

											pygame.display.set_mode((700, 350))
											gameDisplay.blit(GanastePNG,(0,0))
											pygame.display.update()
											pygame.time.delay(3000)	
											return LoopPrincipal()

										elif PosActual == "2":
											Tablero("3", PosPiezas2)
											PosActual = "3"
											Tablero("3", PosPiezas3)
											
											with open("Texts/records.txt", "r+") as archivo:
												for linea in archivo:

													linea = linea.split()
													if linea[0] == Usuario and linea[1] == "Muy_Dificil":
														LineaVieja = ' '.join(linea)
														linea[2] = str(int(linea[2]) + 1)
														LineaNueva = ' '.join(linea)
														break
												archivo.seek(0)
												LineasOriginales = archivo.readlines()

											with open("Texts/records.txt", "w") as archivo:
												for linea in LineasOriginales:
													if linea == LineaVieja + '\n':
														archivo.write(LineaNueva + '\n')
													else:
														archivo.write(linea)

											pygame.display.set_mode((700, 350))
											gameDisplay.blit(GanastePNG,(0,0))
											pygame.display.update()
											pygame.time.delay(3000)	
											return LoopPrincipal()

										elif PosActual == "3":
											Tablero("3", PosPiezas3)

											with open("Texts/records.txt", "r+") as archivo:
												for linea in archivo:

													linea = linea.split()
													if linea[0] == Usuario and linea[1] == "Muy_Dificil":
														LineaVieja = ' '.join(linea)
														linea[2] = str(int(linea[2]) + 1)
														LineaNueva = ' '.join(linea)
														break
												archivo.seek(0)
												LineasOriginales = archivo.readlines()

											with open("Texts/records.txt", "w") as archivo:
												for linea in LineasOriginales:
													if linea == LineaVieja + '\n':
														archivo.write(LineaNueva + '\n')
													else:
														archivo.write(linea)

											pygame.display.set_mode((700, 350))
											gameDisplay.blit(GanastePNG,(0,0))
											pygame.display.update()
											pygame.time.delay(3000)	
											return LoopPrincipal()
				except:
					print("Formato incorrecto")
					return CargarPartida()



	#guardado = "Partida " + str(lineas + 1) + " " + time.strftime("%d/%m/%y") + " " + 'Infinito' + " " + strNivel + " "+ string

		pygame.display.update()
		fpsClock.tick(FPS)


#arriba mientras tanto

#Se define el Loop principal del juego
def LoopPrincipal():

	display_width  = 760
	display_height = 760
	gameDisplay = pygame.display.set_mode((display_width, display_height))

	#Para la escogencia de la opcion del menu, definimos un InputMenu con longitud 1 para un solo numero
	InputMenu = eztext.Input(maxlength=1, color=white, prompt='Opcion: ')
	InputMenu.set_pos(248,480)
	EzTextusuario = eztext.Input(maxlength = 0, color=white, prompt=Usuario)
	#Muesta el nombre del usuario que esta jugando en la ventana
	pygame.display.set_caption('USB\'s Solitaire Chess - ' + Usuario)

	#Variable que verifica si ejecuta la parte del codigo del menu principal
	#Menunivel = Niveles()
	MenuPrincipal = True
	PantallaDeOpcionesPrincipal = True #Muestra las opciones principales
	OpcionNuevaPartida  = False        #Ejecuta el codigo de la partida nueva
	OpcionCargarPartida = False        #Ejecuta el codigo de Cargar Partida
	OpcionScoreboard    = False        #Ejecuta el codigo del Scoreboard

	#Si se cambia a True en el loop, se rompe y termina la ejecucion del juego

	while True:

	#Refresca los eventos a esta variable	
		eventos = pygame.event.get()

	#Variable que verifica si una tecla esta presionada
		presionada = pygame.key.get_pressed()

	#Bloque del Menu Principal
		if MenuPrincipal:

		#Animacion del background
			AnimacionBackground()

		#Muestra las Opciones principales
			if PantallaDeOpcionesPrincipal:

				gameDisplay.blit(MenuPrincipalPNG, (180,125))

				InputMenu.draw(gameDisplay)
				InputMenu.update(eventos)
				OpcionMenuPrincipal = InputMenu.value

		#Opcion Nueva Partida
			if OpcionNuevaPartida:
				OpcionNuevaPartida = False
				Niveles()
				PantallaDeOpcionesPrincipal = True
						

		#Opcion Cargar Partida
			if OpcionCargarPartida:
				###EN CONSTRUCCION### LAS TRES LINEAS DE ABAJO SON TEMPORALES
				OpcionCargarPartida = False
				CargarPartida()
				PantallaDeOpcionesPrincipal = True

		#Opcion Scoreboard
			if OpcionScoreboard:
				###EN CONSTRUCCION### LAS TRES LINEAS DE ABAJO SON TEMPORALES
				OpcionScoreboard = False
				PantallaDeOpcionesPrincipal = True
				LeerRecords()
				pygame.display.set_mode((760, 760))

	###
		###
	###		###
		###		### ESPACIO PARA EL RESTO DEL CODIGO DESHABILITANDO EL MENU PRINCIPAL
	###		###
		###
	###


	#Eventos del Loop Principal
		for event in eventos:

			if event.type == pygame.locals.QUIT: 
				pygame.quit() 
				sys.exit()

			#Opcion de Menu para Partida Nueva
			if presionada[pygame.K_RETURN] and OpcionMenuPrincipal == "1":
				OpcionNuevaPartida  = True
				PantallaDeOpcionesPrincipal = False

			#Opcion de Menu para Cargar Partida
			if presionada[pygame.K_RETURN] and OpcionMenuPrincipal == "2":
				OpcionCargarPartida = True
				PantallaDeOpcionesPrincipal = False

			#Opcion de Menu para Scoreboard
			if presionada[pygame.K_RETURN] and OpcionMenuPrincipal == "3":
				OpcionScoreboard    = True
				PantallaDeOpcionesPrincipal = False

			#Opcion de Menu para salir dejuego
			if presionada[pygame.K_RETURN] and OpcionMenuPrincipal == "4": 
				pygame.quit() 
				sys.exit()				

	#Actualiza los dibujos de la pantalla a un determinado FPS
		pygame.display.update()
		fpsClock.tick(FPS)

			#Nivel es el parametro q determinara que opciones cargada segun el nivel

def Tablero(Nivel, PosPiezas):

	#Muesta el nombre del usuario que esta jugando en la ventana
	pygame.display.set_caption('USB\'s Solitaire Chess - ' + Usuario)
	
	#Variables que manejaran cuando desactivar o activar un input (Dependiendo de la opcion seleccionada)
	Mostrar_Input_Tablero_Opcion = True
	Mostrar_Input_Jugar = False
	Mostrar_Input_Jugar_0 = False
	Mostrar_Input_Jugar_1 = False
	Mostrar_Input_Pausa = False
	Mostrar_Input_Terminar = False
	#Declarar todos los inputs abajo de esto
	#---------------------------------------
	Input_Tablero_Opcion = eztext.Input(maxlength=1, color=white, prompt='Elija una opcion: ')
	Input_Tablero_Opcion.set_pos(799,720)
	Opcion_Tablero=Input_Tablero_Opcion.value
	#---------------------------------------
	Input_Jugar_0 = eztext.Input(maxlength=2, color=white, prompt='Posicion Inicial: ')
	Input_Jugar_0.set_pos(799,680)
	Jugar_0 = Input_Jugar_0.value
	#---------------------------------------
	Input_Jugar_1 = eztext.Input(maxlength=2, color=white, prompt='Posicion Final: ')
	Input_Jugar_1.set_pos(799,720)
	Jugar_1 = Input_Jugar_1.value
	#---------------------------------------
	Input_Pausa = eztext.Input(maxlength=1, color=white, prompt='Inserte 0 y presione enter para resumir: ')
	Input_Pausa.set_pos(250,350)
	Opcion_Pausa = Input_Pausa.value
	#---------------------------------------
	Input_Terminar = eztext.Input(maxlength=1, color=white, prompt='1) Salir 2) guardar: ')
	Input_Terminar.set_pos(799,680)
	Salir_o_Guardar = Input_Terminar.value
	#---------------------------------------
	#Declarar todos los inputs encima de esto

	#Ancho y largo de la ventana que se generara
	display_width  = 1060
	display_height = 760

	#Cargamos de nuevo el display del juego con los nuevos valores
	gameDisplay = pygame.display.set_mode((display_width, display_height))

	#Variables de tiempo
	global contador
	global ContadorMuyDificil
	TextoDeContador = 'Tiempo restante: '
	if Nivel == '1':
		contador = 3*60
	elif Nivel == '2':
		contador = int(1.5*60)
	elif Nivel == '4':
		TextoDeContador = 'Tiempo restante: Infinito'
	elif Nivel == 'Custom 1':
		contador = contador
	elif Nivel == 'Custom 2':
		contador = contador
	elif Nivel == 'Custom 4':
		contador = contador

	#Nombre de usuario en pantalla
	Nombre = "Usuario: " + Usuario

	#Relativo a Deshacer
	lectura(PosPiezas)
	Deshacer_Temp_List = [MatrizToString(matriz)]
	Contador_de_deshacer = 0

	#Relativo a Solucion
	Solucion = False

	#Relativo a Perder o Ganar
	VerificarEstadoPartida = False


	
	while True:

		#Creamos la ventana nueva y le damos nombre

		#Refresca los eventos a esta variable	
		eventos = pygame.event.get()

		#Variable que verifica si una tecla esta presionada
		presionada = pygame.key.get_pressed()

		for event in eventos:

			if event.type == pygame.locals.QUIT: 
				pygame.quit() 
				sys.exit()

			#Funcion contadora de tiempo para niveles facil y dificil
			if event.type == pygame.USEREVENT and Mostrar_Input_Pausa == False and Nivel != '3' and Nivel != '4' and Nivel != "Custom 4":
				contador -= 1
				if contador > 0:
					TextoDeContador = 'Tiempo restante: ' + str(contador)
				else:
					pygame.display.set_mode((700, 350))
					gameDisplay.blit(PerdistePNG,(0,0))
					pygame.display.update()
					pygame.time.delay(3000)	
					return LoopPrincipal()

			#Funcion contadora de tiempo para nivel muy dificil
			if event.type == pygame.USEREVENT and Nivel == '3':
				ContadorMuyDificil -= 1
				if ContadorMuyDificil > 0:
					TextoDeContador = 'Tiempo restante: ' + str(ContadorMuyDificil)
				else:
					pygame.display.set_mode((700, 350))
					gameDisplay.blit(PerdistePNG,(0,0))
					pygame.display.update()
					pygame.time.delay(3000)	
					return LoopPrincipal()
			
			#Funcion jugar
			if  Opcion_Tablero == "1" and presionada[pygame.K_RETURN]:
				Mostrar_Input_Jugar = True
				Mostrar_Input_Jugar_0 = True
				Mostrar_Input_Tablero_Opcion = False
				Input_Tablero_Opcion.value = ""

			#Relativo a Funcion Jugar: Jugar_0
			if len(Input_Jugar_0.value) == 2 and presionada[pygame.K_RETURN]:
				Mostrar_Input_Jugar_0 = False
				Pos_i = Jugar_0

				if not Solucion:
					Mostrar_Input_Jugar_1 = True

				else: #if Solucion
					Torre(Pos_i, "Posicion Final nula", matriz, PosPiezas, False, True)
					Peon(Pos_i, "Posicion Final nula", matriz, PosPiezas, False, True)
					Caballo(Pos_i, "Posicion Final nula", matriz, PosPiezas, False, True)
					Rey(Pos_i, "Posicion Final nula", matriz, PosPiezas, False, True)
					Alfil(Pos_i, "Posicion Final nula", matriz, PosPiezas, False, True)
					Reina(Pos_i, "Posicion Final nula", matriz, PosPiezas, False, True)
					Solucion = False
					Jugar_0 = None
					Jugar_1 = None
					Input_Jugar_0.value = ""
					Input_Jugar_1.value = ""
					Input_Tablero_Opcion.value = ""
					Mostrar_Input_Jugar_1 = False
					Mostrar_Input_Jugar = False
					Mostrar_Input_Tablero_Opcion = True
					lectura(PosPiezas)
					VerificarEstadoPartida = True

			if len(Input_Jugar_1.value) == 2 and presionada[pygame.K_RETURN]:
				Pos_f = Jugar_1
				Torre(Pos_i, Pos_f, matriz, PosPiezas, False, False)
				Peon(Pos_i, Pos_f, matriz, PosPiezas, False, False)
				Caballo(Pos_i, Pos_f, matriz, PosPiezas, False, False)
				Rey(Pos_i, Pos_f, matriz, PosPiezas, False, False)
				Alfil(Pos_i, Pos_f, matriz, PosPiezas, False, False)
				Reina(Pos_i, Pos_f, matriz, PosPiezas, False, False)
				Jugar_0 = None
				Jugar_1 = None
				Input_Jugar_0.value = ""
				Input_Jugar_1.value = ""
				Input_Tablero_Opcion.value = ""
				Mostrar_Input_Jugar_1 = False
				Mostrar_Input_Jugar = False
				Mostrar_Input_Tablero_Opcion = True
				lectura(PosPiezas)
				Deshacer_Temp_List.append(MatrizToString(matriz))
				VerificarEstadoPartida = True

			#Funcion pausar
			if  Opcion_Tablero == "2" and Nivel != '3' and presionada[pygame.K_RETURN]:
				Mostrar_Input_Pausa = True
				Mostrar_Input_Tablero_Opcion = False
				Opcion_Tablero = ""
				Input_Tablero_Opcion.value = ""

			#Relativo a Funcion Pausar: Resumir despues de pausar
			if Opcion_Pausa == "0" and presionada[pygame.K_RETURN]:
				Mostrar_Input_Pausa = False
				Mostrar_Input_Tablero_Opcion = True
				Opcion_Pausa = ""
				Input_Pausa.value = ""		

			#Funcion Salir
			if  Opcion_Tablero == "3" and presionada[pygame.K_RETURN]:
				Mostrar_Input_Tablero_Opcion = False
				Mostrar_Input_Terminar=True
				Opcion_Tablero = ""
				Input_Tablero_Opcion.value = ""

			#Relativo a Funcion Salir: Salir sin Guardar
			if Salir_o_Guardar == "1" and presionada[pygame.K_RETURN]:
				return LoopPrincipal()

			#Relativo a Funcion Salir: Guardar y Salir
			if Salir_o_Guardar == "2" and presionada[pygame.K_RETURN]:
				string = MatrizToString(matriz)
				lineas = sum(1 for linea in open('Texts/partidasguardadas.txt'))
				if Nivel == '1' or Nivel == "Custom 1":
					strNivel = "Facil"
				elif Nivel == '2' or Nivel == "Custom 2":
					strNivel = "Dificil"
				elif Nivel == '3':
					strNivel = "MuyDificil"
				elif Nivel == '4' or Nivel == "Custom 4":
					strNivel = 'Tutorial'

				with open('Texts/partidasguardadas.txt', 'a+') as archivo:
					if Nivel != '3' and Nivel != '4' and Nivel != "Custom 4":	
						guardado = "Partida " + str(lineas + 1) + " " + time.strftime("%d/%m/%y") + " " + str(contador) + " " + strNivel + " "+ string
					elif Nivel == '3':
						string1 = MatrizToString(lectura(PosPiezas1))
						string2 = MatrizToString(lectura(PosPiezas2))
						string3 = MatrizToString(lectura(PosPiezas3))
						guardado = "Partida " + str(lineas + 1) + " " + time.strftime("%d/%m/%y") + " " + str(ContadorMuyDificil) + " " + strNivel + " " + PosActual + " " + string1 + " " + string2 + " " + string3
					elif Nivel == '4' or Nivel == "Custom 4":
						guardado = "Partida " + str(lineas + 1) + " " + time.strftime("%d/%m/%y") + " " + 'Infinito' + " " + strNivel + " "+ string
					print("A continuacion se guardara en una nueva linea:\n" + '"' + guardado + '"')
					if lineas + 1 == 1:
						archivo.write(guardado)
					else:
						archivo.write('\n' + guardado)

				return LoopPrincipal()

			#Funcion Deshacer
			if  Opcion_Tablero == "4" and presionada[pygame.K_RETURN] and (Nivel == "1" or Nivel == '4'):
				Opcion_Tablero = ""
				Input_Tablero_Opcion.value = ""
				if len(Deshacer_Temp_List) - Contador_de_deshacer > 1:
					Contador_de_deshacer += 1
					PosPiezas = Deshacer_Temp_List[len(Deshacer_Temp_List) - Contador_de_deshacer - 1].split('-')
					lectura(PosPiezas)
				else:
					print("ERROR, has deshecho todo lo posible, esta es la lista temporal actual:" + str(Deshacer_Temp_List))

			#Funcion Solucion
			if  Opcion_Tablero == "5" and presionada[pygame.K_RETURN] and (Nivel == '4' or Nivel == "Custom 4"):
				Solucion = True
				Mostrar_Input_Jugar = True
				Mostrar_Input_Jugar_0 = True
				Mostrar_Input_Tablero_Opcion = False
				Opcion_Tablero = ""
				Input_Tablero_Opcion.value = ""

			#Funcion Ganar o Perder
			if VerificarEstadoPartida:
				ListaTotalDePosibles = []
				tmp = []
				for i, j in matriz.items(): #i = key, j = value del diccionario Matriz
					for k, v in j.items(): # k = key, v = value de los diccionarios que son cada j
						if v != 0: #Si no esta vacio, se anade el valor
							tmp.append(str(k) + str(i))
				for Pos_i in tmp:
					try:
						ListaTotalDePosibles += Torre(Pos_i, "Posicion Final nula", matriz, PosPiezas, True, False)
					except:
						pass
					try:
						ListaTotalDePosibles +=  Peon(Pos_i, "Posicion Final nula", matriz, PosPiezas, True, False)
					except:
						pass
					try:
						ListaTotalDePosibles += Caballo(Pos_i, "Posicion Final nula", matriz, PosPiezas, True, False)
					except:
						pass
					try:
						ListaTotalDePosibles += Rey(Pos_i, "Posicion Final nula", matriz, PosPiezas, True, False)
					except:
						pass
					try:
						ListaTotalDePosibles += Alfil(Pos_i, "Posicion Final nula", matriz, PosPiezas, True, False)
					except:
						pass
					try:
						ListaTotalDePosibles += Reina(Pos_i, "Posicion Final nula", matriz, PosPiezas, True, False)
					except:
						pass
			
				if len(ListaTotalDePosibles) == 0:
					if len(PosPiezas) == 1 and Nivel != "3":

						with open("Texts/records.txt", "r+") as archivo:
							if Nivel == "1" or "Custom 1":
								NivelActual = "Facil"
							elif Nivel == "2" or "Custom 2":
								NivelActual = "Dificil"
							elif Nivel == "4" or "Custom 4":
								NivelActual = "Tutorial"

							for linea in archivo:

								linea = linea.split()
								if linea[0] == Usuario and linea[1] == NivelActual:
									LineaVieja = ' '.join(linea)
									linea[2] = str(int(linea[2]) + 1)
									LineaNueva = ' '.join(linea)
									break
							archivo.seek(0)
							LineasOriginales = archivo.readlines()

						with open("Texts/records.txt", "w") as archivo:
							for linea in LineasOriginales:
								if linea == LineaVieja + '\n':
									archivo.write(LineaNueva + '\n')
								else:
									archivo.write(linea)


						pygame.display.set_mode((700, 350))
						gameDisplay.blit(GanastePNG,(0,0))
						pygame.display.update()
						pygame.time.delay(3000)
						return LoopPrincipal()
					elif len(PosPiezas) == 1 and Nivel == "3":
						return
					elif len(PosPiezas) > 1:
						pygame.display.set_mode((700, 350))
						gameDisplay.blit(PerdistePNG,(0,0))
						pygame.display.update()
						pygame.time.delay(3000)	
						return LoopPrincipal()
				else:
					VerificarEstadoPartida = False				

			#ULTIMA FUNCION DEL EVENTO, LIMPIA DESPUES DE ENTER EL TABLERO OPCION
			if Mostrar_Input_Tablero_Opcion == True and presionada[pygame.K_RETURN]:
				Input_Tablero_Opcion.value = ""

		#En caso de ser nivel 1(Facil) cargara el menu con botones faciles
		if Nivel == "1" or Nivel == "Custom 1":
			gameDisplay.blit(Opcionesfacil,(758,0))
		#En caso de ser nivel 2(dificil) cargara el menu con los botones dificiles
		elif Nivel == "2" or Nivel == "Custom 2":
			gameDisplay.blit(OpcionesDificil,(758,0))
		elif Nivel == '3':
			gameDisplay.blit(OpcionesMuyDificil,(758,0))
		elif Nivel == '4' or Nivel == "Custom 4":
			gameDisplay.blit(OpcionesTutorial,(758,0))


		gameDisplay.blit(TableroPNG,(0,0))

		if Mostrar_Input_Tablero_Opcion == True:
			Input_Tablero_Opcion.draw(gameDisplay)
			Input_Tablero_Opcion.update(eventos)			
			Opcion_Tablero=Input_Tablero_Opcion.value

		if Mostrar_Input_Jugar == True:
			Input_Jugar_0.draw(gameDisplay)
			if not Solucion:
				Input_Jugar_1.draw(gameDisplay)

			if Mostrar_Input_Jugar_0 == True:
				Input_Jugar_0.draw(gameDisplay)				
				Input_Jugar_0.update(eventos)
				Jugar_0 = Input_Jugar_0.value
			
			if Mostrar_Input_Jugar_1 == True:
				Input_Jugar_1.draw(gameDisplay)				
				Input_Jugar_1.update(eventos)
				Jugar_1 = Input_Jugar_1.value


		if Mostrar_Input_Terminar == True:
			Input_Terminar.draw(gameDisplay)
			Input_Terminar.update(eventos)
			Salir_o_Guardar = Input_Terminar.value	


		gameDisplay.blit(TableroPNG,(0,0))

		lectura(PosPiezas)




		#Pantalla de Pausa
		if Mostrar_Input_Pausa == True:
			gameDisplay.blit(TableroPNG,(0,0))
			gameDisplay.blit(CajaPNG, (250, 350))
			Input_Pausa.draw(gameDisplay)
			Input_Pausa.update(eventos)
			Opcion_Pausa = Input_Pausa.value

		#Pantalla de Tiempo
		gameDisplay.blit(Font.render(TextoDeContador, True, black), (5,5))

		#Pantalla de Nombre
		gameDisplay.blit(Font.render(Nombre, True, black), (5, 30))

		#Pantalla de Tabler Actual en dificultad Muy Dificil
		if Nivel == "3":
			gameDisplay.blit(Font.render("Tablero actual: " + PosActual, True, black), (550, 5))

		pygame.display.update()
		fpsClock.tick(FPS)

				#OpcionMenuNiveles es el parametro que guarda el nivel(facil/dif...)

def MenuDesafio(Nivel):

	#Muesta el nombre del usuario que esta jugando en la ventana
	pygame.display.set_caption('USB\'s Solitaire Chess - ' + Usuario)

	InputCargado = eztext.Input(maxlength=1, color=white, prompt='')
	InputCargado.set_pos(495, 263)

	while True:
		#Refresca los eventos a esta variable	
		eventos = pygame.event.get()

		#Variable que verifica si una tecla esta presionada
		presionada = pygame.key.get_pressed()

		#Animacion del background
		AnimacionBackground()

		for event in eventos:

			if event.type == pygame.locals.QUIT: 
				pygame.quit() 
				sys.exit()


			if presionada[pygame.K_RETURN] and Opcion_Teclado_Desafio == "1":
				#Llamamos la funcion que contiene la ventana del input para el usuario cree su tablero
				Configuracion_por_teclado(Nivel)
			if presionada[pygame.K_RETURN] and Opcion_Teclado_Desafio == "2":
				global ContadorMuyDificil
				ContadorMuyDificil = 2*60
				lineas = 1
				if Nivel == '1':
					rndm = random.randint(1, 20)
					with open('Texts/partidasnuevas.txt', 'r+') as archivo:
						for linea in archivo:
							if lineas == rndm:
								PosPiezas = linea.split()[0].split("-")
								Tablero(Nivel, PosPiezas)
							else:
								lineas += 1

				elif Nivel == '2':
					rndm = random.randint(20, 40)
					with open('Texts/partidasnuevas.txt', 'r+') as archivo:
						for linea in archivo:
							if lineas == rndm:
								PosPiezas = linea.split()[0].split("-")
								Tablero(Nivel, PosPiezas)
							else:
								lineas += 1

				elif Nivel == '4':
					rndm = random.randint(1, 60)
					with open('Texts/partidasnuevas.txt', 'r+') as archivo:
						for linea in archivo:
							if lineas == rndm:
								PosPiezas = linea.split()[0].split("-")
								Tablero(Nivel, PosPiezas)
							else:
								lineas += 1
			if Nivel == '3':
				ContadorMuyDificil = 2*60
				global PosActual
				lineas = 1
				rndm = random.sample(range(40, 61), 3)
				with open('Texts/partidasnuevas.txt', 'r+') as archivo:
					for linea in archivo: #Primera Partida
						if lineas == rndm[0]:
							global PosPiezas1
							PosPiezas1 = linea.split()[0].split("-")
							break
						else:
							lineas += 1
					archivo.seek(lineas, 0)
					lineas = 1				
					for linea in archivo: #Segunda Partida
						if lineas == rndm[1]:
							global PosPiezas2
							PosPiezas2 = linea.split()[0].split("-")
							break
						else:
							lineas += 1
					archivo.seek(lineas, 0)
					lineas = 1
					for linea in archivo: #Tercera Partida
						if lineas == rndm[2]:
							global PosPiezas3
							PosPiezas3 = linea.split()[0].split("-")
							break
						else:
							lineas += 1
					global PosActual
					PosActual = '1'
					Tablero(Nivel, PosPiezas1)
					PosActual = '2'
					Tablero(Nivel, PosPiezas2)
					PosActual = '3'
					Tablero(Nivel, PosPiezas3)

					with open("Texts/records.txt", "r+") as archivo:
						for linea in archivo:

							linea = linea.split()
							if linea[0] == Usuario and linea[1] == "Muy_Dificil":
								LineaVieja = ' '.join(linea)
								linea[2] = str(int(linea[2]) + 1)
								LineaNueva = ' '.join(linea)
								break
						archivo.seek(0)
						LineasOriginales = archivo.readlines()

					with open("Texts/records.txt", "w") as archivo:
						for linea in LineasOriginales:
							if linea == LineaVieja + '\n':
								archivo.write(LineaNueva + '\n')
							else:
								archivo.write(linea)

					pygame.display.set_mode((700, 350))
					gameDisplay.blit(GanastePNG,(0,0))
					pygame.display.update()
					pygame.time.delay(3000)	
					return LoopPrincipal()




		gameDisplay.blit(CargadoTablero,(198,90))
		gameDisplay.blit(DesafioTeclado,(90,350))
		InputCargado.draw(gameDisplay)
		
		InputCargado.update(eventos)
		Opcion_Teclado_Desafio= InputCargado.value
		pygame.display.update()
		fpsClock.tick(FPS)

def lectura(PosPiezas):
	global matriz
	matriz = {
			  1:{'a':0, 'b':0, 'c':0, 'd':0},
			  2:{'a':0, 'b':0, 'c':0, 'd':0},
			  3:{'a':0, 'b':0, 'c':0, 'd':0},
			  4:{'a':0, 'b':0, 'c':0, 'd':0}
			 }
	x=0
	y=0

	for pieza in PosPiezas:
		if len(pieza) == 3:

			if pieza[0].lower() == "t":
				if pieza[1]=="a":
					matriz[int(pieza[2])]['a']="t"
					x=69
				elif pieza[1] == "b":
					matriz[int(pieza[2])]['b']="t"
					x=225
				elif pieza[1] == "c":
					matriz[int(pieza[2])]['c']="t"
					x=381
				elif pieza[1] == "d":
					matriz[int(pieza[2])]['d']="t"
					x=538

				if pieza[2]=="4":
					gameDisplay.blit(TorrePNG, (x,65)) 

				elif pieza[2]=="3":
					gameDisplay.blit(TorrePNG, (x,222)) 

				elif pieza[2] == "2":
					gameDisplay.blit(TorrePNG, (x,378)) 

				elif pieza[2] == "1":
					gameDisplay.blit(TorrePNG, (x,536)) 

			elif pieza[0].lower() == "c":
				if pieza[1]=="a":
					matriz[int(pieza[2])]['a']="c"
					x=69
				elif pieza[1] == "b":
					matriz[int(pieza[2])]['b']="c"
					x=225
				elif pieza[1] == "c":
					matriz[int(pieza[2])]['c']="c"
					x=381
				elif pieza[1] == "d":
					matriz[int(pieza[2])]['d']="c"
					x=538

				if pieza[2]=="4":
					gameDisplay.blit(CaballoPNG, (x,65)) 

				elif pieza[2]=="3":
					gameDisplay.blit(CaballoPNG, (x,222)) 

				elif pieza[2] == "2":
					gameDisplay.blit(CaballoPNG, (x,378)) 

				elif pieza[2] == "1":
					gameDisplay.blit(CaballoPNG, (x,534)) 

			elif pieza[0].lower() == "a":
				if pieza[1]=="a":
					matriz[int(pieza[2])]['a']="a"
					x=69
				elif pieza[1] == "b":
					matriz[int(pieza[2])]['b']="a"
					x=225
				elif pieza[1] == "c":
					matriz[int(pieza[2])]['c']="a"
					x=381
				elif pieza[1] == "d":
					matriz[int(pieza[2])]['d']="a"
					x=538

				if pieza[2]=="4":
					gameDisplay.blit(AlfilPNG, (x,65)) 

				elif pieza[2]=="3":
					gameDisplay.blit(AlfilPNG, (x,222)) 

				elif pieza[2] == "2":
					gameDisplay.blit(AlfilPNG, (x,378)) 

				elif pieza[2] == "1":
					gameDisplay.blit(AlfilPNG, (x,534)) 

			elif pieza[0].lower() == "r":
				if pieza[1]=="a":
					matriz[int(pieza[2])]['a']="r"
					x=69
				elif pieza[1] == "b":
					matriz[int(pieza[2])]['b']="r"
					x=225
				elif pieza[1] == "c":
					matriz[int(pieza[2])]['c']="r"
					x=381
				elif pieza[1] == "d":
					matriz[int(pieza[2])]['d']="r"
					x=538

				if pieza[2]=="4":
					gameDisplay.blit(ReyPNG, (x,65)) 

				elif pieza[2]=="3":
					gameDisplay.blit(ReyPNG, (x,222)) 

				elif pieza[2] == "2":
					gameDisplay.blit(ReyPNG, (x,378)) 

				elif pieza[2] == "1":
					gameDisplay.blit(ReyPNG, (x,534)) 

			elif pieza[0].lower() == "d":
				if pieza[1]=="a":
					matriz[int(pieza[2])]['a']="d"
					x=69
				elif pieza[1] == "b":
					matriz[int(pieza[2])]['b']="d"
					x=225
				elif pieza[1] == "c":
					matriz[int(pieza[2])]['c']="d"
					x=381
				elif pieza[1] == "d":
					matriz[int(pieza[2])]['d']="d"
					x=538

				if pieza[2]=="4":
					gameDisplay.blit(DamaPNG, (x,65)) 

				elif pieza[2]=="3":
					gameDisplay.blit(DamaPNG, (x,222)) 

				elif pieza[2] == "2":
					gameDisplay.blit(DamaPNG, (x,378)) 

				elif pieza[2] == "1":
					gameDisplay.blit(DamaPNG, (x,534)) 

		elif len(pieza)==2:
				if pieza[0]=="a":
					matriz[int(pieza[1])]['a']="P"
					x=69
				elif pieza[0] == "b":
					matriz[int(pieza[1])]['b']="P"
					x=225
				elif pieza[0] == "c":
					matriz[int(pieza[1])]['c']="P"
					x=381
				elif pieza[0] == "d":
					matriz[int(pieza[1])]['d']="P"
					x=538

				if pieza[1]=="4":
					gameDisplay.blit(PeonPNG, (x,65)) 

				elif pieza[1]=="3":
					gameDisplay.blit(PeonPNG, (x,222)) 

				elif pieza[1] == "2":
					gameDisplay.blit(PeonPNG, (x,378)) 

				elif pieza[1] == "1":
					gameDisplay.blit(PeonPNG, (x,534))

	return matriz

def MatrizToString(Matriz):
	string = ""
	tmp = []
	for i, j in Matriz.items(): #i = numero
		for k, v in j.items(): # k = letra #v = pieza
			if v == 'P': #Si v es un peon
				tmp.append(str(k) + str(i)) #No se anade la P
			elif v != 0: #Si no esta vacio, se anade el valor
				tmp.append(str(v).upper() + str(k) + str(i))

	for i in range(len(tmp)):
		if i == 0:
			string += tmp[i]
		else:
			string += '-' + tmp[i]

	print(string)
	return string

def Configuracion_por_teclado(Nivel):

	#Muesta el nombre del usuario que esta jugando en la ventana
	pygame.display.set_caption('USB\'s Solitaire Chess - ' + Usuario)

	#Cargara la cuadricula para habilitarle al usuario el poder ingresar como desea el tablero
	InputConfiguracionTeclado = eztext.Input(maxlength=31, color=white, prompt='Introduce tu configuracion: ')
	InputConfiguracionTeclado.set_pos(0,727)
	InputConfiguracionTeclado.value="" #METODO PARA PROBAR LA POSICION DE LAS FICHAS

	while True:

		eventos = pygame.event.get()

		#Variable que verifica si una tecla esta presionada
		presionada = pygame.key.get_pressed()

		#Efecto de animacion
		AnimacionBackground()

		for event in eventos:

			if event.type == pygame.locals.QUIT: 
				pygame.quit() 
				sys.exit()

			if presionada[pygame.K_RETURN]: #colocar la condicion de que sea un string valido
				#Convertimos el string de configuracion_Teclado en una lista
				InputConfiguracionTeclado.value = InputConfiguracionTeclado.value.split('-')
				PosPieza = InputConfiguracionTeclado.value
				PosPiezas = []
				for elemento in PosPieza:
					if len(elemento) == 2:
						PosPiezas.append(elemento.lower())
					elif len(elemento) == 3:
						PosPiezas.append(elemento[0].upper() + elemento[1:].lower())

				print("Usted ha introducido: " + str(PosPiezas))
			#Chequeamos que cumpla con las reglas de longitud
				if  not 0 < len(PosPiezas) <= 8:
					print("Has insertado un numero invalido de piezas, maximo 8.")
					return Configuracion_por_teclado(Nivel)
			#Chequeamos que todos sigan las reglas de escritura
				for elemento in PosPiezas:
					if not 2 <= len(elemento) <= 3:
						print("Hay elemento/s con menos de 2 o mas de 3 caracteres, se regresara al menu")
						return Configuracion_por_teclado(Nivel)
					if len(elemento) == 3:
						if not ((elemento[0] == 'R' or elemento[0] == 'D' or elemento[0] == 'A' or elemento[0] == 'C' or elemento[0] == 'T') and (elemento[1] == 'a' or elemento[1] == 'b' or elemento[1] == 'c' or elemento[1] == 'd') and (elemento[2] == '1' or elemento[2] == '2' or elemento[2] == '3' or elemento[2] == '4')):
							print("Hay elementos mal formateados, se regresara al menu")
							Configuracion_por_teclado(Nivel)
					if len(elemento) == 2:
						if not ((elemento[0] == 'a' or elemento[0] == 'b' or elemento[0] == 'c' or elemento[0] == 'd') and (elemento[1] == '1' or elemento[1] == '2' or elemento[1] == '3' or elemento[1] == '4')):
							print("Hay elementos mal formateados, se regresara al menu")
							Configuracion_por_teclado(Nivel)
			#Chequeamos que ninguno este en la posicion de otro
				for elem_1 in PosPiezas:
					if len(elem_1) == 3:
						for elem_2 in PosPiezas:
							if len(elem_2) == 3:
								if  (elem_1 != elem_2) and (elem_1[1:] == elem_2[1:]):
									print("No puedes mas de una pieza en una posicion")
									return Configuracion_por_teclado(Nivel)
							elif len(elem_2) == 2:
								if  (elem_1 != elem_2) and (elem_1[1:] == elem_2[0:]):
									print("No puedes mas de una pieza en una posicion")
									return Configuracion_por_teclado(Nivel)		
					if len(elem_1) == 2:
						for elem_2 in PosPiezas:
							if len(elem_2) == 3:
								if  (elem_1 != elem_2) and (elem_1[0:] == elem_2[1:]):
									print("No puedes mas de una pieza en una posicion")
									return Configuracion_por_teclado(Nivel)
							elif len(elem_2) == 2:
								if  (elem_1 != elem_2) and (elem_1[0:] == elem_2[0:]):
									print("No puedes mas de una pieza en una posicion")
									return Configuracion_por_teclado(Nivel)								
			#Chequeamos que no hayan dos piezas iguales en el string
				ListaTMP = []
				for elemento in PosPiezas:
					if not (elemento in ListaTMP):
						ListaTMP.append(elemento)
					else:
						print("Hay elementos duplicados, por favor intente de nuevo")
						Configuracion_por_teclado(Nivel)
			#Chequeamos que haya maximo dos peones, dos caballos, dos alfiles, dos torres, 1 rey, 1 reina
				for elem_1 in PosPiezas:
					for elem_2 in PosPiezas:
						for elem_3 in PosPiezas:
							if elem_1 != elem_2 and elem_1 != elem_3 and elem_2 != elem_3:
								if len(elem_1) == len(elem_2) == len(elem_3) == 3:
									if elem_1[0] == elem_2[0] == elem_3[0]:
										print("Como maximo puede haber dos peones, dos caballos, dos alfiles, dos torres, un rey y una reina")
										return Configuracion_por_teclado(Nivel)
								elif len(elem_1) == len(elem_2) == len(elem_3) == 2:
									print("Como maximo puede haber dos peones, dos caballos, dos alfiles, dos torres, un rey y una reina")
									return Configuracion_por_teclado(Nivel)

						if elem_1 != elem_2:
							if (elem_1[0] == elem_2[0] == "R") or (elem_1[0] == elem_2[0] == "D"):
								print("Como maximo puede haber dos peones, dos caballos, dos alfiles, dos torres, un rey y una reina")
								return Configuracion_por_teclado(Nivel)

				#retornamos el tablero con el nivel seleccionado
				Tablero(Nivel,PosPiezas)


		gameDisplay.blit(CajaPNG,(0,717))
		gameDisplay.blit(CajaPNG,(300,717))
		gameDisplay.blit(CajaPNG,(600,717))
		gameDisplay.blit(Leyenda,(88,145))
		InputConfiguracionTeclado.draw(gameDisplay)
		InputConfiguracionTeclado.update(eventos)
		#Asignamos el valor de la configuracion a la variable Configuracion_teclado
		Configuracion_Teclado = InputConfiguracionTeclado.value
		pygame.display.update()
		fpsClock.tick(FPS)

def CambioLetra(letra, sentido):
	if sentido == 1:
		if letra == 'a':
			return 'b'
		elif letra == 'b':
			return 'c'
		elif letra == 'c':
			return 'd'
		elif letra == 'd':
			return False
	elif sentido == -1:
		if letra == 'a':
			return False
		elif letra == 'b':
			return 'a'
		elif letra == 'c':
			return 'b'
		elif letra == 'd':
			return 'c'	
	elif sentido == 2:
		if letra == 'a':
			return 'c'
		elif letra == 'b':
			return 'd'
		elif letra == 'c':
			return False
		elif letra == 'd':
			return False
	elif sentido == 3:
		if letra == 'a':
			return 'd'
		elif letra == 'b':
			return False
		elif letra == 'c':
			return False
		elif letra == 'd':
			return False		
	elif sentido == -2:	
		if letra == 'a':
			return False
		elif letra == 'b':
			return False
		elif letra == 'c':
			return 'a'
		elif letra == 'd':
			return 'b'
	elif sentido == -3:	
		if letra == 'a':
			return False
		elif letra == 'b':
			return False
		elif letra == 'c':
			return False
		elif letra == 'd':
			return 'a'
	elif sentido == 0:
		if letra == 'a':
			return 'a'
		elif letra == 'b':
			return 'b'
		elif letra == 'c':
			return 'c'
		elif letra == 'd':
			return 'd'		

def Peon(Pos_i, Pos_f, Matriz, PosPiezas, EstadoPartida, Solucion):

	try:
		Pos_i = [Pos_i[:1], int(Pos_i[1:])] #letra, numero
		if not (EstadoPartida or Solucion):
			Pos_f = [Pos_f[:1], int(Pos_f[1:])] #letra, numero
		posibles = [] #lista de posibles jugadas, cada elemento sera [letra, numero], numero en int
		assert(Matriz[Pos_i[1]][Pos_i[0]].lower() == "p") #que el inicial sea torre y el final distinto de 0	
		if not (EstadoPartida or Solucion):
			assert(Matriz[Pos_f[1]][Pos_f[0]] != 0 and Matriz[Pos_f[1]][Pos_f[0]].lower() != "r")
		
		#En este for, se construye la lista de posibles para el peon, sin refinar.
		for numero, diccionario in Matriz.items():
			for letra, pieza in diccionario.items():
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0], 1) and numero == Pos_i[1] + 1:
					posibles.append([letra, numero])		
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0],-1) and numero == Pos_i[1] + 1:
					posibles.append([letra, numero])
				#Al parecer el peon solo se mueve en diagonal de adelante.
				#if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0], -1) and numero == Pos_i[1] - 1:
				#	posibles.append([letra, numero])	
				#if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0], 1) and numero == Pos_i[1] - 1:
				#	posibles.append([letra, numero])	
		if Solucion:
			try:
				Pos_f = posibles[0]
			except:
				print("No hay jugadas posibles")
				return

		if EstadoPartida:
			return posibles

		if not EstadoPartida:
			if [Pos_f[0], int(Pos_f[1])] in posibles:
				try:
					PosPiezas.remove((Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('D' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('A' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('C' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('T' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass			

				PosPiezas.remove((Pos_i[0] + str(Pos_i[1])).lower())
			else:
				print("Si la pieza inicial era un peon, la jugada fue invalida")

			for posible in posibles:
				if posible[0] == Pos_f[0] and posible[1] == Pos_f[1]:
					PosPiezas.append(Pos_f[0] + str(Pos_f[1]))
					print("La jugada con el Peon en (" + Pos_i[0] + ", " + str(Pos_i[1]) + ") a la posicion (" + Pos_f[0] + ", " + str(Pos_f[1]) + ") ha sido exitosa.")
			return PosPiezas



	except:
		pass

def Torre(Pos_i, Pos_f, Matriz, PosPiezas, EstadoPartida, Solucion):
	try:
		Pos_i = [Pos_i[:1], int(Pos_i[1:])] #letra, numero
		if not (EstadoPartida or Solucion):
			Pos_f = [Pos_f[:1], int(Pos_f[1:])] #letra, numero
		posibles = [] #lista de posibles jugadas, cada elemento sera [letra, numero], numero en int
		posiblesRef = [] #lista refinada de "posibles"
		assert(Matriz[Pos_i[1]][Pos_i[0]].lower() == "t") #que el inicial sea torre y el final distinto de 0
		if not (EstadoPartida or Solucion):
			assert(Matriz[Pos_f[1]][Pos_f[0]] != 0 and Matriz[Pos_f[1]][Pos_f[0]].lower() != "r")
		#En este for, se construye la lista de posibles para la torre, sin refinar.
		for numero, diccionario in Matriz.items():
			for letra, pieza in diccionario.items():			
				if numero == Pos_i[1]: #Primero trabajamos en el eje de los numeros
					if pieza != 0 and pieza.lower() != 'r' and letra != Pos_i[0]: #Si hay una pieza				
						posibles.append([letra, numero])
				if letra == Pos_i[0]: #Ahora trabajamos en el eje de las letras
					if pieza != 0 and pieza.lower() != 'r' and numero != Pos_i[1]: #Si hay una pieza
						posibles.append([letra, numero])

		#Variables usadas para refinar la lista de posibles jugadas
		tmp_letra_mayor = 'z'
		tmp_letra_menor = '1'
		tmp_numero_mayor = 10
		tmp_numero_menor = 0
		TMPNumLETRA =    "No" #Variable que almacena la pieza mas cercana a la Torre, por la   derecha de la Torre
		tmpNumletra =    "No" #Variable que almacena la pieza mas cercana a la Torre, por la izquierda de la Torre
		tmpLetraNUMERO = "No" #Variable que almacena la pieza mas cercana a la Torre, por       arriba de la Torre
		tmpLetranumero = "No" #Variable que almacena la pieza mas cercana a la Torre, por        abajo de la Torre

		#Refinando la lista
		for valor in posibles:

			if valor[1] == Pos_i[1]: #Mismo numero
				if valor[0] > Pos_i[0]: #letra mayor a la inicial
					if valor[0] < tmp_letra_mayor: #El valor actual", valor[0], "es menor que la tmp actual", tmp_letra_mayor
						tmp_letra_mayor = valor[0]
						TMPNumLETRA = valor
				elif valor[0] < Pos_i[0]: #letra menor a la inicial
					if valor[0] > tmp_letra_menor:
						tmp_letra_menor = valor[0]
						tmpNumletra = valor

			elif valor[0] == Pos_i[0]: #Misma letra
				if valor[1] > Pos_i[1]: #
					if valor[1] < tmp_numero_mayor: #El valor actual", valor[1], "es menor que la tmp actual", tmp_numero_mayor
						tmp_numero_mayor = valor[1]
						tmpLetraNUMERO = valor			
				elif valor[1] < Pos_i[1]: #numero menor al inicial
					if valor[1] > tmp_numero_menor:
						tmp_numero_menor = valor[1]
						tmpLetranumero = valor				

		#anadiendo a posiblesRef
		if TMPNumLETRA !=    "No":
			posiblesRef.append(TMPNumLETRA)
		if tmpNumletra !=    "No":
			posiblesRef.append(tmpNumletra)
		if tmpLetraNUMERO != "No":
			posiblesRef.append(tmpLetraNUMERO)
		if tmpLetranumero != "No":
			posiblesRef.append(tmpLetranumero)
		
		if Solucion:
			try:
				Pos_f = posiblesRef[0]
			except:
				print("No hay jugadas posibles")
				return

		if EstadoPartida:
			return posibles

		if not EstadoPartida:	
			#En este for se busca la posicion final entre los posibles y se cambia el inicial por "0" y el final por la torre
			if [Pos_f[0], int(Pos_f[1])] in posiblesRef:
				try:
					PosPiezas.remove((Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('D' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('A' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('C' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('T' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass			

				PosPiezas.remove("T" + (Pos_i[0] + str(Pos_i[1])).lower())
			else:
				print("Si la pieza inicial era una torre, la jugada fue invalida")

			for posible in posiblesRef:
				if posible[0] == Pos_f[0] and posible[1] == Pos_f[1]:
					PosPiezas.append("T" + Pos_f[0] + str(Pos_f[1]))
					print("La jugada con la Torre en (" + Pos_i[0] + ", " + str(Pos_i[1]) + ") a la posicion (" + Pos_f[0] + ", " + str(Pos_f[1]) + ") ha sido exitosa.")
			return PosPiezas	

	except:
		pass

 #Actualmente necesita rehacerse el metodo de busqueda y de refinamiento

def Caballo(Pos_i, Pos_f, Matriz, PosPiezas, EstadoPartida, Solucion):
	try:
		Pos_i = [Pos_i[:1], int(Pos_i[1:])] #letra, numero
		if not (EstadoPartida or Solucion):
			Pos_f = [Pos_f[:1], int(Pos_f[1:])] #letra, numero
		posibles = [] #lista de posibles jugadas, cada elemento sera [letra, numero], numero en int
		assert(Matriz[Pos_i[1]][Pos_i[0]].lower() == "c") #que el inicial sea caballo y el final distinto de 0
		if not (EstadoPartida or Solucion):
			assert(Matriz[Pos_f[1]][Pos_f[0]] != 0 and Matriz[Pos_f[1]][Pos_f[0]].lower() != "r")

		#En este for, se construye la lista de posibles para el peon, sin refinar.
		for numero, diccionario in Matriz.items():
			for letra, pieza in diccionario.items():
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0], 2) and numero == Pos_i[1] + 1:
					posibles.append([letra, numero])		
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0], 1) and numero == Pos_i[1] + 2:
					posibles.append([letra, numero])
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0],-1) and numero == Pos_i[1] + 2:
					posibles.append([letra, numero])	
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0],-2) and numero == Pos_i[1] + 1:
					posibles.append([letra, numero])	
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0],-2) and numero == Pos_i[1] - 1:
					posibles.append([letra, numero])		
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0],-1) and numero == Pos_i[1] - 2:
					posibles.append([letra, numero])
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0], 1) and numero == Pos_i[1] - 2:
					posibles.append([letra, numero])	
				if pieza != 0 and pieza.lower() != 'r' and letra == CambioLetra(Pos_i[0], 2) and numero == Pos_i[1] - 1:
					posibles.append([letra, numero])

		if Solucion:
			try:
				Pos_f = posibles[0]
			except:
				print("No hay jugadas posibles")
				return

		if EstadoPartida:
			return posibles

		if not EstadoPartida:
			if [Pos_f[0], int(Pos_f[1])] in posibles:
				try:
					PosPiezas.remove((Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('D' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('A' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('C' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('T' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass		

				PosPiezas.remove("C" + (Pos_i[0] + str(Pos_i[1])).lower())
			else:
				print("Si la pieza inicial era un caballo, la jugada fue invalida")

			for posible in posibles:
				if posible[0] == Pos_f[0] and posible[1] == Pos_f[1]:
					PosPiezas.append("C" + Pos_f[0] + str(Pos_f[1]))
					print("La jugada con el Caballo en (" + Pos_i[0] + ", " + str(Pos_i[1]) + ") a la posicion (" + Pos_f[0] + ", " + str(Pos_f[1]) + ") ha sido exitosa.")
			return PosPiezas	


	except:
		pass

def Alfil(Pos_i, Pos_f, Matriz, PosPiezas, EstadoPartida, Solucion):
	try:
		Pos_i = [Pos_i[:1], int(Pos_i[1:])] #letra, numero
		if not (EstadoPartida or Solucion):
			Pos_f = [Pos_f[:1], int(Pos_f[1:])] #letra, numero
		posibles = [] #lista de posibles jugadas, cada elemento sera [letra, numero], numero en int
		posiblesRef = [] #lista refinada de "posibles"
		assert(Matriz[Pos_i[1]][Pos_i[0]].lower() == "a") #que el inicial sea torre y el final distinto de 0
		if not (EstadoPartida or Solucion):
			assert(Matriz[Pos_f[1]][Pos_f[0]] != 0 and Matriz[Pos_f[1]][Pos_f[0]].lower() != "r")

		#En este for, se construye la lista de posibles para el alfil, sin refinar.
		for i in range (-3,4): #Pasando por -3,-2,-1,0,1,2,3
			if i == 0:
				pass
			else:
				for numero, diccionario in Matriz.items():
					for letra, pieza in diccionario.items():			
						if (numero == Pos_i[1] + i) and (letra == CambioLetra(Pos_i[0], i)): #Diagonal 1
							if pieza != 0 and pieza.lower() != 'r' and letra != Pos_i[0]: #Si hay una pieza				
								posibles.append([letra, numero])
						if (numero == Pos_i[1] + i) and (letra == CambioLetra(Pos_i[0], -i)): #Diagonal 2
							if pieza != 0 and pieza.lower() != 'r' and numero != Pos_i[1]: #Si hay una pieza
								posibles.append([letra, numero])

		#Variables usadas para refinar la lista de posibles jugadas
		tmp_letra_mayor_1 = 'z'
		tmp_letra_mayor_2 = 'z'
		tmp_letra_menor_1 = '1'
		tmp_letra_menor_2 = '1'
		tmp_Ypos_Xpos = "No"
		tmp_Ypos_Xneg = "No"
		tmp_Yneg_Xpos = "No"
		tmp_Yneg_Xneg = "No"

		#Refinando la lista
		for valor in posibles:
			if valor[1] > Pos_i[1]: #Numero mayor al inicial #(Eje 'y'+)	
				if valor[0] > Pos_i[0]: #letra mayor a la inicial #(Eje 'y'+ 'x'+)
					if valor[0] < tmp_letra_mayor_1:	#Tengo que buscar la menor letra posible, inicialmente comparandola con la mayor
						tmp_letra_mayor_1 = valor[0]
						tmp_Ypos_Xpos = valor
				elif valor[0] < Pos_i[0]: #letra menor a la inicial	#(Eje 'y'+ 'x'-)
					if valor[0] > tmp_letra_menor_1:	#Tengo que buscar la mayor letra posible, inicialmente comparandola con la menor
						tmp_letra_menor_1 = valor[0]
						tmp_Ypos_Xneg = valor

			elif valor[1] < Pos_i[1]: #Numero menor al inicial () #(Eje 'y'-)
				if valor[0] > Pos_i[0]: #letra mayor a la inicial #(Eje 'y'- 'x'+ )
					if valor[0] < tmp_letra_mayor_2:	#Tengo que buscar la mayor letra posible, inicialmente comparandola con la menor		
						tmp_letra_mayor_2 = valor[0]
						tmp_Yneg_Xpos = valor			
				elif valor[0] < Pos_i[0]:  #letra menor a la inicial #(Eje 'y'- 'x'- )
					if valor[0] > tmp_letra_menor_2:	#Tengo que buscar la menor letra posible, inicialmente comparandola con la mayor
						tmp_letra_menor_2 = valor[0]
						tmp_Yneg_Xneg = valor
		
		#anadiendo a posiblesRef
		if tmp_Ypos_Xpos !=    "No":
			posiblesRef.append(tmp_Ypos_Xpos)
		if tmp_Ypos_Xneg !=    "No":
			posiblesRef.append(tmp_Ypos_Xneg)
		if tmp_Yneg_Xpos != "No":
			posiblesRef.append(tmp_Yneg_Xpos)
		if tmp_Yneg_Xneg != "No":
			posiblesRef.append(tmp_Yneg_Xneg)

		if Solucion:
			try:
				Pos_f = posiblesRef[0]
			except:
				print("No hay jugadas posibles")
				return

		if EstadoPartida:
			return posibles

		if not EstadoPartida:
			#En este for se busca la posicion final entre los posibles y se cambia el inicial por "0" y el final por la torre
			if [Pos_f[0], int(Pos_f[1])] in posiblesRef:
				try:
					PosPiezas.remove((Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('D' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('A' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('C' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('T' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass			

				PosPiezas.remove("A" + (Pos_i[0] + str(Pos_i[1])).lower())
			else:
				print("Si la pieza inicial era un alfil, la jugada fue invalida")

			for posible in posiblesRef:
				if posible[0] == Pos_f[0] and posible[1] == Pos_f[1]:
					PosPiezas.append("A" + Pos_f[0] + str(Pos_f[1]))
					print("La jugada con el Alfil en (" + Pos_i[0] + ", " + str(Pos_i[1]) + ") a la posicion (" + Pos_f[0] + ", " + str(Pos_f[1]) + ") ha sido exitosa.")

			return PosPiezas	

	except:
		pass


 #Falta anadir la parte del Alfil que esta siendo trabajada

 #Actualmente necesita anadirse el metodo de busqueda y de refinamiento del alfil

def Reina(Pos_i, Pos_f, Matriz, PosPiezas, EstadoPartida, Solucion):
	try:
		Pos_i = [Pos_i[:1], int(Pos_i[1:])] #letra, numero
		if not (EstadoPartida or Solucion):
			Pos_f = [Pos_f[:1], int(Pos_f[1:])] #letra, numero
		posibles = [] #lista de posibles jugadas, cada elemento sera [letra, numero], numero en int
		posiblesRef = [] #lista refinada de "posibles"
		assert(Matriz[Pos_i[1]][Pos_i[0]].lower() == "d") #que el inicial sea torre y el final distinto de 0
		if not (EstadoPartida or Solucion):
			assert(Matriz[Pos_f[1]][Pos_f[0]] != 0 and Matriz[Pos_f[1]][Pos_f[0]].lower() != "r")

	#Funcion de Torre + Funcion de Alfil de posibles
		for i in range (-3,4): #Pasando por -3,-2,-1,0,1,2,3
			if i == 0:
				pass
			else:
				for numero, diccionario in Matriz.items():
					for letra, pieza in diccionario.items():			
						if (numero == Pos_i[1] + i) and (letra == CambioLetra(Pos_i[0], i)): #Diagonal 1
							if pieza != 0 and pieza.lower() != 'r' and letra != Pos_i[0]: #Si hay una pieza				
								posibles.append([letra, numero])
						if (numero == Pos_i[1] + i) and (letra == CambioLetra(Pos_i[0], -i)): #Diagonal 2
							if pieza != 0 and pieza.lower() != 'r' and numero != Pos_i[1]: #Si hay una pieza
								posibles.append([letra, numero])
					
						if numero == Pos_i[1]: #Primero trabajamos en el eje de los numeros
							if pieza != 0 and pieza.lower() != 'r' and letra != Pos_i[0]: #Si hay una pieza				
								posibles.append([letra, numero])
						if letra == Pos_i[0]: #Ahora trabajamos en el eje de las letras
							if pieza != 0 and pieza.lower() != 'r' and numero != Pos_i[1]: #Si hay una pieza
								posibles.append([letra, numero])

	#Funcion de Torre + Funcion de Alfil de refinamiento
		#Variables usadas para refinar la lista de posibles jugadas
		tmp_letra_mayor = 'z'
		tmp_letra_menor = '1'
		tmp_numero_mayor = 10
		tmp_numero_menor = 0
		TMPNumLETRA =    "No" #Variable que almacena la pieza mas cercana a la Reina, por la   derecha de la Torre
		tmpNumletra =    "No" #Variable que almacena la pieza mas cercana a la Reina, por la izquierda de la Torre
		tmpLetraNUMERO = "No" #Variable que almacena la pieza mas cercana a la Reina, por       arriba de la Torre
		tmpLetranumero = "No" #Variable que almacena la pieza mas cercana a la Reina, por        abajo de la Torre

		#Variables usadas para refinar la lista de posibles jugadas
		tmp_letra_mayor_1 = 'z'
		tmp_letra_mayor_2 = 'z'
		tmp_letra_menor_1 = '1'
		tmp_letra_menor_2 = '1'
		tmp_Ypos_Xpos = "No"
		tmp_Ypos_Xneg = "No"
		tmp_Yneg_Xpos = "No"
		tmp_Yneg_Xneg = "No"

		#Refinando la lista
		for valor in posibles:
			if valor[1] > Pos_i[1]: #Numero mayor al inicial #(Eje 'y'+)	
				if valor[0] > Pos_i[0]: #letra mayor a la inicial #(Eje 'y'+ 'x'+)
					if valor[0] < tmp_letra_mayor_1:	#Tengo que buscar la menor letra posible, inicialmente comparandola con la mayor
						tmp_letra_mayor_1 = valor[0]
						tmp_Ypos_Xpos = valor
				elif valor[0] < Pos_i[0]: #letra menor a la inicial	#(Eje 'y'+ 'x'-)
					if valor[0] > tmp_letra_menor_1:	#Tengo que buscar la mayor letra posible, inicialmente comparandola con la menor
						tmp_letra_menor_1 = valor[0]
						tmp_Ypos_Xneg = valor
						
			elif valor[1] < Pos_i[1]: #Numero menor al inicial () #(Eje 'y'-)
				if valor[0] > Pos_i[0]: #letra mayor a la inicial #(Eje 'y'- 'x'+ )
					if valor[0] < tmp_letra_mayor_2:	#Tengo que buscar la mayor letra posible, inicialmente comparandola con la menor		
						tmp_letra_mayor_2 = valor[0]
						tmp_Yneg_Xpos = valor			
				elif valor[0] < Pos_i[0]:  #letra menor a la inicial #(Eje 'y'- 'x'- )
					if valor[0] > tmp_letra_menor_2:	#Tengo que buscar la menor letra posible, inicialmente comparandola con la mayor
						tmp_letra_menor_2 = valor[0]
						tmp_Yneg_Xneg = valor

			elif valor[1] == Pos_i[1]: #Mismo numero
				if valor[0] > Pos_i[0]: #letra mayor a la inicial
					if valor[0] < tmp_letra_mayor: #El valor actual", valor[0], "es menor que la tmp actual", tmp_letra_mayor
						tmp_letra_mayor = valor[0]
						TMPNumLETRA = valor
				elif valor[0] < Pos_i[0]: #letra menor a la inicial
					if valor[0] > tmp_letra_menor:
						tmp_letra_menor = valor[0]
						tmpNumletra = valor

			if valor[0] == Pos_i[0]: #Misma letra
				if valor[1] > Pos_i[1]: #
					if valor[1] < tmp_numero_mayor: #El valor actual", valor[1], "es menor que la tmp actual", tmp_numero_mayor
						tmp_numero_mayor = valor[1]
						tmpLetraNUMERO = valor			
				elif valor[1] < Pos_i[1]: #numero menor al inicial
					if valor[1] > tmp_numero_menor:
						tmp_numero_menor = valor[1]
						tmpLetranumero = valor	

		#anadiendo a posiblesRef
		if tmp_Ypos_Xpos !=    "No":
			posiblesRef.append(tmp_Ypos_Xpos)
		if tmp_Ypos_Xneg !=    "No":
			posiblesRef.append(tmp_Ypos_Xneg)
		if tmp_Yneg_Xpos != "No":
			posiblesRef.append(tmp_Yneg_Xpos)
		if tmp_Yneg_Xneg != "No":
			posiblesRef.append(tmp_Yneg_Xneg)

		if TMPNumLETRA !=    "No":
			posiblesRef.append(TMPNumLETRA)
		if tmpNumletra !=    "No":
			posiblesRef.append(tmpNumletra)
		if tmpLetraNUMERO != "No":
			posiblesRef.append(tmpLetraNUMERO)
		if tmpLetranumero != "No":
			posiblesRef.append(tmpLetranumero)

		if Solucion:
			try:
				Pos_f = posiblesRef[0]
			except:
				print("No hay jugadas posibles")
				return

		if EstadoPartida:
			return posibles

		if not EstadoPartida:
			#Funcion de Remover lo inicial + final y anadir Reina al final
			if [Pos_f[0], int(Pos_f[1])] in posiblesRef:
				try:
					PosPiezas.remove((Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('A' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('C' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('T' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass			

				PosPiezas.remove("D" + (Pos_i[0] + str(Pos_i[1])).lower())
			else:
				print("Si la pieza inicial era una reina, la jugada fue invalida")

			for posible in posiblesRef:
				if posible[0] == Pos_f[0] and posible[1] == Pos_f[1]:
					PosPiezas.append("D" + Pos_f[0] + str(Pos_f[1]))
					print("La jugada con la Reina en (" + Pos_i[0] + ", " + str(Pos_i[1]) + ") a la posicion (" + Pos_f[0] + ", " + str(Pos_f[1]) + ") ha sido exitosa.")
			return PosPiezas	

	except:
		pass

def Rey(Pos_i, Pos_f, Matriz, PosPiezas, EstadoPartida, Solucion):
	try:
		Pos_i = [Pos_i[:1], int(Pos_i[1:])] #letra, numero
		if not (EstadoPartida or Solucion):
			Pos_f = [Pos_f[:1], int(Pos_f[1:])] #letra, numero
		posibles = [] #lista de posibles jugadas, cada elemento sera [letra, numero], numero en int
		assert(Matriz[Pos_i[1]][Pos_i[0]].lower() == "r") #que el inicial sea torre y el final distinto de 0
		if not (EstadoPartida or Solucion):
			assert(Matriz[Pos_f[1]][Pos_f[0]] != 0)

		#En este for, se construye la lista de posibles para el peon, sin refinar.
		for numero, diccionario in Matriz.items():
			for letra, pieza in diccionario.items():
				if pieza != 0 and letra == CambioLetra(Pos_i[0], 1) and numero == Pos_i[1] + 1:
					posibles.append([letra, numero])		
				if pieza != 0 and letra == CambioLetra(Pos_i[0], 0) and numero == Pos_i[1] + 1:
					posibles.append([letra, numero])
				if pieza != 0 and letra == CambioLetra(Pos_i[0],-1) and numero == Pos_i[1] + 1:
					posibles.append([letra, numero])	
				if pieza != 0 and letra == CambioLetra(Pos_i[0], 1) and numero == Pos_i[1] + 0:
					posibles.append([letra, numero])	
				if pieza != 0 and letra == CambioLetra(Pos_i[0],-1) and numero == Pos_i[1] + 0:
					posibles.append([letra, numero])		
				if pieza != 0 and letra == CambioLetra(Pos_i[0], 1) and numero == Pos_i[1] - 1:
					posibles.append([letra, numero])
				if pieza != 0 and letra == CambioLetra(Pos_i[0], 0) and numero == Pos_i[1] - 1:
					posibles.append([letra, numero])	
				if pieza != 0 and letra == CambioLetra(Pos_i[0],-1) and numero == Pos_i[1] - 1:
					posibles.append([letra, numero])

		if Solucion:
			try:
				Pos_f = posibles[0]
			except:
				print("No hay jugadas posibles")
				return

		if EstadoPartida:
			return posibles

		if not EstadoPartida:
			if [Pos_f[0], int(Pos_f[1])] in posibles:
				try:
					PosPiezas.remove((Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('D' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:
					PosPiezas.remove('A' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('C' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass
				try:			
					PosPiezas.remove('T' + (Pos_f[0] + str(Pos_f[1])).lower())
				except:
					pass		

				PosPiezas.remove("R" + (Pos_i[0] + str(Pos_i[1])).lower())
			else:
				print("Si la pieza inicial era un rey, la jugada fue invalida")

			for posible in posibles:
				if posible[0] == Pos_f[0] and posible[1] == Pos_f[1]:
					PosPiezas.append("R" + Pos_f[0] + str(Pos_f[1]))
					print("La jugada con el Rey en (" + Pos_i[0] + ", " + str(Pos_i[1]) + ") a la posicion (" + Pos_f[0] + ", " + str(Pos_f[1]) + ") ha sido exitosa.")
			return PosPiezas	


	except:
		pass


def LeerRecords():
	
	pygame.display.set_mode((1280, 1024))
	
	class LineaDeRecord:
		def __init__(self, nombre, dificultad, puntuaje):
			self.nombre = nombre
			self.dificultad = dificultad
			self.puntuaje = puntuaje
		
		def __repr__(self): #Con esta funcion ganamos control de que devuelva valores en vez de object id
			return repr((self.puntuaje, self.nombre)) #Devolviendo en orden puntuaje, nombre (sin dificultad)

	ListaTutorial = []
	ListaFacil = []
	ListaDificil = []
	ListaMuyDificil = []
	with open("Texts/records.txt", "r+") as archivo:
		for linea in archivo:
			linea = tuple(linea.split())

			if linea[1] == "Tutorial":
				ListaTutorial.append(LineaDeRecord(*linea)) #Con el asterisco se toma la topla como raw y se usa como argumento de la clase
			elif linea[1] == "Facil":
				ListaFacil.append(LineaDeRecord(*linea))
			elif linea[1] == "Dificil":
				ListaDificil.append(LineaDeRecord(*linea))
			elif linea[1] == "Muy_Dificil":
				ListaMuyDificil.append(LineaDeRecord(*linea))

		ListaTutorial = sorted(ListaTutorial, key = attrgetter('nombre')) #se ordena el nombre no en reversa
		ListaTutorial = sorted(ListaTutorial, key = attrgetter('puntuaje'), reverse = True) #se ordena el restante en puntuaje en reversa
		
		ListaFacil = sorted(ListaFacil, key = attrgetter('nombre')) #se ordena el nombre no en reversa
		ListaFacil = sorted(ListaFacil, key = attrgetter('puntuaje'), reverse = True) #se ordena el restante en puntuaje en reversa
		
		ListaDificil = sorted(ListaDificil, key = attrgetter('nombre')) #se ordena el nombre no en reversa
		ListaDificil = sorted(ListaDificil, key = attrgetter('puntuaje'), reverse = True) #se ordena el restante en puntuaje en reversa
		
		ListaMuyDificil = sorted(ListaMuyDificil, key = attrgetter('nombre')) #se ordena el nombre no en reversa
		ListaMuyDificil = sorted(ListaMuyDificil, key = attrgetter('puntuaje'), reverse = True) #se ordena el restante en puntuaje en reversa


		#limitamos a 5 elementos por cada dificultad
		while True:
			#Refresca los eventos a esta variable
			eventos = pygame.event.get()
			#Variable que verifica si una tecla esta presionada
			presionada = pygame.key.get_pressed()
		    #Evento para salir hacia el menu Principal o para cargar el juego en su respectivo nivel
			for event in eventos:

				if event.type == pygame.locals.QUIT: 
					pygame.quit() 
					sys.exit()
				if presionada[pygame.K_RETURN]:
					return 				
			gameDisplay.blit(ScoreboardPNG,(0,0))

			try:
				gameDisplay.blit(Font.render(ListaTutorial[0].puntuaje + " " + ListaTutorial[0].nombre, True, white), (71, 247))
				gameDisplay.blit(Font.render(ListaTutorial[1].puntuaje + " " + ListaTutorial[1].nombre, True, white), (88, 312))
				gameDisplay.blit(Font.render(ListaTutorial[2].puntuaje + " " + ListaTutorial[2].nombre, True, white), (81, 369))
				gameDisplay.blit(Font.render(ListaTutorial[3].puntuaje + " " + ListaTutorial[3].nombre, True, white), (83, 431))
				gameDisplay.blit(Font.render(ListaTutorial[4].puntuaje + " " + ListaTutorial[4].nombre, True, white), (75, 495))
			except:
				pass

			try:
				gameDisplay.blit(Font.render(ListaFacil[0].puntuaje + " " + ListaFacil[0].nombre, True, white), (775, 276))
				gameDisplay.blit(Font.render(ListaFacil[1].puntuaje + " " + ListaFacil[1].nombre, True, white), (794, 344))
				gameDisplay.blit(Font.render(ListaFacil[2].puntuaje + " " + ListaFacil[2].nombre, True, white), (780, 405))
				gameDisplay.blit(Font.render(ListaFacil[3].puntuaje + " " + ListaFacil[3].nombre, True, white), (787, 464))
				gameDisplay.blit(Font.render(ListaFacil[4].puntuaje + " " + ListaFacil[4].nombre, True, white), (791, 524))
			except:
				pass

			try:
				gameDisplay.blit(Font.render(ListaDificil[0].puntuaje + " " + ListaDificil[0].nombre, True, white), (63, 729))
				gameDisplay.blit(Font.render(ListaDificil[1].puntuaje + " " + ListaDificil[1].nombre, True, white), (78, 794))
				gameDisplay.blit(Font.render(ListaDificil[2].puntuaje + " " + ListaDificil[2].nombre, True, white), (74, 860))
				gameDisplay.blit(Font.render(ListaDificil[3].puntuaje + " " + ListaDificil[3].nombre, True, white), (85, 918))
				gameDisplay.blit(Font.render(ListaDificil[4].puntuaje + " " + ListaDificil[4].nombre, True, white), (80, 974))
			except:
				pass

			try:
				gameDisplay.blit(Font.render(ListaMuyDificil[0].puntuaje + " " + ListaMuyDificil[0].nombre, True, white), (744, 706))
				gameDisplay.blit(Font.render(ListaMuyDificil[1].puntuaje + " " + ListaMuyDificil[1].nombre, True, white), (747, 775))
				gameDisplay.blit(Font.render(ListaMuyDificil[2].puntuaje + " " + ListaMuyDificil[2].nombre, True, white), (738, 833))
				gameDisplay.blit(Font.render(ListaMuyDificil[3].puntuaje + " " + ListaMuyDificil[3].nombre, True, white), (743, 891))
				gameDisplay.blit(Font.render(ListaMuyDificil[4].puntuaje + " " + ListaMuyDificil[4].nombre, True, white), (745, 948))
			except:
				pass

			#Actualiza los dibujos de la pantalla a un determinado FPS
			pygame.display.update()
			fpsClock.tick(FPS)		


#Se asigna a la variable Usuario el nombre del usuario

global Usuario
Usuario = LoopIntro()

#Se ejecuta el loop principal que contiene al menu y demas cosas
LoopPrincipal()