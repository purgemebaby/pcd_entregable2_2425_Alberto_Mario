Por Mario Sáez Muela y Alberto Algarate Pastor
--
#Patrones-de-diseño #Programación-Funcional #Streams
--
---

### 2. Histórico de Git

Inicializamos nuestro repositorio local:
$\hspace{2pt}$
![[Pasted image 20250412024544.png|center]]
$\hspace{2pt}$
Luego creamos el repositorio remoto, que estará compartido con los miembros del equipo:


![[Pasted image 20250412024911.png|center]]
$\hspace{2pt}$

Realizamos un `git switch -c development` y realizamos nuestro 1º _commit_.

![[Pasted image 20250412030127.png|center]]

Para mayor claridad en los mensajes de los _commits_, hemos añadido un **<span style="color:rgb(107, 123, 118)">git hook</span>** donde se coge la rama actual y se inserta al principio de la línea del mensaje:

```sh
#!C:\Program Files\Git\usr\bin\sh.exe
branch = $(git branch --show-current)
if [[ -f "$1"]]; then
	sed -i "1s/^/$branch: /" "$1"  
```
$\hspace{2pt}$
El resultado tras el 1º _push_ es exitoso:

>[!column] Git Push
>> [!note|clean no-title]
>> ![[Pasted image 20250412030950.png]]
>
>>[!note|clean no-title]
>>![[Pasted image 20250412031253.png]]


Procesado de datos ~ Cadena de responsabilidad

Subscriptor mientras que se vaya modificando los valores



#### Restricciones cumplidas (Conservar solo motivos de diseño)

-  R1 Hecho, Falta hacer literalmente toda la clase XD. Se decidió seguir el patrón de diseño _Singleton_ para tatata.

-  R2 se ha hecho el update, falta conectarlo para que lo vaya notificando al servidor, a su vez, cada vez que se llame a esta funcion, luego se llamará a una funcion para recoger los datos. Cuando en concreto se recojan las coordenas, se llamará al Adapter para que hago su chambeo. Los camiones se actualizarán a través del observer, mandando al servidor la nueva información.

-  R5 Hecho, Falta conectarlo con el """"servidor""". Se decidió seguir el patrón de diseño _Adapter_ de objeto para cumplir con el requisito de conversión de coordenadas _GMS_ a _OCL_ para su posterior almacenamiento. Se siguió el siguiente esquema **UML**:

mover lo de la media y desviación a una cadena de decisión.