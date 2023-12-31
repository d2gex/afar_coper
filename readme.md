 **Table of content:**
 - [Introduction](#introduction)
 - [Installation](#installation)
 - [Configuration](#configuration)
 - [Execution](#execution)

<a id="introduction"></a>
# Introduction
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
# Installation

<a id="configuration"></a>
# Configuration

<a id="execution"></a>
# Execution

