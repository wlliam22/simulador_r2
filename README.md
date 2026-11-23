# Simulador de trayectorias R2

Proyecto educativo de cinemática para demostrar el movimiento parabólico de un
proyectil en un plano bidimensional.

## Ejecutar localmente

Desde la carpeta del proyecto:

```powershell
.\.venv\Scripts\python.exe -m http.server 8000 --bind 127.0.0.1 --directory .\web
```

Abrir `http://127.0.0.1:8000` en el navegador.

## Probar

Con Node.js disponible:

```powershell
node tests/verify-model.js
```

Casos recomendados para la demostración:

| Velocidad | Ángulo | Resultado esperado |
|---|---:|---|
| 32 m/s | 53° | Impacto en el techo del objetivo |
| 40 m/s | 20° | Impacto en el lado izquierdo del objetivo |
| 45 m/s | 45° | Aterrizaje después de la estructura |
| 20 m/s | 45° | Aterrizaje antes del objetivo |

Para cada caso, comparar los resultados mostrados con las fórmulas teóricas:

- `V0x = V0 cos(ángulo)`
- `V0y = V0 sen(ángulo)`
- `t = 2V0y / g`
- `Hmax = V0y² / 2g`
- `Alcance = V0x * t`
- `g = 9,81 m/s²`

## Modelo físico

La simulación usa un modelo ideal: gravedad constante, plano horizontal y
ausencia de resistencia del aire. El objetivo es fijo y está ubicado a 85 m,
con 12 m de ancho y 8 m de alto.

El objetivo es una estructura de referencia para la demostración, no una
representación física de un edificio real. Los ejes representan metros y usan
la misma escala física.

## Publicar como sitio estático

La versión web es completamente estática. Puede subir solamente el contenido
de `web/` a GitHub Pages, Netlify, Cloudflare Pages u otro servicio público.
No requiere Nginx ni servicios del lado del servidor.
