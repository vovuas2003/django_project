pylint --load-plugins pylint_django --django-settings-module=config.settings --disable=C0114,C0115 --ignore=__pycache__ config core > pylint_res.txt
type pylint_res.txt