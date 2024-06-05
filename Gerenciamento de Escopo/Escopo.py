# Aluno: Pedro Affono Silva Marques
# Função para ler o código fonte do arquivo
# Abre o arquivo e retorna uma lista onde cada item é uma linha do arquivo(prorama)
# Encoding = 'utf-8' para suportar acentos e caracteres especiais
def lerArq(caminhoArq):
    try:
        with open(caminhoArq, 'r', encoding='utf-8') as arquivo:
            arq = arquivo.readlines()
            return arq
    except FileNotFoundError:
        print(f"Arquivo {caminhoArq} não encontrado")
    except Exception as e:
        print(f"O erro {e} foi encontrado ao tentar ler {caminhoArq}")

# Função para escrever a saída nos arquivos de saída em relação a cada código
# Abre em modo 'a' para que cada alteração não sobrescreva o processo de escrita
# Encoding = 'utf-8' para suportar acentos e caracteres especiais
def escreverArq(caminhoArq, texto):
    try:
        with open(caminhoArq, 'a', encoding='utf-8') as arquivo:  # Usando modo 'a' para adição
            arquivo.write(texto + "\n")
    except IOError as e:
        print(f'Ocorreu um erro ao abrir ou escrever no arquivo: {e}')
# Classe que representa um símbolo da linguagem fictícia proposta no trabalho
# Um símbolo possui token, lexema,tipoDado e valor
class Simbolo:
    def __init__(self, token, lexema, tipoDado, valor=None):
        self.token = token
        self.lexema = lexema
        self.tipoDado = tipoDado
        # Se nenhum valor for atribuido na criação do símbolo ele verifica o tipo
        if valor is None:
            if self.tipoDado == "NUMERO":
                self.valor = 0  # Valor padrão para número
            elif self.tipoDado == "CADEIA":
                self.valor = ""  # Valor padrão para cadeia
        else:
            self.valor = valor  # Qualquer outro valor é atribuído

# Classe que simula a tabela (dicionário) para abordagem da op2 proposta no trabalho
class TabelaSimbolo:
    # Tk_identificador é o único token que importa para o contexto do trabalho
    # Trata o lexema para guardar cada variável encontrada
    # Toda variável quando declarada vai possui um valor se não houver erro de tipo

    def __init__(self):
        self.tabela = {}  # Dicionário onde a chave é a variável e o valor é objeto simbolo

    def adicionarSimbolo(self, simbolo):
        # Adiciona o objeto simbolo completo na chave referente a varíavel
        self.tabela[simbolo.lexema] = simbolo

    def obterSimbolo(self, lexema):
        # Obtêm a variável da tabela de símbolos, None se não houver
        return self.tabela.get(lexema, None)

    def __contains__(self, lexema):
        # Retorna True se a varíavel(Lexema) está na tabela de símbolos
        return lexema in self.tabela
    
# Pilha para armazenar as tabelas de símbolos (escopos)
# Cada índice da pilha guarda uma instância(objeto) da classe TabelaSimbolo
# Desssa forma cada posicão da pilha guarda a tabela de símbolos do último escopo aberto
# Utilizando lista para simular a pilha, já que o pop retira o último da lista
pilhaTabelas = []
# Função principal que é usada para percorrer as linhas do programa
# Função responsável por verificar os erros e adicionar os prints corretos na saída
# Processa cada linha do programa, verificando todos os casos possíveis
def processarLinha(linha, numeroLinha):
    # A pilha de tabelas é global, porque é uma pilha para o programa inteiro
    global pilhaTabelas
    linha = linha.strip()  # Remove espaços em branco no início e no final da linha
    if linha.startswith("BLOCO"):
        # Cria uma nova tabela de símbolos e empilha
        # Todo BLOCO encontrado representa uma nova instância da classe TabelaSimbolo
        # Adiciona uma nova tabela(novo bloco) na pilha
        pilhaTabelas.append(TabelaSimbolo())
    elif linha.startswith("FIM"):
        # Remove a tabela de símbolos do escopo atual (desempilha)
        # Como está organizado lexicalmente e sintaticamente sempre retira o bloco respectivo à última abertura
        if pilhaTabelas:
            # Remove a última tabela inteira, toda a tabela de símbolo do último bloco (finalizado)
            pilhaTabelas.pop()

    elif linha.startswith("NUMERO") or linha.startswith("CADEIA"):
        # Considerando a organização sintática e semântica
        # Basicamente aqui é jogar o primeiro elemento do split por espaço, que vai ser o tipo de dado certamente
        # Utilizei a lógica de que a organização iria me ajudar então só fui separando pela organização esperada
        # Todo o resto(sem ser o tipo) faz parte de declarações
        tipoDado, declaracoes = linha.split(" ", 1)
        # Se existir declaração de mais uma variável separada por vírgula retorna vetor com mais de um elemento
        declaracoes = declaracoes.split(",")
        for declaracao in declaracoes:
            if "=" in declaracao:
                # Caso tenha a = 10 separa cada uma das atribuições
                # Aplica str.strip para cada lado
                # Declaracao.split("=") retorna vetor o lado esquerdo e o lado direito são os elementos
                # Lado esquerdo = variavél(lexema)
                # Lado direito = valor
                lexema, valor = map(str.strip, declaracao.split("="))
                if tipoDado == "NUMERO":
                    valor = float(valor) if '.' in valor else int(
                        valor)  # Cast para cada tipo de numero
                elif tipoDado == "CADEIA":
                    valor = valor.strip('"')
                    # Retira as "" para capturar exatamente a palavra, "" é adicionada apenas para escrever saída
                simbolo = Simbolo("tk_identificador", lexema,
                                  tipoDado, valor)  # Cria o símbolo
            else:
                # Se não houver "=" a declaração é diretamente a variável(lexema)
                # Caso declaracao seja " a " retira espaços em branco no ínicio e no final e guarda a
                lexema = declaracao.strip()
                # Cria o símbolo com valor base definido para cada tipo 0 pra NUMERO e "" para CADEIA
                simbolo = Simbolo("tk_identicador", lexema, tipoDado)
            # Adiciona o símbolo na tabela do escopo atual
            pilhaTabelas[-1].adicionarSimbolo(simbolo)
            # Topo da pilha recebe uma chave nova(variável) e o valor que é o objeto simbolo criado

    elif linha.startswith("PRINT"):
        # Impressão de variáveis
        # Segundo elemento desse vetor sempre vai ser a varíavel(lexema)
        lexema = linha.split(" ")[1]
        simbolo = None  # Se o simbolo não for encontrado imprime erro, por isso assume valor None inicialmente

        # Olha a pilha de trás pra frente, pois dessa forma olha do bloco mais interno para o mais externo
        for tabela in reversed(pilhaTabelas):
            # Percorre a pilhaTabelas como se fosse uma pilha então o último elemento sempre é o bloco mais interno
            # Se a chave existe no dicionário(tabela) do escopo
            if lexema in tabela:
                # Obtêm o símbolo associado a essa variável
                simbolo = tabela.obterSimbolo(lexema)
                break  # Termina a busca
        if simbolo:
            valor = f'"{simbolo.valor}"' if simbolo.tipoDado == "CADEIA" else str(
                simbolo.valor)
            escreverArq("saida.txt", valor)  # Escreve no arquivo de saída
        else:
            erro_msg = f"Erro linha {numeroLinha} - Variável não declarada"
            escreverArq("saida.txt", erro_msg)  # Escreve no arquivo de saída

    # Verifica linhas que contem atribuição, não começam NUMERO, CADEIA, BLOCO,FIM ou PRINT
    elif "=" in linha:
        # Atribuições do tipo ID=ID ou ID=CONST
        # Atribuição de valores, separa o lado esquerdo do lado lado direito
        lexema, valor = map(str.strip, linha.split("="))
        simbolo = None
        # Percorre cada tabela,do escopo interno até o mais externo
        for tabela in reversed(pilhaTabelas):
            # Olhando do escopo atual até o mais antigo
            if lexema in tabela:
                # Se existe a variável, obtêm objeto Símbolo
                simbolo = tabela.obterSimbolo(lexema)
                break
        if simbolo:
            # Achou símbolo, verifica se é NUMERO
            if simbolo.tipoDado == "NUMERO":
                # Olha se o lado direito é um NUMERO de fato e substitui - float se tiver "." e int senão tiver
                # Verifica se a string em valor(lado direito) é de fato um número real válido (positivo ou negativo)
                if valor.replace('.', '', 1).isdigit() or valor.lstrip('-').replace('.', '', 1).isdigit():
                    simbolo.valor = float(
                        valor) if '.' in valor else int(valor)
                # Se o lado direito for uma const do tipo CADEIA então erro de incompatibilidade
                elif valor.startswith('"') and valor.endswith('"'):
                    erro_msg = f"Erro linha {
                        numeroLinha}, tipos não compatíveis"
                    escreverArq("saida.txt", erro_msg)
                else:
                    # Se o lado direito = valor for um ID
                    # Olha se o lado direito de ID=ID é de uma variável com tipos compatíveis
                    simbolo_origem = None
                    # Procura a variavél do lado direito e obtem
                    for tabela in reversed(pilhaTabelas):
                        if valor in tabela:
                            # Obtêm o objeto Símbolo guardado em valor(ID)
                            simbolo_origem = tabela.obterSimbolo(valor)
                            break
                    if simbolo_origem:
                        if simbolo_origem.tipoDado == "NUMERO":
                            # Se o lado direito de ID = ID existe e for de mesmo tipo então atualiza valor
                            simbolo.valor = simbolo_origem.valor
                        else:
                            # Se for diferente acusa erro de tipos incompatíveies
                            erro_msg = f"Erro linha {
                                numeroLinha}, tipos não compatíveis"
                            escreverArq("saida.txt", erro_msg)
                    else:
                        # Se variavél do lado direito não existe printa erro de declaração
                        erro_msg = f"Erro linha {
                            numeroLinha} - Variável não declarada"
                        escreverArq("saida.txt", erro_msg)

            elif simbolo.tipoDado == "CADEIA":
                # Se o lado direito for do tipo CADEIA olha se o lado direito também é uma
                if valor.startswith('"') and valor.endswith('"'):
                    # Retiro "" para adicionar só na hora de escrever saída
                    simbolo.valor = valor.strip('"')
                # Se o lado direito tiver const do tipo NUMERO então erro de incompatibilidade
                elif valor.replace('.', '', 1).isdigit() or valor.lstrip('-').replace('.', '', 1).isdigit():
                    erro_msg = f"Erro linha {
                        numeroLinha}, tipos não compatíveis"
                    escreverArq("saida.txt", erro_msg)
                else:
                    # Se o lado direito for uma variável, procura pela variável
                    simbolo_origem = None
                    for tabela in reversed(pilhaTabelas):
                        if valor in tabela:
                            simbolo_origem = tabela.obterSimbolo(valor)
                            break
                    if simbolo_origem:
                        if simbolo_origem.tipoDado == "CADEIA":
                            # Se o lado direito de ID = ID existe e for de mesmo tipo então atualiza valor
                            simbolo.valor = simbolo_origem.valor
                        else:
                            # Se for diferente acusa erro de tipos incompatíveies
                            erro_msg = f"Erro linha {
                                numeroLinha}, tipos não compatíveis"
                            escreverArq("saida.txt", erro_msg)
                    else:
                        # Se variavél do lado direito não existe printa erro de declaração
                        erro_msg = f"Erro linha {
                            numeroLinha} - Variável não declarada"
                        escreverArq("saida.txt", erro_msg)
        else:
            # Se símbolo (variável retornou none a partir do get do dicionário(tabela) então não está em nenhum escopo
            erro_msg = f"Erro linha {numeroLinha} - Variável não declarada"
            escreverArq("saida.txt", erro_msg)

# Lê o programa do arquivo de entrada
programa = lerArq("exemplo2.txt")
if programa:
    # Limpa o arquivo de saída antes de escrever nele
    open("saida.txt", 'w', encoding='utf-8').close()
    # Usa enumarate para obter índice i e a linha = conteúdo da linha (string) de cada linha do código
    for i, linha in enumerate(programa):
        linha = linha.strip()
        if linha:
            # Se linha não estiver vazia, processar linha
            # Passa i+1 para começar do 1 e não do 0
            processarLinha(linha, i + 1)