# D.U.M.M.Y

DUMMY

Integrantes del grupo:
  *Capote Pratts, Miguel Lincoln
  *Garcia Marrero, Aaron Adasat
  *Herrera Delgado, Víctor

*Descripción del trabajo realizado

DUMMY, es un brazo robótico capaz de detectar un objeto en la trayectoria de su recorrido agarrarlo y colocarlo en otro lugar a 
detectar.

*Construcción

Para la construcción del brazo hemos usado dos motores grandes, uno para la rotación horizontal (derecha o izquierda) y otro para la 
rotación vertical (bajar y subir el propio brazo), además usamos un motor pequeño para el agarre de los objetos, en cuanto a los 
sensores hemos hecho uso de un sensor de ultrasonidos que es el encargado de detectar el objeto y además detectar el lugar a colocarlo. 
El sensor ha sido colocado de tal manera que no choca con el brazo aun pudiendo reconocer lo que tiene delante. 
Para mejorar la eficiencia se ha implementado un contrapeso para ayudar al brazo a subir debido al peso de la garra y demás componentes.

*Manejo de sensores

En cuanto al manejo de los sensores, como ya hemos comentado, los usamos para detectar la posición del bloque a mover y el lugar a 
colocar, para ello, consultamos el sensor de manera periódica en la rotación del brazo, cuando se detecta un cambio brusco en la 
distancia con respecto al objetivo guardamos ese primer valor y seguimos rotando el brazo, cuando vuelve a suceder la situación anterior 
guardamos el segundo valor y hacemos una media, para que el motor que controla la rotación se mueva esa distancia hacia el lado 
contrario quedando así en el centro del objeto donde puede agarrarlo con mejores resultados. Debido a la diferencia de posición de la
garra con respecto del sensor es necesario sumarle un pequeño valor a la media para ajustarlo. Recalcamos además que el sensor se
encarga además de  que una vez subido el brazo tras supuestamente coger el objeto este no siga siendo detectado.
 
*Funcionamiento

El brazo empieza con una posición inicial central y bajado (tocando la base en la que se apoye) y con la garra parcialmente cerrada. El
brazo subirá y empezará su reconocimiento del espacio de 180º que tiene a su disposición teniendo para ello unos límites que apuntan
cuando debe buscar girando en el sentido contrario. Si encuentra un cambio brusco se aplica lo explicado en “Manejo de sensores” para
hallar su punto medio, tras lo cual abre la garra y pasa a bajar el nivel del brazo con la intención de coger el objeto. En caso de que
no se coja el bloque seguirá siendo detectado y se pasará a intentarlo de nuevo. Tras esto con el brazo subido y agarrando el bloque se
ejecuta una búsqueda similar a la anteriormente mencionada para encontrar el lugar en el cual se depositará el objeto.


*Algoritmo de control

El algoritmo de control usado si bien resulta simple para el movimiento lateral y la búsqueda (debido a la falta de tiempo del equipo)
se ha podido mejorar para el control de la subida del brazo en el cual se ha implementado un control proporcional-derivativo con el que
se controla una velocidad gradual del brazo en la subida, reduciendo en gran medida las oscilaciones de este.

*Prototipos descartados:

Se intentó combinar el sensor ultrasónico ya instalado con otro igual adicional que pudiera controlar la subida y bajada del brazo en
cuanto a la distancia al suelo y no en cuanto a la posición que le habíamos impuesto. El motivo de su descarte fueron las interferencias
que causaba el nuevo al original debido a su posición y la aparente inevitabilidad de tener que tener ambos sensores en acción a la vez
que impedían la correcta detección del objeto buscado.
