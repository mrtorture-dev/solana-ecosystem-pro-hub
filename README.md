# 💎 Solana Ecosystem Pro Hub & API v1

Una infraestructura robusta de datos y analítica en tiempo real para el ecosistema **Solana**, integrando métricas de mercado de **CoinGecko** y data técnica de alta resolución desde **Binance**.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Solana](https://img.shields.io/badge/Solana-9945FF?style=for-the-badge&logo=solana&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white)

## 🚀 Características Principales

- **Doble Fuente de Datos:** Combina el historial técnico de Binance (1h, 4h, 1d) con la tendencia de mercado de 7 días de CoinGecko.
- **Filtrado Estricto Solana:** Solo proyectos reales de la red Solana verificados en Binance (sin stables ni duplicados).
- **Dashboard de Comparación:** Interfaz avanzada para comparar precios entre sectores (DeFi, LST, DePIN, Memecoins).
- **Infraestructura de API Pro:** Endpoints dinámicos listos para ser consumidos por otros desarrolladores.
- **Dockerizado:** Despliegue en segundos con un solo comando.

## 🛠️ Arquitectura de la API (v1)

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/v1/data/full` | Retorna el ecosistema completo (50 tokens + Métricas + Históricos). |
| `GET` | `/api/v1/data/sector/{name}` | Filtrado dinámico por sector (DeFi, LST, etc). |
| `GET` | `/api/v1/data/history/{sym}/{int}` | Datos técnicos OHLCV puros desde Binance. |

## 📦 Instalación y Despliegue

### Requisitos previos
- Docker y Docker Compose instalados.

### Pasos
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/solana-pro-hub.git
   cd solana-pro-hub
   ```
2. Levantar el servicio:
   ```bash
   docker-compose up --build
   ```
3. Acceder al dashboard:
   Abrir `http://localhost:8000` en tu navegador.

## 📊 Visualización de Datos
El hub permite alternar entre:
- **Binance Technical:** Velas de alta precisión para análisis de corto/mediano plazo.
- **CoinGecko 7D Trend:** Tendencia semanal con métricas de Capitalización de Mercado y Volumen.

---
Desarrollado para el ecosistema Solana. 🚀
