pylint --load-plugins pylint_django --django-settings-module=config.settings --ignore=__pycache__ config core > pylint_res.txt
type pylint_res.txt