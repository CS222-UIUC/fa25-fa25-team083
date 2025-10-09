The development branch has been set-up. There are two ways from what I gathered you can code. 

## 1) Using GitHub's Codespace
You go to: branches -> develop -> Code -> Codespaces

## 2) Local Machine (Windows)
I was only able to set this up using my Windows laptop. Sorry if you are using Linux or Mac
##This is assuming you have Docker Desktop running, Git, and VS Code with the Dev Containers extension

Make a folder somewhere on your machine and remember the path to your folder.

Open a new window of VS Code and open a terminal window (Terminal -> New Terminal) or (Ctrl + Shift + `)
```powershell
cd "Path to your project folder on your machine"

git clone https://github.com/CS222-UIUC/fa25-fa25-team083.git
cd fa25-fa25-team083

git checkout develop

Copy-Item .env.example .env

docker compose up -d

docker compose ps
Invoke-WebRequest -UseBasicParsing http://localhost:8001/health | Select-Object -ExpandProperty Content

code .
```

### And you should now be able to work in the develop branch. We can go and do seperate branches or all work in develop. If you need help setting this up then let me know (Kayetan J.). I tried my best at running this so it can work on everyone's machine so hopefully this works.

If you want to develop in your own branch, such as a feature, then I'm assuming you can do this.

```powershell
git checkout develop
git pull --ff-only
git checkout -b feat/"PUT YOUR FEATURE NAME WITHOUT THE QUOTES"
```

Now you can add a new file python file or do whatever prior commiting and pushing.
Assuming you are doing a backend file like I did here:

```powershell
git add backend\hello.py
git commit -m "feat: add hello world script" #<--- This stays in quotes
git push -u origin feat/"PUT YOUR FEATURE NAME WITHOUT THE QUOTES LIKE BEFORE"
```

And now you should be able to see a pull request at the top of the screen under: https://github.com/CS222-UIUC/fa25-fa25-team083/tree/develop





[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/19BwrNgF)

