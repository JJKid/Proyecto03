README
Arroyo Rivera Juan José 416053223

Ejecución del programa:

1. Instalar python3

2. Desde esta carpeta donde esta el README, instalar las bibliotecas
ejecutando: pip install -r libraries.txt

3. Moverse a la carpeta /src y ejecutar las pruebas unitarias con el comando: python -m pytest

4. Ejecutar el comando: python Main.py c -h.
   Ó de forma análoga :  python Main.py d -h 

Esto sirve para ver las opciones validas como argumentos en la linea de comandos para 
las 2 opciones posibles: cifrar o descifrar

Para mayor referencia

	Cifrar:
		python Main.py c <archivo para guardar shares .frg> n t <archivo de entrada>

	Descifrar:
		python Main.py d <archivo donde estan las shares> <archivo encriptado>

5. Ejecutar primero la opcion c (cifrar), teclear un password y dar enter.
Se genera el archivo encriptado (.aes) y el que contiene las shares (.frg).
Tras cifrar se elimina el archivo en texto claro

6. Posteriormente usar ambos archivos generados con la opcion d (descifrar).
Tras descifrar se eliminan el archivo encriptado y el que contiene las shares,
y se recupera el archivo en texto claro con su extension original



