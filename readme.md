 # Table of content:
 - [Introduction](#introduction)
 - [Installation](#installation)
 - [Quickstart](#quickstart)
 - [Configuration](#configuration)
 - [Execution](#execution)

<a id="introduction"></a>
# 1. Introduction
This is a wrapper to help you download data from [Copernicus servers](https://marine.copernicus.eu/register-copernicus-marine-service?mtm_campaign=Copernicus-Souscription&mtm_medium=cpc&mtm_source=google&mtm_content=text&mtm_cid=145762311002&mtm_kwd=copernicus%20marine%20data&gad_source=1&gclid=CjwKCAiAnL-sBhBnEiwAJRGigvyODuGJ__Aa1pjKNB8H7VvH_lrn3Fu-CJdZO1T_g-ChP95GC8fxFRoCLZsQAvD_BwE) via a configuration file, eliminating therefore the
need to deal with programming. It has been developed in Python 3.9 and makes calls to the recently released [Copernicus Marine Toolbox's python API](https://help.marine.copernicus.eu/en/collections/5821001-python-library-api) - as per December 2023.

The main advantages over the [toolbox's console client](https://help.marine.copernicus.eu/en/collections/5820990-command-line-interface-cli) are as follows:

1. The inputted data is processed by rows, fetching each row individually to avoid having to deal with massive files.
2. The downloaded data is all amalgamated together and converted to csv.
3. Although the data fetched is by area, the script will find the point in the downloaded area nearest to the that requested, meaning that
   the final downloaded file has got the same number of rows as the inputted file.
4. Original individual fetched files are kept intact - **.nc format** - so that they can be post-processed in whichever way you consider appropriate, should you need to do so in the forthcoming future.

This wrapper uses solely the `subset` functionality of the Copernicus Marine Toolbox's Python API.

<a id="installation"></a>
# 2. Installation

First you need to install **Python >=3.9 and < 3.12** as required by Copernicus Marine Toolbox. You will also need to
install **pip**. You need to download the version of your choice from https://www.python.org/downloads/ and then follow the instructions on https://docs.python.org/3/using/index.html.
Details for Windows, Mac and *nix users are provided in the appropriate sections.

Second you need to download the source code from Github either by downloading  the zip directly from the web on https://github.com/d2gex/copernicus-subset-wrapper.git as
shown in the figure below ...

<img src="images/github_zip_dowload.png">

... Or just git-cloning to your preferred location, ensuring that the destination folder is empty:

```
   cd <<your_source_folder>>
   git clone https://github.com/d2gex/copernicus-subset-wrapper.git .
```

Third you need to install the dependencies. If you do not want to install them system-wide which is highly recommended not do so, you
can create a virtual environment as described on [Python Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html).
A quick tutorial for virtual environment creations is shown below:

```
   python3 -m venv <<your_virtualenv_folder>>
   source /path/to/your_virtualenv_folder/bin/activate
```

Lastly, all that is left now is to install all requirements at once as follows:

```
   pip install -r /path/to/your_source_folder/requirements.txt
```
The file **requirements.txt** contain all libraries that are necessary for this wrapper to run.


<a id="quickstart"></a>
# 3. Quickstart

<a id="configuration"></a>
# 4. Configuration

<a id="execution"></a>
# 5. Execution

