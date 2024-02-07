 # Table of content:
 - [1. Introduction](#introduction)
 - [2. Installation](#installation)
 - [3. Login to Copernicus](#login_to_copernicus)
 - [4. Running](#running)


<a id="introduction"></a>
# 1. Introduction
This is a wrapper to help you download data from [Copernicus servers](https://marine.copernicus.eu/register-copernicus-marine-service?mtm_campaign=Copernicus-Souscription&mtm_medium=cpc&mtm_source=google&mtm_content=text&mtm_cid=145762311002&mtm_kwd=copernicus%20marine%20data&gad_source=1&gclid=CjwKCAiAnL-sBhBnEiwAJRGigvyODuGJ__Aa1pjKNB8H7VvH_lrn3Fu-CJdZO1T_g-ChP95GC8fxFRoCLZsQAvD_BwE) via a configuration file, eliminating therefore the
need to deal with programming. It has been developed in Python 3.9 and makes calls to the recently released [Copernicus Marine Toolbox's python API](https://help.marine.copernicus.eu/en/collections/5821001-python-library-api) - as per December 2023.

The main advantages over the [toolbox's console client](https://help.marine.copernicus.eu/en/collections/5820990-command-line-interface-cli) are as follows:

1. The input data is processed by single unique dates, meaning that rows which dates are the same are processed together 
   by calculating the widest area that embeds all given coordinates for that day. This avoids reducing the number of calls
   or the generation of massive files should the whole set be requested at once.
2. Only one single csv file is generated.
3. Although the data fetched is by area and date, the script will find the point in the downloaded dataset closest to the coordinates 
   given in each row of the input file, meaning that the final generated csv file has got the same number of rows as the input file.
4. All Individual and original downloaded files are kept intact - **.nc format** - so that they can be post-processed in whichever way 
   you consider appropriate, should you need to do so in the forthcoming future.

This wrapper uses solely the [subset](https://help.marine.copernicus.eu/en/articles/8283072-copernicus-marine-toolbox-api-subset) functionality of the Copernicus Marine Toolbox's Python API.

<a id="installation"></a>
# 2. Installation

First, install **Python >=3.9 and < 3.12** as required by Copernicus Marine Toolbox and **pip**.  To do 
so download the Python version of your choice from https://www.python.org/downloads/ and then follow the instructions 
on https://docs.python.org/3/using/index.html. Details for Windows, Mac and *nix users are provided in the appropriate sections.

Second, download the source code from Github either by downloading the zip directly from the web on https://github.com/d2gex/copernicus-subset-wrapper.git as
shown in the figure below ...

<img src="images/github_zip_dowload.png">

... Or just git-cloning to your preferred location, ensuring that the destination folder is empty:

```bash
   cd <<your_source_folder>>
   git clone https://github.com/d2gex/copernicus-subset-wrapper.git .
```

Third, install the project dependencies. If you do not want to install them system-wide, which is highly 
recommended not do so, you can create a virtual environment as described on [Python Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html).
A quick tutorial for the virtual environment creation is shown below:

```bash
   python3 -m venv <<your_virtualenv_folder>>
   source /path/to/your_virtualenv_folder/bin/activate
```

Lastly, all that is left now is to install all requirements at once as follows:

```bash
   pip install -r /path/to/your_source_folder/requirements.txt
```
The file **requirements.txt** contains all libraries that are necessary for this wrapper to run.


<a id="login_to_copernicus"></a>
# 3. Loging to Copernicus
If you have not yet registered with Copernicus you need first to do so [here](https://data.marine.copernicus.eu/register).
Then you need to run the `login` function from Copernicus API one-off for your credentials to be generated. Subsequent calls
to the wrapper will know where you credentials are stored and pick them as needed. To call login you need to run the following
on the console:

```bash
  copernicus-marine login
```
You will be asked for the username and password you used earlier on in the registration process. Upon providing it, a message
saying that the credentials have been generated and the location where they are should be prompted to you. You are now
ready to use the wrapper without worrying in the future about credentials or whatsoever.


<a id="running"></a>
# 4. Running

## 4.1 Configure your *setup.toml* file

The `setup.toml` file is the configuration file used by the wrapper and contains information about the products and
variables you are trying to download. It is placed within *<<your_source_folder>>* and its options have been explained
within the file itself and should be self-explanatory.

#### setup.toml
```yaml
input_filename = "api_parameters.csv" # name of the file holding the input parameters
output_filename = "result.nc" # suffix added to the name of each individual file fetched per input row
dataset_id = "cmems_mod_glo_phy_my_0.083deg_P1M-m" # data set identifier
variables = ["thetao", "zos"] # variables wanting to be fetched
years = [2012, 2020] #  date interval of interest. One single year can be defined as [2012]
# distance method used to calculate the nearest point.
# See alternatives on https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
distance = "euclidean"
# [days, hours, minutes, seconds] time added to each start_time - per row - in days, hours, minutes and seconds
time_offset = [0, 23, 59, 59]
start_mode = 0  # 0 start afresh, 1 resume from given years interval and 2 read only from disk
```

## 4.2 Ensure input file is in the correct format
The wrapper will read a csv file within `data` folder in '<<your_source_folder>>' provided by the variable 
`input_filename` in your configuration file. An example is shown below:

#### <<your_apir_parameters_filename>>.csv
<img src="images/api_parameters_input_sample.png">

In a nutshell, columns `lat`, `lon`, `time` and `depth` must be named as such and `time` must be in `%d/%m/%Y %H:%M`. 
The coordinate system is **WGS 84 EPSG: 4326**. There must be a column in the spreadsheet identifying each row uniquely,
although its name is down to you. In the example above it is called `ID_Gil`.

## 4.3 Run the wrapper

```bash
   cd your_source_folder
   python -m src.main
```

## 4.4 Look for the results

After the data has been downloaded look for the resulting csv file in  '<<your_source_folder>>/**data**/<<dataset_identifier>>/**csv**/<<dataset_identifier>>.csv'.
The wrapper will also place each downloaded `*.nc` files in '<<your_source_folder>>/**data**/<<dataset_identifier>>/**nc**/'.


