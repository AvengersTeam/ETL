# ETL
Repositorio con el código para realizar la migración de los datos a formato RDF

Tutorial Instalación
--------------------

* Instalar [Python2.7](https://www.python.org/download/releases/2.7/)
* Instalar la biblioteca [lxml](http://lxml.de/installation.html)
```bash
> pip install lxml
```

* Clonar el repositorio
```bash
> git clone https://github.com/AvengersTeam/ETL.git
```

Tutorial Ejecución
------------------

* Ejecutar ETL correspondiente
```bash
> python etl_[tipo].py
```
###### Nota: algunos etl requieren que se haya ejecutado al menos alguna vez uno de los otros etl. Utilice `run.py` para evitar problemas

* Si desea correr todos a la vez ejecutar `run.py`
```bash
> python run.py
```
