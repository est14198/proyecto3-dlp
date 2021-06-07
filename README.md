# Proyecto No. 2
# Generación de Analizadores Léxicos

### Diseño de Lenguajes de Programación - Sección 10
### María Fernanda Estrada 14198
### Abril 2021
------------------------------------------------------------------------------------------------------
#### Link de video explicativo
https://youtu.be/-nA7LoYX58Y
#### Para ejecutar el proyecto (Paso 1)
Ejecutar el proyecto con el siguiente comando: `python Proyecto2.py *nombre_archivo.ATG*`. En el repositorio se encuentran los 4 archivos ATG de prueba para este proyecto. Se lee el archivo ATG y se generan regex de los tokens indicados en este archivo para luego generar autómatas.
#### Para ejecutar el proyecto (Paso 2)
Por el paso anterior, se genera el archivo `Scanner.py`. Este contiene la información para simular los autómatas generados en el paso anterior. Para analizar un archivo de texto, se debe ejecutar el siguiente comando: `python Scanner.py *nombre_archivo.txt*`. Esto imprimirá los token encontrados y el tipo de token que es.
