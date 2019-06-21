# MEEP MEEP MOBILITY API

Create a virtual environment with pyenv

```
pyenv virtualenv 3.6.5 meep-meep-3.6.5
```

Create a python environment file

```
echo meep-meep-3.6.5 > .python.version
```

Deploy to aws (Configure locally your Serverless with your aws creds)
```
sls deploy
```