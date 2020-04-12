# findCPweb

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## Table of Contents
- [Install](#install)
- [Run](#Run)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Install
```sh
$ sudo apt-get install redis-server
$ pip3 install -r findCPweb/requirements.txt
```

## Run
```
$ sudo service redis-server start
#   Change secret-key in 'findCPweb/DjangoProject/settings.py'
$ python3 findCPweb/manage.py runserver
```
Go to http://127.0.0.1:8000/app/

## Maintainers

[@alexOarga](https://github.com/alexOarga)

## Contributing

Feel free to dive in! [Open an issue](https://github.com/findCP/findCP/issues/new) or submit PRs.

Standard Readme follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

## License

[MIT](LICENSE) © Alex Oarga
