PAV - P5: síntesis musical polifónica
=====================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 5](https://github.com/albino-pav/P5) 
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde que
los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A modo de memoria de la práctica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

Ejercicios.
-----------

### Envolvente ADSR.

Tomando como modelo un instrumento sencillo (puede usar el InstrumentDumb), genere cuatro instrumentos que
permitan visualizar el funcionamiento de la curva ADSR.

* Un instrumento con una envolvente ADSR genérica, para el que se aprecie con claridad cada uno de sus
  parámetros: ataque (A), caída (D), mantenimiento (S) y liberación (R).

````
Seno	ADSR_A=0.2; ADSR_D=0.2; ADSR_S=0.2; ADSR_R=0.2; N=16;
````

- ADSR_A (Attack): 0.2, este parámetro determina cuánto tiempo tarda en alcanzar el nivel máximo de amplitud después de que se ha iniciado un sonido.
- ADSR_D (Decay): 0.2, este parámetro determina cuánto tiempo tarda en alcanzar el nivel de sostenimiento después de que se ha alcanzado el nivel máximo de amplitud.
- ADSR_S (Sustain): 0.2, este parámetro determina el nivel de amplitud en el que se mantiene el sonido mientras se mantiene presionada una tecla.
- ADSR_R (Release): 0.2, este parámetro determina cuánto tiempo tarda en llegar a 0 el nivel de amplitud después de que se ha liberado una tecla.
- N: 16, el número de muestras en un período de onda senoidal.

Con estos parámetros, cada fase de la envolvente ADSR será clara y fácilmente perceptible, ya que todos los parámetros tienen un valor de 0.2. El ataque será rápido, el decaimiento y el sostenimiento serán moderados y la liberación será rápida. Este instrumento generará un sonido sencillo con una envolvente fácilmente perceptible.
![](work/plots/res/Figure_1.png)

* Un instrumento *percusivo*, como una guitarra o un piano, en el que el sonido tenga un ataque rápido, no
  haya mantenimiemto y el sonido se apague lentamente.
  - Para un instrumento de este tipo, tenemos dos situaciones posibles:
    * El intérprete mantiene la nota *pulsada* hasta su completa extinción.

```
Seno	ADSR_A=0.02; ADSR_D=0.9; ADSR_S=0.0; ADSR_R=0.0; N=16;
```
![](work/plots/res/Figure_2.png)

  * El intérprete da por finalizada la nota antes de su completa extinción, iniciándose una disminución
  abrupta del sonido hasta su finalización.

```
Seno	ADSR_A=0.02; ADSR_D=0.9; ADSR_S=0.0; ADSR_R=0.0; N=16;
```

  ![](work/plots/res/Figure_3.png)
  - Debera representar en esta memoria **ambos** posibles finales de la nota.


* Un instrumento *plano*, como los de cuerdas frotadas (violines y semejantes) o algunos de viento. En
  ellos, el ataque es relativamente rápido hasta alcanzar el nivel de mantenimiento (sin sobrecarga), y la
  liberación también es bastante rápida.

```
Seno	ADSR_A=0.05; ADSR_D=0.02; ADSR_S=0.4; ADSR_R=0.2; N=40;
```

![](work/plots/res/Figure_4.png)


Para los cuatro casos, deberá incluir una gráfica en la que se visualice claramente la curva ADSR. Deberá
añadir la información necesaria para su correcta interpretación, aunque esa información puede reducirse a
colocar etiquetas y títulos adecuados en la propia gráfica (se valorará positivamente esta alternativa).

### Instrumentos Dumb y Seno.

Implemente el instrumento `Seno` tomando como modelo el `InstrumentDumb`. La señal **deberá** formarse
mediante búsqueda de los valores en una tabla.

- Incluya, a continuación, el código del fichero `seno.cpp` con los métodos de la clase Seno.

Este código es una implementación de un sintetizador de ondas senoidales utilizando el método Linear Interpolation (Lerp) para generar una onda suave y continua. 

```cpp
#include <iostream>
#include <iomanip> 
#include <fstream>
#include <math.h>
#include "seno.h"
#include "keyvalue.h"

#include <stdlib.h>

using namespace upc;
using namespace std;

Seno::Seno(const std::string &param)
  : adsr(SamplingRate, param) {
  bActive = false;
  x.resize(BSIZE);

  KeyValue kv(param);

  if (!kv.to_int("N", N)) {
    N = 40; //default value
  }

  //Create a tbl with one period of a sinusoidal wave
  tbl.resize(N);
  float phase = 0, step = 2 * M_PI /(float) N;
  index = 0.0f;

  for (int i=0; i < N ; ++i) {
    tbl[i] = sin(phase);
    phase += step;
  }
}
```
La clase Seno tiene un constructor que toma un parámetro de cadena y utiliza la clase KeyValue para inicializar un parámetro N que es el número de muestras en un período de onda senoidal. 

```cpp
void Seno::command(long cmd, long note, long vel) {
  if (cmd == 9) {		//'Key' pressed: attack begins
    bActive = true;
    adsr.start();
    index = 0;

    if (vel > 127) {
        vel = 127;
    }
    A = vel / 127.0f;

    // Calculate delta for the table index
    float f0_note = 440 * powf(2, (note - 69.0f) / 12.0f);
    delta_idx = (float)N * f0_note / SamplingRate;
    
  } else if (cmd == 8) {	//'Key' released: sustain ends, release begins
    adsr.stop();

  } else if (cmd == 0) {	//Sound extinguished without waiting for release to end
    adsr.end();
  }
}
```

El método "command" que se utiliza para recibir comandos desde un teclado o controlador MIDI. Este método se utiliza para iniciar, detener y finalizar un sonido.

```cpp
const vector<float> & Seno::synthesize() {
  
  fstream f;

  f.open("work/Lerp.txt", ios::out | ios::app);

  if (not adsr.active()) {
    x.assign(x.size(), 0);
    bActive = false;
    return x;

  } else if (not bActive) {
    return x;
  }

  float frac;
  int il, ir;

  for (unsigned int i = 0; i < x.size(); ++i, index += delta_idx) {
    // It's like the modulus operator but with floats
    while (index > (float)tbl.size()) { index -= (float)tbl.size();}

    // Get base and fraction indices
    il = (int)floor(index);
    frac = index - (float)il;
    ir = il == N-1 ? 0 : il + 1;

    // Lerp
    x[i] = A * ((1-frac)*tbl[il] + frac*tbl[ir]);
  }

  //apply envelope to x and update internal status of ADSR
  adsr(x);

  return x;
}
```
En el método de síntesis, la clase utiliza una tabla de valores precalculados de seno y utiliza un índice para seleccionar los valores de la tabla y lerp para interpolarlos para generar una onda continua. El método de síntesis también aplica el envoltorio adsr a la onda generada antes de devolverla.

- Explique qué método se ha seguido para asignar un valor a la señal a partir de los contenidos en la tabla,
  e incluya una gráfica en la que se vean claramente (use pelotitas en lugar de líneas) los valores de la
  tabla y los de la señal generada.

El método utilizado para asignar un valor a la señal a partir de los contenidos en la tabla es el método de interpolación lineal, también conocido como Lerp. Este método se utiliza para generar un valor intermedio entre dos valores conocidos, en este caso, dos valores de la tabla de valores precalculados de seno.

En el método de síntesis, se utiliza un índice para seleccionar los valores de la tabla. El índice se actualiza en cada iteración del bucle for con un valor delta_idx, que es calculado en el método command. Luego, en cada iteración, se utiliza el índice para calcular el índice de base (il) y el índice de fracción (frac) de la tabla. El índice de base se calcula mediante la función floor y el índice de fracción se calcula restando el índice de base del índice total.

Una vez que se tiene el índice de base e índice de fracción, se utilizan para calcular el valor intermedio en la señal. Se selecciona el valor de la tabla en el índice de base (il) y en el índice siguiente (ir) y se utilizan para calcular el valor intermedio en la señal. El valor intermedio se calcula mediante la fórmula (1-frac)tbl[il] + fractbl[ir], donde tbl es la tabla de valores precalculados de seno.

En resumen, se utiliza el método de interpolación lineal para asignar un valor a la señal a partir de los contenidos en la tabla, eligiendo dos valores de la tabla y utilizando un índice de fracción para calcular un valor intermedio entre ellos.

![](work/plots/res/Figure_5.png)


- Si ha implementado la síntesis por tabla almacenada en fichero externo, incluya a continuación el código
  del método `command()`.

### Efectos sonoros.

- Incluya dos gráficas en las que se vean, claramente, el efecto del trémolo y el vibrato sobre una señal
  sinusoidal. Deberá explicar detalladamente cómo se manifiestan los parámetros del efecto (frecuencia e
  índice de modulación) en la señal generada (se valorará que la explicación esté contenida en las propias
  gráficas, sin necesidad de *literatura*).

Parámetros usados:
 - A: es la amplitud
 - Fm: La frecuencia en la que se aplica el efecto. 
 - I: Índice de modulación

![](work/plots/res/Figure_6.png)

![](work/plots/res/Figure_7.png)

![](work/plots/res/Figure_8.png)

![](work/plots/res/Figure_9.png)

![](work/plots/res/Figure_10.png)


- Si ha generado algún efecto por su cuenta, explique en qué consiste, cómo lo ha implementado y qué
  resultado ha producido. Incluya, en el directorio `work/ejemplos`, los ficheros necesarios para apreciar
  el efecto, e indique, a continuación, la orden necesaria para generar los ficheros de audio usando el
  programa `synth`.

### Síntesis FM.

Construya un instrumento de síntesis FM, según las explicaciones contenidas en el enunciado y el artículo
de [John M. Chowning](https://web.eecs.umich.edu/~fessler/course/100/misc/chowning-73-tso.pdf). El
instrumento usará como parámetros **básicos** los números `N1` y `N2`, y el índice de modulación `I`, que
deberá venir expresado en semitonos.

- Use el instrumento para generar un vibrato de *parámetros razonables* e incluya una gráfica en la que se
  vea, claramente, la correspondencia entre los valores `N1`, `N2` e `I` con la señal obtenida.

La gráfica muestra el espectro de un tono "do" con diferentes parámetros N1, N2, I.

Podemos comprobar una frecuencia fundamental de 250 Hz.

Los parámetros para la línea azul son:
 - N1 = 1
 - N2 = 2
 - I = 3

![](work/plots/res/FMcomparación.png)


- Use el instrumento para generar un sonido tipo clarinete y otro tipo campana. Tome los parámetros del
  sonido (N1, N2 e I) y de la envolvente ADSR del citado artículo. Con estos sonidos, genere sendas escalas
  diatónicas (fichero `doremi.sco`) y ponga el resultado en los ficheros `work/doremi/clarinete.wav` y
  `work/doremi/campana.work`.
  * También puede colgar en el directorio work/doremi otras escalas usando sonidos *interesantes*. Por
    ejemplo, violines, pianos, percusiones, espadas láser de la
	[Guerra de las Galaxias](https://www.starwars.com/), etc.


**Campana**
````
SynthFM ADSR_A=0.01; ADSR_D=0.50; ADSR_S=0.00; ADSR_R=0.00; I=10.0; N1=1.0; N2=1.6;
````

```sh
synth work/instruments/campana.orc work/score/doremi.sco work/doremi/campana.wav
```

![](work/plots/res/Figure_12.png)


**Clarinete**
````
SynthFM ADSR_A=0.10; ADSR_D=0.00; ADSR_S=1.00; ADSR_R=0.05; I=4.0; N1=3.0; N2=2.0;
````

```sh
synth work/instruments/clarinete.orc work/score/doremi.sco work/doremi/clarinete.wav
```

![](work/plots/res/Figure_13.png)


### Orquestación usando el programa synth.

Use el programa `synth` para generar canciones a partir de su partitura MIDI. Como mínimo, deberá incluir la
*orquestación* de la canción *You've got a friend in me* (fichero `ToyStory_A_Friend_in_me.sco`) del genial
[Randy Newman](https://open.spotify.com/artist/3HQyFCFFfJO3KKBlUfZsyW/about).

- En este triste arreglo, la pista 1 corresponde al instrumento solista (puede ser un piano, flautas,
  violines, etc.), y la 2 al bajo (bajo eléctrico, contrabajo, tuba, etc.).

Estos parámetros están diseñados para simular el sonido de un piano eléctrico, donde el ataque es rápido, el decaimiento es moderado, el nivel de sostenimiento es moderado y el tiempo de liberación es rápido. Los valores de Index Modulation y Ratio de modulación de frecuencia son utilizados para generar un sonido más complejo en el piano eléctrico.

```
# Electric Piano
1   SynthFM ADSR_A=0.005;   ADSR_D=0.10;    ADSR_S=0.30;    ADSR_R=0.25;    I=10.0; N1=1;   N2=2;

# Electric Bass
2   SynthFM ADSR_A=0.01;    ADSR_D=0.50;    ADSR_S=0.20;    ADSR_R=0.20;    I=4.0;  N1=7;   N2=3;
```

- Coloque el resultado, junto con los ficheros necesarios para generarlo, en el directorio `work/music`.

  - [Toy_story.wav](work/music/toy_story.wav)


- Indique, a continuación, la orden necesaria para generar la señal (suponiendo que todos los archivos
  necesarios están en directorio indicado).

```sh
synth work/instruments/toy_story.orc samples/ToyStory_A_Friend_in_me.sco work/music/toy_story.wav
```

También puede orquestar otros temas más complejos, como la banda sonora de *Hawaii5-0* o el villacinco de
John Lennon *Happy Xmas (War Is Over)* (fichero `The_Christmas_Song_Lennon.sco`), o cualquier otra canción
de su agrado o composición. Se valorará la riqueza instrumental, su modelado y el resultado final.
- Coloque los ficheros generados, junto a sus ficheros `score`, `instruments` y `efffects`, en el directorio
  `work/music`.
- Indique, a continuación, la orden necesaria para generar cada una de las señales usando los distintos
  ficheros.
