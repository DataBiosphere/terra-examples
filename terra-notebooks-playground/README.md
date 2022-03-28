
**A workspace for trying out Terra functionality as it evolves**.

**IMPORTANT NOTE FOR USERS NEW TO JUPYTER NOTEBOOKS:**

* Not all warning messages are bad! Often you will run a cell that will return warnings in the output (sometimes these warnings will even be alarmingly color-coded in red or pink). This does not mean that the cell was not successful, and these warnings can often be ignored.


**What's in Terra Notebooks Playground**.

Terra includes multiple tools for interactive computational analysis, including Jupyter, a web-based application that supports code in a variety of languages (R and Python, among others), and streamlines interaction with cloud-based resources. This workspace contains a set of Jupyter Notebooks that allow users to play with this functionality, and the notebooks are organized into two categories: **R** and **Python**.
 
The notebooks available in this workspace are listed below. If you are entirely new to Jupyter and are not sure where to start, try the first two notebooks at the top of each list (italics)!

* **Python**
    * *Py3 - How to read data from BigQuery.ipynb*
    * Py3 - How to use a cohort.ipynb
    * Py3 - How to use Facets for interactive visualization of data.ipynb
    * Py3 - How to load data to BigQuery.ipynb
    * Py3 - How to store analysis results in BigQuery and Cloud Storage.ipynb
    * Py3 - How to use IGV in a Terra notebook.ipynb
* **R**
    * *R - How to read data from BigQuery.ipynb*
    * R - How to retrieve a cohort.ipynb
    * R - Analysis example for exploring power law distributions.ipynb
    * R - Plotting example for Boston 311 data.ipynb
    * R - How to emit markdown from code cells.ipynb
    * R - How to save images and tables to files.ipynb
    * R - How to store revisions and reports.ipynb
    * R - How to load data to BigQuery.ipynb
    * R - How to pull in reusable code from source control.ipynb
    * R - How to save and load R objects from the workspace bucket.ipynb
* **Notebook-based tools**
    * Create HTML snapshots of notebooks.ipynb

PLEASE NOTE:

* This is pragmatic training material, rather than polished presentation material. 
* This workspace is shared with all Terra users. To understand public access policies in Terra, check out this article on [Terra Access Policy](https://broadinstitute.zendesk.com/hc/en-us/articles/360024617851-Access-Policy)
* Only public data is used in these example notebooks.
* Have questions, comments, feedback? You can file a [GitHub issue](https://github.com/DataBiosphere/notebooks/issues) or click “Contact Us” in the main menu on the left to submit feedback, or go to our [forum](https://broadinstitute.zendesk.com/hc/en-us/community/topics/360000500432-General-Discussion) by clicking “Community Discussion”, also in the left-hand menu
* Interested in contributing new notebooks or code improvements for this workspace? You can send a [pull request](https://github.com/DataBiosphere/notebooks/pulls) or submit a [feature request](https://broadinstitute.zendesk.com/hc/en-us/community/topics/360000500452-Feature-Requests) by clicking the “Request a feature” button  in the main menu on the left
* Don’t forget to come back and check for updates to this workspace!

The notebooks here often use 1000 Genomes sample metadata from either of:

* BigQuery table [*bigquery-public-data:human_genome_variants.1000_genomes_sample_info*](https://bigquery.cloud.google.com/table/bigquery-public-data:human_genome_variants.1000_genomes_sample_info?pli=1)
* Cloud Storage file [*gs://genomics-public-data/1000-genomes/other/sample_info/sample_info.csv*](https://console.cloud.google.com/storage/browser/genomics-public-data/1000-genomes/other/sample_info/)

## Appendix

### Terra documentation and support

Please also see [Terra documentation](https://broadinstitute.zendesk.com/hc/en-us). For assistance, reach out to the support team by following the “Contact Us” link in the Terra menu.

You can also interact with the Terra team, as well as other fellow users, by clicking “Community Discussion” in the Terra menu to visit our [forum](https://broadinstitute.zendesk.com/hc/en-us/community/topics/360000500432-General-Discussion).

### R resources

For data wrangling, visualization, and general analysis:

* [R for Data Science](http://r4ds.had.co.nz/) teaches how to wrangle and visualize data
* [Cheat Sheets](https://www.rstudio.com/resources/cheatsheets/) for commonly used R packages. Of particular note:
    * [Data Transformation Cheat Sheet [dplyr]](https://www.rstudio.com/resources/cheatsheets/#dplyr)
    * [Work with Strings Cheat Sheet [stringr]](https://github.com/rstudio/cheatsheets/raw/master/strings.pdf)
    * [Dates and Times Cheat Sheet [lubridate]](https://github.com/rstudio/cheatsheets/raw/master/lubridate.pdf)
    * [Apply Functions Cheat Sheet [purrr]](https://github.com/rstudio/cheatsheets/raw/master/purrr.pdf)

For domain-specific analysis packages you might consider using, see 

* [CRAN Task View: Survival Analysis](https://cran.r-project.org/web/views/Survival.html)
* [CRAN Task View: Time Series Analysis](https://cran.r-project.org/web/views/TimeSeries.html)

If you are developing R packages:

* [The tidyverse style guide](https://style.tidyverse.org/)
* [Advanced R](http://adv-r.had.co.nz/)
* [R packages](http://r-pkgs.had.co.nz/)
* [RStudio, Git and GitHub](http://r-pkgs.had.co.nz/git.html)

### Plotting Resources

* Great [talk](https://youtu.be/IzXxTeQhdO0) on data visualization, interesting points on:
    * use of 'small multiples': same data plotted multiple ways
    * using color intentionally
    * how to decide how much time and energy to put into your plots
* [One chapter]( http://r4ds.had.co.nz/data-visualisation.html) on ggplot2
* [ggplot2 cheatsheet](https://www.rstudio.com/resources/cheatsheets/#ggplot2) 
* [R Graph Gallery](https://www.r-graph-gallery.com/) inspiration and help with R Graphics
* [This is the most important tip of all ;-)](https://flowingdata.com/2012/06/07/always-label-your-axes/)

---

### Contact information

In addition to Terra support, you can also reach us on GitHub by [filing an issue](https://github.com/DataBiosphere/notebooks/issues).

### License
Please see the BSD-3-Clause [license on GitHub](https://github.com/DataBiosphere/notebooks/blob/master/LICENSE.md)

### Workspace Change Log
Please see the [pull request history](https://github.com/DataBiosphere/notebooks/pulls?q=is%3Apr+) on GitHub.
