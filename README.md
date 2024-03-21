# Polygon Wars
Projeto final para a disciplina de Introdução à Programação do Curso de Ciências de Computação do CIn - UFPE.

## Grupo
- Josias Netto (jhcn)
- Samuel (slgb)
- Fábio Papais (flfp)
- Gustavo Macena (gmp5)
- Felipe Maran Alves (fma3)
- Marx Andrey (malpf)


## Arquitetura do projeto
O código tem como ponto de partida o módulo menu.py, que é responsável por chamar o módulo principal chamado main.py, onde está o loop principal do jogo, que também chama o arquivo gameover.py, caso o jogador perca. Dentro de main.py, estão as declarações e importações principais do jogo, assim como a criação dos principais objetos. Todos os objetos, incluindo o player, inimigos, e botões, estão definidos e separados dentro do módulo objects.py e são importados e instanciados durante o jogo. 
No loop principal, além da criação dos indicadores para o usuário, também estão definidas funções que controlam o comportamento e andamento do jogo. Essas funções são chamadas "strategies", e estão isoladas dentro do módulo strategies.py. Nele, estão definidas ferramentas que permitem criar padrões de spawn, movimentação e criação de inimigos do jogo, nos mais diferentes formatos. No loop principal, usamos estas funções, junto de outros parâmetros como contadores de tempo, para criar padrões de ataques contra o inimigo ao decorrer do jogo. Além disso, a main controla todo a lógica de colisões entre sprites de diferentes tipos, assim como a atualização de valores como hp, attackspeed e outros parâmetros importantes para a lógica do jogador.


Ferramentas utilizadas
O projeto foi programado em Python, e fez uso da biblioteca externa Pygame, a qual permite com que o programa rode de forma constante e, dessa forma, permite com que o jogo funcione. Além disso, também foram utilizadas algumas bibliotecas como random, a fim de implementar elementos de aleatoriedade no que inimigos podem deixar pra trás ao morrerem.


## Divisão de trabalho
Criação dos objetos principais, coletáveis, colisões –> Felipe e Fábio
Criação dos sprites e da interface –>  Samuel e Gustavo 
Sons –> Marx e Josias
Criação do relatório, feedback –> Marx
Posições relativas ao mouse e orientação ao player  –> Josias e Samuel


## Conceitos apresentados na disciplina e utilizados no projeto
Como o framework influencia a lógica do desenvolvimento e da implementação de conceitos, a modularização como um todo foi muito útil, herança na criação de multiclasses / heranças múltiplas, além de muitos conceitos básicos que foram essenciais no desenvolvimento do projeto como um todo, com assuntos como tuplas, listas, normalização de vetores, entre muitos outros.


## Desafios, erros, e lições aprendidas
### - Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele? 
Não ter começado features além da gameplay antes (menu, gráficos, sons, etc). Lidamos implementando na última semana, mas caso tivéssemos começado antes, talvez pudéssemos ter criado esses elementos com mais tranquilidade e organização.

### - Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele? 
Entender a escala do projeto, implementear o movimento de elementos de um modo geral, e dividir as tarefas entre os membros da equipe. Lidamos com um aumento da comunicação entre os membros e reuniões que estabeleceram o escopo do projeto.

### - Quais as lições aprendidas durante o projeto? 
Aprender a trabalhar em equipe para fazer um projeto dessa escala, comunicação entre a equipe, familizarização maior com a biblioteca de pygame, aprender a escrever código modularizado, a importancia de bons comentários no código, e a importância de padronizar o código quando se trabalha em equipe.


## Capturas de tela

![screenshot_menu](https://github.com/fabiopapais/bullet-hell/assets/160965589/9cb0eca6-2547-4caf-bae2-a0ffb7118750)

![screenshot_game](https://github.com/fabiopapais/bullet-hell/assets/160965589/ac93a9bd-5a32-453a-8808-c8984c98c459)

![game_gif](https://github.com/fabiopapais/bullet-hell/assets/160965589/6223e7a7-302e-4686-879d-9602e4bd2ff7)



## Como inicializar o projeto:
```
pip install -r requirements.txt
python bullet-hell/menu.py
```
