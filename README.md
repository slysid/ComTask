Dependencies
------------

Following are the python libraries needed to run this application.

gevent
jinja2



How to install Dependencies
---------------------------

From home directory of the application run following command

[sudo] pip install -r deps/requirements.txt



How to run the script
---------------------

From home directory of the application run the following command

python main.py

The application generates a HTML report in reports/report.html once execution is completed and the path of the file is printed out after execution


Some info on report.html
------------------------

1. Report is generated using Jinja2 template
2. Templete is rendered with values from template.yaml
3. Color coding are used to highlight critial values
4. Language can be set according to locale settings from settings.yaml