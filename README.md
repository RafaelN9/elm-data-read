# Leitura e Monitoramento de Dados de Motores de Combustão Interna

## 1. Como usar?

Instale [python](https://www.python.org/downloads/) e [flutter](https://docs.flutter.dev/get-started/install)

Conecte o leitor OBD2 via USB

Para usar o programa, ative a biblioteca python e execute a API:

```sh
    source .venv/bin/activate
    python -m app "$(ls /dev/tty.usb* | grep -E 'serial')" # para MacOS
```

Em seguida execute o aplicativo flutter:

```sh
    cd app
    flutter run
```