# Terra notebooks playground

A workspace for trying out Terra functionality as it evolves.

---
## What's in this workspace?

Terra includes multiple tools for interactive computational analysis, including Jupyter, a web-based application that supports code in a variety of languages (R and Python, among others), and streamlines interaction with cloud-based resources. This workspace contains a set of Jupyter Notebooks that allow users to play with this functionality.
 
The notebooks available in this workspace are listed below. If you are entirely new to Jupyter and are not sure where to start, first see the [Notebooks Quickstart Guide](https://support.terra.bio/hc/en-us/articles/360059009571-Notebooks-Quickstart-Guide).

* **Python**
    * `py3__how_to_read_data_from_bigquery.ipynb`
    * `py3__how_to_load_data_to_bigquery.ipynb`
    * `py3__how_to_read_data_from_cloud_storage.ipynb`
    * `py3__how_to_store_analysis_results_in_bigquery_and_cloud_storage.ipynb`
    * `py3__how_to_use_a_cohort.ipynb`
    * `py3__how_to_use_facets_for_interactive_visualization_of_data.ipynb`
    * `py3__how_to_use_igv_in_a_terra_notebook.ipynb`
* **R**
    * `r__how_to_read_data_from_bigquery.ipynb`
    * `r__how_to_load_data_to_bigquery.ipynb`
    * `r__how_to_save_and_load_r_objects_from_the_workspace_bucket.ipynb`
    * `r__how_to_save_images_and_tables_to_files.ipynb`
    * `r__how_to_use_a_cohort.ipynb`
    * `r__how_to_emit_markdown_from_code_cells.ipynb`
    * `r__how_to_pull_in_reusable_code_from_source_control.ipynb`
    * `r__how_to_store_revisions_and_reports.ipynb`
    * `r__analysis_example_for_exploring_power_law_distributions.ipynb`
    * `r__plotting_example_for_boston_311_data.ipynb`
* **Notebook-based tools**
    * `create_html_snapshots_of_notebooks.ipynb`
    * `hail__how_to_run_a_notebook_in_the_background.ipynb`

Details
* Only public data is used in these example notebooks. The notebooks here often use 1000 Genomes sample metadata from either of:
    * BigQuery table [`bigquery-public-data:human_genome_variants.1000_genomes_sample_info`](https://console.cloud.google.com/bigquery?ws=!1m5!1m4!4m3!1sbigquery-public-data!2shuman_genome_variants!3s1000_genomes_sample_info)
    * Cloud Storage file [`gs://genomics-public-data/1000-genomes/other/sample_info/sample_info.csv`](https://console.cloud.google.com/storage/browser/genomics-public-data/1000-genomes/other/sample_info/)
* Tip: Not all warning messages are bad! Often you will run a cell that will return warnings in the output (sometimes these warnings will even be alarmingly color-coded in red or pink). This does not mean that the cell was not successful, and these warnings can often be ignored.

Next steps:
* **Have questions, comments, feedback?** You can file a [GitHub issue](https://github.com/DataBiosphere/terra-examples/issues) or click “Contact Us” in the main menu on the left to submit feedback, or go to our [forum](https://broadinstitute.zendesk.com/hc/en-us/community/topics/360000500432-General-Discussion) by clicking “Community Discussion”, also in the left-hand menu
* **Interested in contributing new notebooks or code improvements for this workspace?** You can send a [pull request](https://github.com/DataBiosphere/terra-examples/pulls) or submit a [feature request](https://broadinstitute.zendesk.com/hc/en-us/community/topics/360000500452-Feature-Requests) by clicking the “Request a feature” button  in the main menu on the left
* **Don’t forget to come back and check for updates to this workspace!**

## Appendix

### Terra documentation and support

Please also see [Terra documentation](https://broadinstitute.zendesk.com/hc/en-us). For assistance, reach out to the support team by following the “Contact Us” link in the Terra menu.

You can also interact with the Terra team, as well as other fellow users, by clicking “Community Discussion” in the Terra menu to visit our [forum](https://broadinstitute.zendesk.com/hc/en-us/community/topics/360000500432-General-Discussion).

### R resources

For data wrangling, visualization, and general analysis:

* [R for Data Science](http://r4ds.had.co.nz/) teaches how to wrangle and visualize data
* [Cheat Sheets](https://www.rstudio.com/resources/cheatsheets/) for commonly used R packages. Of particular note:
    * [Data Transformation Cheat Sheet [dplyr]](https://raw.githubusercontent.com/rstudio/cheatsheets/main/data-transformation.pdf)
    * [Work with Strings Cheat Sheet [stringr]](https://raw.githubusercontent.com/rstudio/cheatsheets/main/strings.pdf)
    * [Dates and Times Cheat Sheet [lubridate]](https://raw.githubusercontent.com/rstudio/cheatsheets/main/lubridate.pdf)
    * [Apply Functions Cheat Sheet [purrr]](https://raw.githubusercontent.com/rstudio/cheatsheets/main/purrr.pdf)

For domain-specific analysis packages you might consider using, see 

* [CRAN Task View: Survival Analysis](https://cran.r-project.org/web/views/Survival.html)
* [CRAN Task View: Time Series Analysis](https://cran.r-project.org/web/views/TimeSeries.html)

If you are developing R packages:

* [The tidyverse style guide](https://style.tidyverse.org/)
* [Advanced R](http://adv-r.had.co.nz/)
* [R packages](http://r-pkgs.had.co.nz/)
* [RStudio, Git and GitHub](https://support.rstudio.com/hc/en-us/articles/200532077-Version-Control-with-Git-and-SVN)

### Plotting Resources

* Great [talk](https://youtu.be/IzXxTeQhdO0) on data visualization, interesting points on:
    * use of 'small multiples': same data plotted multiple ways
    * using color intentionally
    * how to decide how much time and energy to put into your plots
* [One chapter]( http://r4ds.had.co.nz/data-visualisation.html) on ggplot2
* [ggplot2 cheatsheet](https://raw.githubusercontent.com/rstudio/cheatsheets/main/data-visualization.pdf) 
* [R Graph Gallery](https://www.r-graph-gallery.com/) inspiration and help with R Graphics
* [This is the most important tip of all ;-)](https://flowingdata.com/2012/06/07/always-label-your-axes/)

---

### Contact information

In addition to Terra support, you can also reach us on GitHub by [filing an issue](https://github.com/DataBiosphere/terra-examples/issues).

### License
Please see the BSD-3-Clause [license on GitHub](https://github.com/DataBiosphere/terra-examples/blob/main/LICENSE.md)

### Workspace Change Log
Please see the [pull request history](https://github.com/DataBiosphere/terra-examples/pulls?q=is%3Apr+) on GitHub.
