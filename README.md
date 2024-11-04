# abstractVectorSearch


## 1. Introdução

### 1.1 Dataset
O dataset utilizado é composto por cerca de 20.000 artigos publicados no arXiv de 2015 a 2024. O [ArXiv](https://arxiv.org/) é um arquivo open-sorce de artigos em diferentes áreas, como física, matemática, ciência da computaçã, finanças, economia, entre outras. Os artigos desse projeto foram retirados do [arXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv) presente no Kaggle.

### 1.2 Embeddings
Para realizar a busca desses artigos com um tema similar da entrada provida pelo usuário foi optado por gerar embeddings dos resumos dos artigos. Esses embeddings foram gerados com a partir dos embeddings pré-treinados do [GloVe](https://aclanthology.org/D14-1162/). O processo consistiu nos seguintes passos:
1. O resumo foi tokenizado baseado no vocabulário do GloVe de modo que cada palavra foi transformada em um número;
2. Os tokens foram transformados em uma matriz com os embeddings do GloVe;
3. Essa matriz passou por um processo no qual foi feita uma média na qual apenas as palavras que estavam no vocabulário do GloVe foram consideradas na conta. Assim, gerando um único vetor do resumo do artigo.

Na imagem abaixo, $t$ representa o tamanho da text e $n$ o tamanho do embedding do GloVe, eles assumem os valores de 800 e 300, respectivamente.

<p align="center">
    <img src="assets/gerador_embedding.png" alt="Dataset Embeddings" width="900"/>
</p>

### 1.3 Treinamento
Além disso, esses embeddings foram treinados para que se ajustassem ao contexto do dataset. O treinamento consistiu em reduzir a dimensão do vetor de $1 \times 300$ para $1 \times 200$, para então tentar recuperar as suas informações, ao fazer redimensionar a matriz para o seu formato original ($1 \times 300$). Esse processo foi realizado em 50 épocas, sendo que em cada uma o dataset foi dividido em batches de 64 linhas. O método utilizado foi o gradiente decendente com a intenção de minimizar o erro entre a matriz de entrada e saída. A função de erro utilizada foi o Erro Quadrático Médio, que pode ser descrita da seguinte forma.

$$
\ell(x, y) = mean(L)  ,\quad L = \{l_1,\dots,l_N\}^\top, \quad l_n = \left( x_n - y_n \right)^2
$$

Sendo $N$, o tamanho do batch.

## 2. Visualização
Para visualizar os embeddings tanto pré-treinamento, quanto pós-treinamento, foi utilizada a ferramenta TSNE. Ao observar as imagens, é possível notar que o formato geral dos artigos segue a mesma forma oval em ambas. Porém, os pequenos cluster formados em cada uma delas estão posicionados em lugares diferentes. 


<p align="center">
    <img src="assets/pre_trained_embeddings.png" alt="Pre-trained Embeddings" width="800"/>
    <img src="assets/tuned_embeddings.png" alt="Tuned Embeddings" width="800"/>
</p>

<p align="center">
</p>


## 3. Sistema de busca
O sistema de busca consiste em passar a entrada do usuário pelo processo de embeddings e usar o resultado para realizar a busca baseada na semelhança da entrada com cada um dos resumos dos artigos. Essa semelhança é calculada através do método do produto interno. 

### 3.1 Testes
Os resultados dos testes pode ser visto no [vector_search.ipynb](vector_search.ipynb)

#### 3.1.1 Teste com 10 resultados
Entrada: `neural network`
Comentário: Apesar de todos os resultados falarem sobre redes, parte de fato fala sobre redes neurais e outra parte fala de redes em geral. 

#### 3.1.2 Teste com menos de 10 resultados
Entrada: `cooper pair box`

#### 3.1.3 Teste não óbvio
Entrada: `wolf`
Comentário: A pesquisa pode sugerir resultados relacionados ao animal, porém ao fazer a busca é obtido como resultados tópicos inesperados como a galáxia Wolf-Rayet. Dessa maneira, pode-se dizer que esse resultado evidencia a capacidade do sistema de identificar e retornar documentos que se relacionam a tópicos mais nichados e menos conhecidos de uma certa entrada.
