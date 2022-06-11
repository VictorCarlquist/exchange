![example workflow](https://github.com/VictorCarlquist/exchange/actions/workflows/django.yml/badge.svg)

# Exchange $

Desafio BR MED
---

Link: [https://exchange-brl.herokuapp.com/](https://exchange-brl.herokuapp.com/)

Este projeto é um site que mostra a cotação do dolar vs real, euro e iene(JPY), sendo apenas uma demonstração.

Os dados são fornecidos pela API  [vatcomply](https://www.vatcomply.com/documentation).

- Backend: Foi utilizado o framework django.
  - Como o vatcomply carrega apenas a cotação de um dia por cada requisição, eu criei uma rotina para enviar múltiplas requições em paralelo veja o arquivo [money/exchange/api_rates.py](https://github.com/VictorCarlquist/exchange/blob/main/money/exchange/api_rates.py)
  - Seguindo os principios do Clean Architecture, criei o arquivo [money/exchange/usecase.py](https://github.com/VictorCarlquist/exchange/blob/main/money/exchange/usecase.py), servindo como uma camada entre o endpoint e o banco de dados, armazenando as regras de negócio.
  - Adicionei alguns testes no arquivo [test.py](https://github.com/VictorCarlquist/exchange/blob/main/money/exchange/tests.py)
  - Arquivo com as Views [views.py](https://github.com/VictorCarlquist/exchange/blob/main/money/exchange/views.py)
  - Arquivo com o código HTML [index.html](https://github.com/VictorCarlquist/exchange/blob/main/money/exchange/templates/exchange/index.html) e [base.html](https://github.com/VictorCarlquist/exchange/blob/main/money/exchange/templates/exchange/base.html)

- Frontend: Foi utilizado [highcharts](https://www.highcharts.com/), [bootstrap](https://getbootstrap.com/) e [sweetalert](https://sweetalert.js.org/guides/).
