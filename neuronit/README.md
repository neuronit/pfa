# neuronit

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`), and pip.

```
## INSTALLATION OF THE DEPENDENCIES
pip install -r requirements.txt
or
python -m pip install -r requirements.txt


## INITIALISATION OF THE DATABASE
./manage.py migrate

## LOAD DATA INTO THE DB
./manage.py loaddata sites
./manage.py loaddata base
./manage.py loaddata game
./manage.py loaddata types
./manage.py loaddata neuronit
./manage.py loaddata about-us
./manage.py loaddata leaderboard

## RUN THE SERVER
./manage.py runserver
```


## observation multiplicator ~100-1000
## passive_reward ~ +-1 recompense tant qu'on est pas mort
## defeat_punishement ~10
## network size [x,x,x,x] ( nb de couches)
## pro_level_exists = 1 (checkbox)
## 