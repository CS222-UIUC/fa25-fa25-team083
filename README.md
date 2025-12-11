# Space Hub
## FA25 CS222 Team 083



Space Hub is a full stack web application that aims to aggregate NASA data into a single, unified dashboard.  
It provides users with access to various resources and APIs: Astronomy Picture of the Day (APOD), Mars InSight weather data, Near-Earth Objects, and upcoming NASA events.  
The project consists of a React (Vite) frontend, a Flask backend, and a Dockerized deployment environment.


## Features
- APOD viewer with image and the description
- Mars InSight data
- Near Earth Object information
- Countdown timers for launches and events
- A responsive dashboard UI built with React and Tailwind
- REST API backend with caching



##  Requirements
Before running the project, ensure you have:

- Docker Desktop (for Windows/macOS) or Docker Engine (for Linux)
- Git

##  Running the Project With Docker

Clone the repository:
```bash
git clone https://github.com/CS222-UIUC/fa25-fa25-team083.git
cd fa25-fa25-team083
copy .env.example .env
```

Now, from the repository root:
```bash
docker compose up --build
```

And, paste into the local host into your browser of choice:
```
http://localhost:5173/
```

To shut it down:
```bash
CTRL + C
```
and

```bash
docker compose down
```




