# Proyecto No. 3
# Generación de Analizadores Sintácticos

### Diseño de Lenguajes de Programación - Sección 10
### María Fernanda Estrada 14198
### Junio 2021
------------------------------------------------------------------------------------------------------
#### Link de video explicativo
s
#### Para ejecutar el proyecto (Paso 1)
Ejecutar el proyecto con el siguiente comando: `python Proyecto2.py testDouble.ATG`. En el repositorio se encuentra el archivo ATG de python para este proyecto. Se lee el archivo ATG y se generan regex de los tokens indicados en este archivo para luego generar autómatas. También se leen las producciones y en base a ellas se genera el Parser.
#### Para ejecutar el proyecto (Paso 2)
Por el paso anterior, se genera el archivo `Scanner.py` y `Parser.py`. El primero contiene la información para simular los autómatas generados en el paso anterior. El segundo contiene las funciones para analizar sintácticamente un archivo de texto. Para analizar un archivo de texto, se debe ejecutar el siguiente comando: `python Parser.py *nombre_archivo.txt*`. Esto devolverá el resultado de las operaciones que se encuentren escritas. Las operaciones deben ir sin espacios, separadas por punto y coma, y terminando en un punto. Por ejemplo `5+5;95+1;0.5*(1+2);-(5)/5;.`
