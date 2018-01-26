# CS50project
Daves final project for the Harvard CS50 course

> 
> The reporting from the UK's [NHS digital](https://digital.nhs.uk/) team is in depth but these publications are not **interactive** (mostly excel based). My aim is build an application that allows the UK public to explore these data sets with some of pythons visualisation libraries.
>
  

## Dash Application

[Dash](https://plot.ly/dash) and [Plotly](https://plot.ly/) were the two key technologies i used to build this application.

#### Outpatient Activity 2016-17


#### 111 Program

#### Cancer Survival

## Jupyter Notebooks

I used [Jupyter Notebooks](http://jupyter.org/) and the [Pandas](https://pandas.pydata.org/) library to initially explore data sets.  

[Jupyter Notebooks](http://jupyter.org/) only render static html images on github. To view the jupyter notebooks i recommend pasting the link of the github notebook into [nbviewer](https://nbviewer.jupyter.org/) e.g. https://github.com/wisemuffin/CS50project/blob/master/jupyter%20notebooks/NHS_111_Programme.ipynb.

However if you want to fully replicate this analysis please see the last section on how to replicate this analysis on your own machine.  



## To replicate this analysis on your machine
* install Conda from [Continuum](https://anaconda.org/anaconda/continuum-docs). This will install python (if you don't already have it) and several scientific packages.
* [clone](https://help.github.com/articles/cloning-a-repository/) this git repository
* create a virtual environment by running 'conda create --name <choose your name of environment> python=3.6' in the command line

* Then [Jupyter Notebooks](http://jupyter.org/) are an excellent way for others to reproduce my analysis

#### Alternatively you can run the dash application by skipping the Jupyer Step and completing the following steps

* Run the app with: $python app.py in the command line
* Visit http:127.0.0.1:8050/ in your web browser (or what ever http site is shown after running the app.py)
