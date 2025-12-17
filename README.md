# Space Hub
## FA25 CS222 Team 083


## Overview
- Space Hub is a full stack web application that aims to aggregate NASA data into a single, unified dashboard.  
- It provides users with access to various resources and APIs: Astronomy Picture of the Day (APOD), Mars InSight weather data, Near-Earth Objects, and upcoming NASA events.  
- The project consists of a React (Vite) frontend, a Flask backend, and a Dockerized deployment environment.
- Our motivation for this project was to simplify and ease the access of infromation from NASA and other Space related APIs.
- As such, users can find relevant, up-to-date space data and information all in one application.

![Example of Space Hub Dashboard](https://github.com/CS222-UIUC/fa25-fa25-team083/blob/main/dashboard.PNG)

---

## Features
- APOD viewer with image and description
- Mars InSight data
- Near Earth Object information
- Countdown timers for launches and events
- A responsive dashboard UI built with React and Tailwind
- REST API backend with caching

## Architecture
### Frontend
- Displays all of the data collectively to the user
- Handles all UI interactions
- React, Vite, Tailwind CSS
- Makes HTTP requests to the backend Flask API
- Worked on by the Frontend Team
  
### Backend
- Directly fetches data from NASA APIs
- Processes the responses
- Python, Flask
- Passes data from external APIs to the frontend
- Worked on by the Backend Team

### APIs
- Provide the real-time and up-to-date space and astronomy data
- APIs Used: NASA's APOD, Mars InSight, Near-Earth Objects, launch/event data, lunar data
- Queried and parsed by the backend
- Worked on by the Backend Team

### Deployment
- Allows for the project/app to be reproducible across systems
- Docker/Docker Compose runs frontend and backend together in isolated containers
- Worked on by the Deployment Team

---

##  Requirements
Before running the project, ensure you have:

- Docker Desktop (for Windows/macOS) or Docker Engine (for Linux)
- Git

---
## Important Note Before Running

This application uses a demo NASA API key.
Because the demo key is rate limited, users may encounter request limits during extended use.
If you wish to avoid this, users are encouraged to register for a free NASA API key at: [https://api.nasa.gov/](https://api.nasa.gov/)

#### You must then access the /.env file and change the NASA_API_KEY to your key.

---

##  Running the Project With Docker

Clone the repository:
```bash
git clone https://github.com/CS222-UIUC/fa25-fa25-team083.git
cd fa25-fa25-team083
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


---
### Team Members and Roles

Frontend Development
- Kayetan Jarzabek
- 
Backend Development
- Kayetan Jarzabek
- Ashrita Jakkam

Deployment
- Kayetan Jarzabek





