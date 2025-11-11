# MovieBuddy

Bem-vindo ao **MovieBuddy**, o seu assistente inteligente de filmes!   
Desenvolvemos esse chatbot com o objetivo de oferecer recomendações personalizadas de forma simples, prática e divertida.  
Com ele, você não precisa mais perder horas navegando em catálogos infinitos ou se decepcionando com escolhas aleatórias — o MovieBuddy entende o que você quer assistir e entrega as melhores opções com base nas avaliações mais altas do público e da crítica!  

Basta pedir sugestões como:
> “Quero um filme de ação em Português”  
ou  
> “Me indique um bom drama em inglês”  

E pronto! O MovieBuddy usa técnicas de Processamento de Linguagem Natural para entender o gênero e o idioma da sua frase, consulta a API do TMDB (The Movie Database) e retorna os filmes mais bem avaliados que combinam com o seu gosto.  

## Download e Ativação

Para utilizar o MovieBuddy basta fazer o download do executável chamado MovieBuddy.exe, para isso existem duas maneiras:

**1 - Download direto do executável**

Clique [AQUI](https://drive.google.com/uc?export=download&id=1XJD-UHv8F-SOPEJJ8b7TP88BByuXYCur) para fazer o download do executável, é possível que a seguinte tela apareça:

![AVISOVIRUS](/Telas/Aviso_Vírus.jpg)

Basta clicar em Fazer o Downlaod mesmo assim que o arquivo sera armazenado no seu computador, isso é apenas uma medida de segurança do próprio GoogleDrive em relação a executáveis no formato .EXE.

**2 - Download via diretório GITHUB**

A segunda maneira é apenas baixar o próprio repositório do GITHUB o salvando em um arquivo .ZIP, da seguinte maneira:

Acesse o repositório do GITHUB por aqui ---> [REPOSITÓRIO MOVIEBUDDY](https://github.com/ClaudioFilipe00/Chatbot-MovieBuddy)

Após isso siga o passo mostrado na imagem:

![ZIP](/Telas/Download_ZIP.jpg)

Basta clicar em **<> Code** e depois em Download ZIP, com isso todo o repositório será salvo no computador no formato ZIP.

Após isso basta descompactar o arquivo clicando em Extract Here para descompactar na pasta atual ou Extract Files para escolher o local de destino, isso não afeta o funcionamento:

![EXTRACT](/Telas/Descompactando.jpg)

Após descompactar surgirá uma pasta com o nome **Chatbot-MovieBuddy-main**, clique nela e localize a pasta **dist**, dentro dela o instalador estará pronto e basta clicar nele duas vezes para executar.

![DIST](/Telas/Pasta_dist.jpg)

Caso queira clonar o repositório para sua máquina será o mesmo passo a passo explicado na segunda maneira, porém ele irá baixar o diretório instantâneo sem o arquivo .ZIP

**ATIVAÇÃO**

Se você decidir baixar através da primeira maneira, ou seja, por um link direto de download, no momento em que executar o .exe o windows provavelmente irá exibir a seguinte mensagem:

![AVISOWINDOWS](/Telas/Aviso_Windows.jpg)

Basa clicar em **mais informações** e logo após isso em **Executar assim mesmo**, dessa maneira o executável do MovieBuddy irá funcionar corretamente.
O Windows bloqueia aplicativos executaveis sem certificados oficiais, então ele lança essa mensagem para proteger o dispositivos de ameaças.

Após isso um prompt de comando será ativado automaticamente no CMD, apenas inicializando o servidor da IDE:

![CMD](/Telas/CMD_Inicio.jpg)

Ao iniciar o servidor o site local em que o chatbot está rodando será aberto automaticamente no seu navegador padrão:

![INCIADO](/Telas/Site_Carregado.jpg)

## Utilização

Com a tela ja carregada corretamente, agora basta utilizar da maneira que desejar, buscando quantos e qualquer genêro de filmes que desejar, alguns exemplos:

**Buscando filmes com Genêro e idioma fornecidos corretamente**

![BUSCACOMP](/Telas/Busca_Completa.jpg)

Colocando as informações corretas de genêro e idioma, o chatbot faz a busca automatica na API do TMDB e devolve os Dez melhores filmes de acordo com o Ranking de avaliação do site.

**Mais sugestões**

![MAISSUG](/Telas/Mais_sugestoes.jpg)

**Filme Selecionado**

Ao clicar em um filme de interesse o usuário pode ver suas informações e decidir se assiste ou não aquele filme sugerido.

![SELECIONADO](/Telas/Filme_selecionado.jpg)

**Mudança de genêro**

É possível alternar entre genêros quando quiser, e caso retorne ao anterior ele irá continuar a lista mostrando os próximos filmes ainda não sugeridos.

![TROCAGEN](/Telas/Troca_genero.jpg)

**Não Fornecendo Idioma**

Caso o usuário não insira o idioma que deseja, o chat não irá buscar o filme e fara uma requisição para usuário completar sua busca.

![NIDIOMA](/Telas/Filmes_sem_idioma.jpg)

**Idioma ajustado**

Após confirmar o idioma, ele faz a busca dos filmes.

![SIDIOMA](/Telas/idioma_ok.jpg)

**Pedindo Sugestão sem Genêro**

Ao não informar o genêro, o chat pede a informação completa ao usuário.

![NGENERO](/Telas/Sem_genero.jpg)

**Finalizando a Conversa e Retornando**

![FIMCONV](/Telas/Finalização_conversa.jpg)

![RETCONV](/Telas/Retorno_conversa.jpg)

**Sem Resultados**

Caso a pesquisa chegue até a ultima lista no TMDB do genêro e idioma fornecidos ou a busca não retorne nenhum filme, aparece uma mensagem de aviso que não foram encontrados filmes para sugerir.

![SEMFILME](/Telas/Sem_filmes.jpg)


## CONCLUSÃO

O MovieBuddy foi desenvolvido com o propósito de unir tecnologia e praticidade, tornando a busca por filmes uma experiência intuitiva, dinâmica e personalizada.
Ao compreender suas preferências e comunicar-se de forma natural, o chatbot oferece sugestões precisas e inteligentes, economizando seu tempo e ampliando suas opções de entretenimento.

Nosso objetivo é continuar aprimorando o MovieBuddy, incorporando novos recursos, expandindo o suporte a idiomas e tornando-o cada vez mais eficiente.

## AUTORES

Projeto desenvolvido pelos alunos do 6º Semestre do curso de Análise e Desenvolvimento de Sistemas da FATEC Arthur de Azevedo em Mogi-Mirim

**ANA BEATRIZ SANTOS LEAL** 

**CLAUDIO FILIPE TEMOTEO DE FARIAS**