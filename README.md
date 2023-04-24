# Jogo da velha com middleware
Trata-se de um projeto de jogo da velha usando middleware em que dois jogadores conseguem jogar "online" o famoso jogo da velha.
O projeto usa a tecnologia `RPC` com a biblioteca `pyro4` do python para gerar seu middleware. Foram criados 2 tipos de clientes: Um cliente com interface gráfica usando a biblioteca `pygame` e um cliente pelo terminal.

![image](https://user-images.githubusercontent.com/50207805/233893489-0825745e-1de6-49f6-9870-7d636d7fa563.png)



## Rodando
### Requisitos
1. é necessário um SO Linux para rodar a aplicação
2. instale a versão `3.10.8` do python na sua máquina para evitar incompatibilidades
3. instale os requisitos do projeto rodando o seguinte comando:
```bash
pip install -r requirements.txt
```

### Rodando o servidor
#### Servidor de nomes
Em um terminal você deve rodar o servidor de nomes do pyro4. Rode o seguinte comando:
```bash
pyro4-ns
```

#### Servidor
Abra outro terminal na pasta `server` e rode o servidor do middleware com o seguinte comando:

```bash
python server.py 
```

#### Cliente
Para cada novo jogador você deve abrir o client em um terminal diferente, caso esteja rodando na mesma máquina. Rode o seguinte comando para abrir:

Cliente de interfáce gráfica:
```bash
python client/gui.py
```

Cliente de terminal:
```bash
python client/client.py 
```

## Autores
- [Marcos Barros](https://github.com/MarcosBB)
- [Gdiael Barros](https://github.com/gdiael)
