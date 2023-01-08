# Programação com Sockets e Multicast I

## Programação com *Sockets*

- **O que é um *socket*?**
  - "Porta" entre o processo da aplicação e o protocolo de transporte *end-to-end*.
- Existem dois tipos de *sockets* para 2 tipos de serviços de transporte:
  - **UDP**: datagramas não confiáveis;
  - **TCP**: confiável, *bytes* orientados às *streams*.

### Com UDP

- Não à "conexão" entre cliente e servidor;
  - Não existe o "*handshaking*" antes de se inicar o envio de dados;
  - Emissor insere o endereço IP de destino e a porta, de forma explícita, em cada *packet*;
  - Recetor extrai o endereço IP e a porta do emissor a partir de *packet* recebido.
- Dados transmitidos podem ser perdidos ou recebidos fora da ordem correta.

### Com TCP

- Cliente deverá entrar em contacto com o servidor;
  - O processo do servidor deve ser o primeiro a correr;
  - O servidor deve criar um *socket* que dará as boas-vindas ao contacto do cliente.
- Cliente contacta o servidor:
  - Cria um *socket* TCP especificando o endereço IP e o número da porta do processo do servidor;
    - Quando cria este *socket* estabelece conexão ao servidor TCP.
- Quando o servidor é contactado pelo cliente, cria um novo *socket* para cada processo do servidor de forma a comunicar com aquele cliente em particular.
  - Permite que o servidor comunique com múltiplos clientes;
  - Os números das portas da origem são usadas para distinguir clientes.

## *Multicast*

- Existe uma série de aplicações que são orientadas a grupos.
  - Uma solução para isto seria estabelecer múltiplas conexões *multicast*.
    - A origem irá manter uma lista de recetores;
    - A origem terá de enviar múltiplas cópias idênticas dos mesmos dados;
    - Solução custosa em termos de recursos.

- A solução para estes problemas passa por enviar 1 única vez o ficheiro e, algures na rede, de preferência o mais perto possível do cliente, os dados serão multiplixados.
  - Ocupar-se-á uma menor largura de banda;
  - Não serão realizados envios desnecessários por parte do servidor de origem;
  - Não é necessário manter em registo todos os endereços IPs dos recetores, utilizando um único endereço especial para realizar esta operação.

- Assim, o grande **objetivo** do *Multicast* é:
  - Enviar uma **única** cópia dos dados para um grupo de clientes identificados pelo endereço de *multicast*.
- Os *routers* deverão reencaminhar os pacotes e, quando necessário, duplicá-los.

![image Multicast](images/multicast.png)

### Como fazer a gestão dos participantes do grupo *multicast*?

- *Apps*/*Hosts* deverão utilizar *Multicast Group Membership Discovery Protocols* (em IPv4 é o IGMP) de forma a informar a rede do seu desejo para receber dados (enviando uma mensagem ao *router* de *multicast*);
- Os *routers* de *multicast* deverão comunicar entre eles utilizando protocolos de *routing multicast*;
  - Os protocolos de *routing* precisão de contruir uma árvore de distribuição de *multicast*;
  - O tráfego chega a todos os recetores que se juntaram ao grupo;
  - O número de cópias idênticas é minimizado.
- Os nós de *overlay multicast* poderão ter de propagar o interesse na rede para informar os nós participantes do trajeto que os dados terão de percorrer e estes poderem iniciar/parar a difusão de dados.
  - De tempos a tempos, o *router* de acesso questiona se ainda há interesse.

**NOTA**

- Mutias vezes, o pedido IGMP nem chega ao servidor fonte, pois, o *router* que vai receber o pedido já tem o conteúdo pretendido.

### *Multicast Group Discovery Protocols*

- Utilizado por *apps*/*hosts* para informar os *routers* na LAN do endereço *multicast* do grupo ao qual se pretendem juntar.
  - Em IPv4 $\rightarrow$ *Internet Group Management Protocol* (IGMP);
  - Em IPv6 $\rightarrow$ *Multicast Listener Discovery*.

- **Operação Básica de IGMP**
  - *Host* pretende juntar-se a um novo grupo de *multicast* $\rightarrow$ envia uma mensagem não solicitada de *IGMP Report* para o grupo;
  - O *router* local utiliza um protocolo de *routing* de *multicast* para juntar-se ao grupo de *multicast*;
  - De forma periódica, um *querier router* envia mensagens *IGMP Query* em *broadcast* para verificar em que grupos os *local hosts* se encontram;
  - *Hosts* respondem às mensagens enviando mensagens de *IGMP Report* a indicar em que grupo se encontram;
  - Se um *router* não receber uma mensagem de *Report* para um dado grupo durante um período de tempo, assume que não existem mais membros desse grupo na LAN e remove-se do grupo de *multicast*.
- Envio de *Queries*
  - IGMPv1 dependo da decisão de qual *router* será o *querier* do protocolo de *routing* de *multicast*;
  - IGMPv2 introduz um processo de eleição do *querier*,
- Respostas a *Queries*
  - Para evitar respostas simultâneas:
    - Cada *host* inicia um *timer* aleatórios para cada grupo do qual é membro;
    - Quando o *timer* terminar, envia um *IGMP report*;
      - Se, entretanto, receber outra mensagem no mesmo grupo:
        - Cancela o *timer*.
- Melhoria da latência do membros do grupo;
  - O IGMPv2 introduz uma *Leave Group Message*.
- Filtragem dos endereços de origem.
  - IGMPv3 introduz mensagens de *report* que permitem a inclusão ou exclusão da lista de origens para grupos de *multicast* do qual é membro.

### *Flood & Prune*

- Abordagem para a construção da árvore *multicast*.

1. Faz *flood* do conteúdo por toda a rede;
2. Começa a cortar os "ramos" que não têm ouvintes.
   1. Vai à informação do estado dos diversos nós da rede e altera a interface de saída $x$ para inativa;
   2. Quando é feito o *join* do nó, essa informação é atualizada.

- Nesta abordagem, o nó de *overlay multicast* tem de manter a seguinte informação:
  - IP da origem;
  - Estado das interfaces de rede.

- É eficiente por se tratar de uma árvore muito dinâmica.
  - Se, por exemplo, se usar *Dijsktra* ter-se-ia de recalcular todas as rotas a cada alteração.

### Outra Estratégia

- Construir a árvore a partir do recetor.
  - Vai informando que se quer juntar e constrói a árvore;
    - Vai criando estado.
  - Em casos de vários caminhos possíveis será o *router unicast* a esolher o percurso que irá percorrer.  