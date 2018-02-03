# CS50project
David Griffiths's final project for the Harvard CS50 course. 

> 
> The reporting from the UK's [NHS digital](https://digital.nhs.uk/) team is in depth but these publications are not **interactive** (mostly excel based). My aim is build an application that allows the UK public to explore these data sets dynamically by utilising pythons visualisation libraries.
>

View the [app on heroku](https://nhs-dash-app.herokuapp.com/)


## About

[Dash](https://plot.ly/dash) and [Plotly](https://plot.ly/) were the two key technologies i used to build this application. Other libraries or tools used:

* heroku - to deploy the site
* font awesome - for social media icons on the footer
* bootstrap - for custom css to help render layout on different devices
* Jupyter Notebooks - to do the initall exploration
* pandas - a python library that allows you to transform database


#### 111 Program Tab

3d plot of NHS areas across time and performance of calls answered within 60 seconds.


![Demo2](https://github.com/wisemuffin/CS50project/blob/master/documenation/nhs-111-dash.gif?raw=true)

Time series with geographical dropdown filtering.  

*GIF TBC*

#### Cancer Survival Tab

hover over the bar cancer site to filter the below time series and donought charts. 

![Demo](https://github.com/wisemuffin/CS50project/blob/master/documenation/nhs-cancer-dash.gif?raw=true)

#### Outpatient Activity 2016-17 Tab

*GIF TBC*

## Jupyter Notebooks

I used [Jupyter Notebooks](http://jupyter.org/) and the [Pandas](https://pandas.pydata.org/) library to initially explore data sets.  

[Jupyter Notebooks](http://jupyter.org/) only render static html images on github. To view the jupyter notebooks i recommend pasting the link of the github notebook into [nbviewer](https://nbviewer.jupyter.org/) e.g. https://nbviewer.jupyter.org/github/wisemuffin/CS50project/blob/master/jupyter%20notebooks/NHS_111_Programme.ipynb

However if you want to fully replicate this analysis please see the last section on how to replicate this analysis on your own machine.  



## To replicate this analysis on your machine
* install Conda from [Continuum](https://anaconda.org/anaconda/continuum-docs). This will install python (if you don't already have it) and several scientific packages.
* [clone](https://help.github.com/articles/cloning-a-repository/) this git repository
* create a virtual environment by running 'conda create --name <choose your name of environment> python=3.6' in the command line

* Then [Jupyter Notebooks](http://jupyter.org/) are an excellent way for others to reproduce my analysis

#### Alternatively you can run the dash application by skipping the Juptyer Step and completing the following steps

* Run the app with: $python app.py in the command line
* Visit http:127.0.0.1:8050/ in your web browser (or what ever http site is shown after running the app.py)

## Future Work

```
* set up [environment.yml](https://github.com/czbiohub/singlecell-dash/blob/master/README.md) so others can use
* get more ideas from the [plotly community](https://community.plot.ly/t/show-and-tell-community-thread-tada/7554)
* could add table from https://github.com/jackdbd/dash-earthquakes
* could add some graphs from mapbox
* think about layout for different devices
```
