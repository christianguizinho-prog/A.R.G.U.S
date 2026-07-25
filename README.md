# A.R.G.U.S.

Monitoramento local de CPU, memória, disco, rede e alertas.

## Segurança e execução

1. Crie o ambiente virtual e instale as dependências:
   `python -m pip install -r requirements-dev.txt`
2. Execute a interface: `python main.py`.
3. Na primeira abertura, registre um usuário com senha de no mínimo 12 caracteres.
4. Execute testes: `python -m pytest -q`.

A API é local por padrão: `python api_server.py`. Ela escuta somente em
`127.0.0.1` e exige o cabeçalho `X-API-Key`. O token é criado localmente em
`database/api_token.txt` (ou pode ser definido por `ARGUS_API_TOKEN`) e nunca
deve ser compartilhado ou versionado.

A localização por IP é consultada no máximo a cada cinco minutos. A métrica de
GPU só é exibida quando há suporte NVML; o sistema não simula uso de GPU.
