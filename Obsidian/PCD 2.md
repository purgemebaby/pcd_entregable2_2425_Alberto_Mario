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

