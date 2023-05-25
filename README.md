# Leitura e Monitoramento de Dados de Motores de Combustão Interna

## 1. Como usar?

Para usar o programa, intale python e pip em sua máquina e execute o seguinte comando para instalar as dependências do projeto:

```sh
    pip install -r requirements.txt
```

Caso não tenha um dispositivo ELM e um veículo à disposição, é possível utilizar um emulador executando os comandos:

```sh
    python3 -m pip install git+https://github.com/ircama/ELM327-emulator #para instalar
    elm #para executar o emulador
```

Durante a execução ele exibe qual porta está conectada (usando linux, a porta padrão é: "/dev/pts/2")

Execute o script usando o comando:

```sh
    python obd-test.py
```