# CS50project
Daves final project for the Harvard CS50 course

> 
> The reporting from the UK's [NHS digital](https://digital.nhs.uk/) team is in depth but these publications are not **interactive** (mostly excel based). My aim is build an > > application that allows the UK public to explore these data sets with some of pythons visualisation libraries.
>





## Tool used to build this application and interactive notebooks:
I used [Jupyter Notebooks](http://jupyter.org/) and the [Pandas](https://pandas.pydata.org/) library to initially explore data sets.

The visualisations were built using a python library called [Plotly](https://plot.ly/).

[Dash](https://plot.ly/dash) then abstracts away all of the technologies (java script) and protocols required to build an interactive web-based application and is a simple and effective way to bind a user interface around your Python code. This allowed me to focus on the python language and its data exploration and visualisation libraries.



## To replicate this analysis on your machine:
* install Conda from [Continuum](https://anaconda.org/anaconda/continuum-docs). This will install python (if you don't already have it) and several scientific packages.
* [clone](https://help.github.com/articles/cloning-a-repository/) this git repository
* create a virtual environment by running 'conda create --name <choose your name of environment> python=3.6' in the command line

* Then [Jupyter Notebooks](http://jupyter.org/) are an excellent way for others to reproduce my analysis

#### Alternatively you can run the dash application by skipping the Jupyer Step and completing the following steps:

* Run the app with: $python app.py in the command line
* Visit http:127.0.0.1:8050/ in your web browser (or what ever http site is shown after running the app.py)
