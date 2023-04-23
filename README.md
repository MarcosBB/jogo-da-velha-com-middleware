# Jogo da velha com middleware
Trata-se de um projeto de jogo da velha usando middleware em que dois jogadores conseguem jogar "online" o famoso jogo da velha.


## Rodando
### Requisitos
1 - instale o python na sua máquina
2 - instale os requisitos do projeto rodando o seguinte comando:
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

```bash
python client/client.py 
```

## Autores
[Marcos Barros](https://github.com/MarcosBB)
[Gdiael Barros](https://github.com/gdiael)
