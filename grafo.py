from tabulate import tabulate
from collections import deque
import networkx as nx
import numpy as np
import heapq
import time
from scipy.optimize import linear_sum_assignment

class Grafo:
    def __init__(self):
        self.vertices = []
        self.grafo = []
        self.tipo = None
        self.ponderado = None

    def adicionar_vertice(self):
        print()
        print('Aqui você informará um grafo para que as operações sejam feitas :)')
        print()
        time.sleep(1)
        
        while True:
            temp = input('Insira um vértice (caso queira parar, pressione enter): ')
            if temp != '':
                if temp in self.vertices:
                    print(f'Erro: o vértice "{temp}" já foi inserido. Por favor, insira um vértice único.')
                else:
                    self.vertices.append(temp)
            else:
                break

        if len(self.vertices) == 0:
            print()
            print('Um grafo não pode possuir 0 vértices.')
            print()
            time.sleep(3)
            self.adicionar_vertice()

    def definir_tipo(self):
        self.tipo = input('O grafo é orientado? (s/n): ').lower()
        if self.tipo not in ['s', 'n']:
            print()
            print('Entrada inválida. Defina como orientado ou não.')
            print()
            time.sleep(3)
            self.definir_tipo()

    def definir_ponderacao(self):
        resposta = input("O grafo é ponderado? (s/n): ").lower()
        if resposta == 's':
            self.ponderado = True
        else:
            self.ponderado = False

    def adicionar_arestas(self):
        pesos = []
        if self.tipo == 's':  # Grafo orientado
            for i in self.vertices:
                for j in self.vertices:
                    if i == j:  # Verifica se é um self-loop
                        ver = input(f'O vértice ({i}) tem um self-loop? ({i}<->{i}) (s/n): ')
                        if ver in 'Ss':
                            if self.ponderado:
                                peso = float(input(f'Insira o peso da aresta que liga ({i}) a ele mesmo: '))
                            else:
                                peso = 1  # Assumindo 1 para grafos não ponderados
                            pesos.append(peso)
                        else:
                            pesos.append(0)
                    else:  # Verifica se há uma conexão direta entre vértices diferentes
                        ver = input(f'O vértice ({i}) tem um caminho direto para ({j})? ({i}->{j}) (s/n): ')
                        if ver in 'Ss':
                            if self.ponderado:
                                peso = float(input(f'Insira o peso da aresta que liga ({i}) a ({j}): '))
                            else:
                                peso = 1  # Assumindo 1 para grafos não ponderados
                            pesos.append(peso)
                        else:
                            pesos.append(0)
                self.grafo.append(pesos[:])  # Adiciona a linha na matriz de adjacência
                pesos.clear()  # Limpa a lista de pesos para a próxima linha

        else:  # Grafo não orientado
            for i in self.vertices:
                for j in self.vertices:
                    if i == j:  # Verifica se é um self-loop
                        ver = input(f'O vértice ({i}) tem um self-loop? ({i}-{i}) (s/n): ')
                        if ver in 'Ss':
                            if self.ponderado:
                                peso = float(input(f'Insira o peso da aresta que liga ({i}) a ele mesmo: '))
                            else:
                                peso = 1  # Assumindo 1 para grafos não ponderados
                            pesos.append(peso)
                        else:
                            pesos.append(0)
                    elif self.vertices.index(i) < self.vertices.index(j):  # Verifica pares não repetidos
                        ver = input(f'O vértice ({i}) tem um caminho direto para ({j})? ({i}-{j}) (s/n): ')
                        if ver in 'Ss':
                            if self.ponderado:
                                peso = float(input(f'Insira o peso da aresta que liga ({i}) a ({j}): '))
                            else:
                                peso = 1  # Assumindo 1 para grafos não ponderados
                            pesos.append(peso)
                        else:
                            pesos.append(0)
                    else:  # Preenche a matriz simetricamente
                        pesos.append(self.grafo[self.vertices.index(j)][self.vertices.index(i)])
                self.grafo.append(pesos[:])  # Adiciona a linha na matriz de adjacência
                pesos.clear()  # Limpa a lista de pesos para a próxima linha

    def exibir_grafo(self):
        print("\nGrafo (em uma matriz de adjacência):")
        # Cabeçalho da tabela com os vértices
        header = [""] + self.vertices

        # Corpo da tabela com os pesos
        tabela = [[self.vertices[i]] + linha for i, linha in enumerate(self.grafo)]

        # Exibir usando tabulate
        print(tabulate(tabela, headers=header, tablefmt="grid"))

    def verificar_aresta(self, vertice1, vertice2):
        if vertice1 not in self.vertices or vertice2 not in self.vertices:
            print(f"Um ou ambos os vértices ({vertice1}, {vertice2}) não existem no grafo.")
            time.sleep(3)
            return False

        i = self.vertices.index(vertice1)
        j = self.vertices.index(vertice2)
        
        # Para grafos orientados ou não, a existência da aresta é verificada pelo peso
        if self.grafo[i][j] != 0:
            print(f"Existe uma aresta entre {vertice1} e {vertice2} com peso {self.grafo[i][j]}.")
            time.sleep(3)
            return True
        else:
            print(f"Não existe uma aresta entre {vertice1} e {vertice2}.")
            time.sleep(3)
            return False
        
    def grau_vertice(self, vertice=None):
        if vertice is None:
            vertice = input("Digite o vértice para verificar o seu grau: ")
        
        if vertice not in self.vertices:
            print(f"O vértice {vertice} não existe no grafo.")
            time.sleep(3)
            return None  # Adicionar retorno para erro

        indice = self.vertices.index(vertice)
        
        if self.tipo == 's':  # Grafo orientado
            grau_saida = 0
            grau_entrada = 0
            
            for j in range(len(self.grafo[indice])):
                if self.grafo[indice][j] != 0:  # Existe uma aresta saindo de 'vertice' para outro
                    if indice == j:  # Se for um self-loop
                        grau_saida += 1
                        grau_entrada += 1
                    else:
                        grau_saida += 1
            
            for i in range(len(self.grafo)):  # Verificar arestas entrando no 'vertice'
                if self.grafo[i][indice] != 0:
                    if i == indice:  # Self-loop
                        continue  # Já contabilizado
                    grau_entrada += 1
            
            print(f"O grau de saída do vértice {vertice} é {grau_saida}.")
            print(f"O grau de entrada do vértice {vertice} é {grau_entrada}.")
            time.sleep(3)
            return grau_saida + grau_entrada  # Retornar a soma dos graus de entrada e saída
            
        else:  # Grafo não orientado
            grau = 0
            for j in range(len(self.grafo[indice])):
                if self.grafo[indice][j] != 0:  # Existe uma aresta conectada a 'vertice'
                    if indice == j:  # Se for um self-loop
                        grau += 2  # Self-loop conta como dois graus
                    else:
                        grau += 1
            
            print(f"O grau do vértice {vertice} é {grau}.")
            time.sleep(3)
            return grau  # Retorna o grau do vértice
    
    def grau_vertice_saida(self, vertice):
        # Contar o número de arestas que saem do vértice
        return sum(self.grafo[self.vertices.index(vertice)])

    def grau_vertice_entrada(self, vertice):
        # Contar o número de arestas que entram no vértice
        return sum(row[self.vertices.index(vertice)] for row in self.grafo)

    def informa_adjacencia(self):
        vertice = input("Digite o vértice para verificar os adjacentes: ")

        if vertice not in self.vertices:
            print(f"O vértice {vertice} não existe no grafo.")
            time.sleep(3)
            return

        indice = self.vertices.index(vertice)
        
        if self.tipo == 's':  # Grafo orientado
            adjacentes_saida = []
            adjacentes_entrada = []

            # Adjacentes de saída (arestas que saem do vértice, sem self-loop)
            for j in range(len(self.grafo[indice])):
                if self.grafo[indice][j] != 0 and self.vertices[j] != vertice:
                    adjacentes_saida.append(self.vertices[j])

            # Adjacentes de entrada (arestas que entram no vértice, sem self-loop)
            for i in range(len(self.grafo)):
                if self.grafo[i][indice] != 0 and self.vertices[i] != vertice:
                    adjacentes_entrada.append(self.vertices[i])

            print(f"Os vértices adjacentes ao vértice {vertice} são:")
            print(f"Adjacentes de saída: {', '.join(adjacentes_saida) if adjacentes_saida else 'Nenhum'}")
            print(f"Adjacentes de entrada: {', '.join(adjacentes_entrada) if adjacentes_entrada else 'Nenhum'}")
            time.sleep(3)

        else:  # Grafo não orientado
            adjacentes = []
            for j in range(len(self.grafo[indice])):
                if self.grafo[indice][j] != 0 and self.vertices[j] != vertice:  # Exclui self-loops
                    adjacentes.append(self.vertices[j])

            print(f"Os vértices adjacentes ao vértice {vertice} são: {', '.join(adjacentes) if adjacentes else 'Nenhum'}.")
            time.sleep(3)

    def encontrar_ciclos(self):
        visitado = set()  # Conjunto de vértices já visitados
        pilha = []  # Pilha para armazenar o caminho atual

        def dfs(v, caminho, pai=None):
            visitado.add(v)
            caminho.append(v)
            
            for i, adj in enumerate(self.grafo[self.vertices.index(v)]):
                if adj != 0:  # Se há uma aresta para o vértice i
                    prox_vertice = self.vertices[i]
                    # Para grafos não orientados, evitamos visitar o vértice pai
                    if prox_vertice != pai:
                        if prox_vertice not in visitado:
                            if dfs(prox_vertice, caminho, v):  # Passamos o vértice atual como pai
                                return True
                        elif prox_vertice in caminho:  # Ciclo encontrado
                            ciclo = caminho[caminho.index(prox_vertice):] + [prox_vertice]
                            print(f"Ciclo encontrado: {' -> '.join(ciclo)}")
                            print('O grafo é cíclico! :D')
                            return True
            caminho.pop()
            return False

        # Chama a DFS para cada vértice
        for v in self.vertices:
            if v not in visitado:
                if dfs(v, pilha):
                    return True
        
        print("Não foram encontrados ciclos no grafo...")
        return False
    
    def eh_conexo(self):
        if self.tipo == 's':  # Verifica se o grafo é orientado
            print("Este grafo é orientado :(. A verificação de conectividade desse programa só é aplicável a grafos não-orientados.")
            return False

        if not self.vertices:
            print("O grafo não possui vértices.")
            return False

        # Função auxiliar para realizar DFS
        def dfs(v, visitados):
            visitados.add(v)
            i = self.vertices.index(v)
            for j in range(len(self.vertices)):
                if self.grafo[i][j] != 0 and self.vertices[j] not in visitados:
                    dfs(self.vertices[j], visitados)

        visitados = set()

        # Iniciamos a DFS a partir do primeiro vértice
        dfs(self.vertices[0], visitados)

        # Verifica se todos os vértices foram visitados
        if len(visitados) == len(self.vertices):
            print("O grafo é conexo.")
            return True
        else:
            print("O grafo não é conexo.")
            return False
    
    def componentes_fortemente_conexos(self):
        if self.tipo == 'n':  # Verifica se o grafo é não orientado
            print("Este grafo não é um dígrafo :(. A verificação de componentes fortemente conexos só é aplicável a dígrafos.")
            return []

        def dfs(v, visitados, pilha=None):
            visitados.add(v)
            i = self.vertices.index(v)
            for j in range(len(self.vertices)):
                if self.grafo[i][j] != 0 and self.vertices[j] not in visitados:
                    dfs(self.vertices[j], visitados, pilha)
            if pilha is not None:
                pilha.append(v)

        def dfs_transposto(v, visitados):
            visitados.add(v)
            i = self.vertices.index(v)
            componente.append(v)
            for j in range(len(self.vertices)):
                if transposto[i][j] != 0 and self.vertices[j] not in visitados:
                    dfs_transposto(self.vertices[j], visitados)

        # 1. Primeira Passagem
        pilha = []
        visitados = set()

        for vertice in self.vertices:
            if vertice not in visitados:
                dfs(vertice, visitados, pilha)

        # 2. Criar grafo transposto
        transposto = [[0 for _ in range(len(self.vertices))] for _ in range(len(self.vertices))]
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                transposto[j][i] = self.grafo[i][j]  # Inverte a direção das arestas

        # 3. Segunda Passagem
        visitados.clear()
        componentes = []

        while pilha:
            vertice = pilha.pop()
            if vertice not in visitados:
                componente = []
                dfs_transposto(vertice, visitados)
                componentes.append(componente)

        # Exibindo os componentes
        print("Componentes fortemente conexos:")
        print(componentes)  # Altera aqui para exibir a lista de componentes

        return componentes

    def ordenacao_topologica(self):
    # Verifica se o grafo é orientado
        if self.tipo == 's':  # Corrigido de self.tipo() para self.tipo
            print("Iniciando a ordenação topológica...")
            
            # Verificar se o grafo é acíclico antes de proceder
            if self.encontrar_ciclos():  # Se o grafo tiver ciclos, não é possível gerar uma ordenação topológica
                print("O grafo possui ciclos e, portanto, não é acíclico.")
                return

            # Iniciando a busca em profundidade (DFS) para a ordenação topológica
            visitado = set()
            pilha = []

            def dfs(v):
                visitado.add(v)
                for vizinho in range(len(self.grafo[v])):
                    if self.grafo[v][vizinho] != 0 and vizinho not in visitado:
                        dfs(vizinho)
                pilha.append(self.vertices[v])

            for vertice in range(len(self.vertices)):
                if vertice not in visitado:
                    dfs(vertice)

            # Inverte a pilha para obter a ordem topológica
            pilha.reverse()
            print("Ordenação Topológica:")
            print(pilha)

        else:
            print("Ordenação topológica só pode ser gerada para dígrafos :(.")

    def verificar_euleriano(self):
        # Verifica se o grafo é orientado
        if self.tipo == 's':
            # Verifica se todos os vértices têm grau de entrada igual ao grau de saída
            for vertice in self.vertices:
                grau_saida = self.grau_vertice_saida(vertice)
                grau_entrada = self.grau_vertice_entrada(vertice)
                if grau_saida is None or grau_entrada is None or grau_saida != grau_entrada:
                    print(f"O vértice {vertice} não tem grau de entrada igual aos grau de saida, logo o grafo não é euleriano.")
                    return

            # Se passar pela verificação, o grafo orientado é euleriano
            print("O grafo orientado é euleriano! Um ciclo euleriano é:")
            
            # Encontrar e imprimir um ciclo euleriano
            ciclo = self.encontrar_ciclo_euleriano()
            print(" -> ".join(ciclo))
            return

        # Verifica se o grafo é conexo
        if not self.eh_conexo():
            print("O grafo não é conexo, então não pode ser euleriano.")
            return

        # Verifica se todos os vértices têm grau par para grafos não orientados
        for vertice in self.vertices:
            grau = self.grau_vertice(vertice)
            if grau is None or grau % 2 != 0:
                print(f"O vértice {vertice} tem grau ímpar, logo o grafo não é euleriano.")
                return

        # Se passar pelas verificações acima, o grafo não orientado é euleriano
        print("O grafo não orientado é euleriano! Um ciclo euleriano é:")
        
        # Encontrar e imprimir um ciclo euleriano
        ciclo = self.encontrar_ciclo_euleriano()
        print(" -> ".join(ciclo))

    def encontrar_ciclo_euleriano(self):
        # Implementação do algoritmo Hierholzer para encontrar um ciclo euleriano
        grafo_copia = [linha[:] for linha in self.grafo]  # Faz uma cópia da matriz de adjacência
        ciclo = []
        stack = [self.vertices[0]]  # Começa em um vértice arbitrário

        while stack:
            u = stack[-1]
            encontrou_aresta = False

            for v in range(len(self.vertices)):
                if grafo_copia[self.vertices.index(u)][v] != 0:  # Verifica se há aresta
                    stack.append(self.vertices[v])
                    # Remove a aresta percorrida
                    grafo_copia[self.vertices.index(u)][v] = 0
                    grafo_copia[v][self.vertices.index(u)] = 0
                    encontrou_aresta = True
                    break

            if not encontrou_aresta:
                ciclo.append(stack.pop())

        return ciclo
    
    def verificar_conjuntos(self):
        # Solicita ao usuário que informe os vértices que deseja verificar
        conjunto = input("Digite os vértices do conjunto separados por vírgula: ").split(',')
        
        # Removendo espaços e garantindo que os vértices estão no grafo
        conjunto = [v.strip() for v in conjunto if v.strip() in self.vertices]
        
        if not conjunto:
            print("Nenhum vértice válido foi informado.")
            return

        # Verifica se o conjunto é independente
        independente = True
        for i in range(len(conjunto)):
            for j in range(i + 1, len(conjunto)):
                v1 = self.vertices.index(conjunto[i])
                v2 = self.vertices.index(conjunto[j])
                if self.grafo[v1][v2] != 0:  # Se existe aresta entre v1 e v2
                    independente = False
                    break

        if independente:
            print("O conjunto informado é independente.")
        else:
            print("O conjunto informado não é independente.")

        # Verifica se o conjunto é um clique
        clique = True
        for i in range(len(conjunto)):
            for j in range(i + 1, len(conjunto)):
                v1 = self.vertices.index(conjunto[i])
                v2 = self.vertices.index(conjunto[j])
                if self.grafo[v1][v2] == 0:  # Se não existe aresta entre v1 e v2
                    clique = False
                    break

        if clique:
            print("O conjunto informado é um clique.")
        else:
            print("O conjunto informado não é um clique.")

        # Verifica se o conjunto é dominante
        dominante = True
        todos_vertices = set(self.vertices)
        dominados = set(conjunto)

        # Verifica se todos os outros vértices estão conectados a algum vértice do conjunto
        for v in self.vertices:
            if v not in conjunto:
                dominado = False
                for u in conjunto:
                    v1 = self.vertices.index(v)
                    v2 = self.vertices.index(u)
                    if self.grafo[v1][v2] != 0 or self.grafo[v2][v1] != 0:
                        dominado = True
                        break
                if not dominado:
                    dominante = False
                    break

        if dominante:
            print("O conjunto informado é dominante.")
        else:
            print("O conjunto informado não é dominante.")
    
    def eh_planar(self):
        # Criar um grafo a partir da matriz de adjacência
        G = nx.Graph()

        # Adicionar nós e arestas a partir da matriz de adjacência
        n = len(self.grafo)
        for i in range(n):
            for j in range(i + 1, n):
                if self.grafo[i][j] == 1:
                    G.add_edge(i, j)

        # Verificar se o grafo é planar
        planar, _ = nx.check_planarity(G)
        return planar 

    def caminho_mais_curto(self, inicio, fim):
        # Verificar se os vértices existem no grafo
        if inicio not in self.vertices or fim not in self.vertices:
            print("Erro: O grafo não possui um ou ambos os vértices inseridos.")
            return None

        # Se os vértices forem válidos, continuar normalmente
        if self.ponderado:
            caminho, distancia = self._dijkstra(inicio, fim)
            return caminho, distancia
        else:
            caminho = self._bfs(inicio, fim)
            return caminho

    def _bfs(self, inicio, fim):
        # Verificar se os vértices existem no grafo
        if inicio not in self.vertices or fim not in self.vertices:
            print("Erro: O grafo não possui um ou ambos os vértices inseridos.")
            return None

        # Implementação de BFS para caminho mais curto em grafo não ponderado
        fila = deque([inicio])
        pais = {inicio: None}
        visitado = set()

        while fila:
            vertice_atual = fila.popleft()
            if vertice_atual == fim:
                return self._reconstruir_caminho(pais, fim)

            indice_atual = self.vertices.index(vertice_atual)
            visitado.add(vertice_atual)

            for i, valor in enumerate(self.grafo[indice_atual]):
                if valor == 1:  # Existe aresta entre vertice_atual e o vértice self.vertices[i]
                    vizinho = self.vertices[i]
                    if vizinho not in visitado and vizinho not in pais:
                        pais[vizinho] = vertice_atual
                        fila.append(vizinho)

        return None  # Nenhum caminho encontrado

    def _dijkstra(self, inicio, fim):
        # Verificar se os vértices existem no grafo
        if inicio not in self.vertices or fim not in self.vertices:
            print("Erro: O grafo não possui um ou ambos os vértices inseridos.")
            return None, float('inf')

        # Inicialização
        fila_prioridade = [(0, inicio)]
        distancias = {vertice: float('inf') for vertice in self.vertices}
        distancias[inicio] = 0
        pais = {inicio: None}
        visitado = set()

        while fila_prioridade:
            custo_atual, vertice_atual = heapq.heappop(fila_prioridade)
            if vertice_atual == fim:
                return self._reconstruir_caminho(pais, fim), distancias[fim]

            indice_atual = self.vertices.index(vertice_atual)  # Converte o vértice para o índice
            visitado.add(vertice_atual)

            # Percorre os vizinhos
            for i, peso in enumerate(self.grafo[indice_atual]):
                if peso > 0 and self.vertices[i] not in visitado:  # Existe uma aresta com peso > 0
                    vizinho = self.vertices[i]  # Converte o índice para o rótulo do vértice
                    novo_custo = custo_atual + peso

                    # Atualiza a distância mínima se encontrado caminho mais curto
                    if novo_custo < distancias[vizinho]:
                        distancias[vizinho] = novo_custo
                        pais[vizinho] = vertice_atual
                        heapq.heappush(fila_prioridade, (novo_custo, vizinho))

        return None, float('inf')  # Retorna None se nenhum caminho for encontrado

    def _reconstruir_caminho(self, pais, fim):
        # Reconstrói o caminho a partir do dicionário de pais
        caminho = []
        while fim is not None:
            caminho.append(fim)
            fim = pais[fim]
        return caminho[::-1]
    
    def arvore_geradora_minima(self, vertice_partida):
        if self.tipo == 's':  # Verifica se o grafo é orientado
            print("Erro: Não é possível realizar essa operação em dígrafos.")
            return None

        # Inicializa estruturas para Prim's algorithm
        visitados = [False] * len(self.vertices)
        arestas = []
        visitados[vertice_partida] = True

        while len(arestas) < len(self.vertices) - 1:
            menor_peso = float('inf')
            aresta_atual = (-1, -1)

            for i in range(len(self.vertices)):
                if visitados[i]:
                    for j in range(len(self.vertices)):
                        if not visitados[j] and self.grafo[i][j] > 0:  # Se a aresta existe
                            if self.grafo[i][j] < menor_peso:
                                menor_peso = self.grafo[i][j]
                                aresta_atual = (i, j)

            if aresta_atual == (-1, -1):
                break  # Não há mais arestas para adicionar

            arestas.append(aresta_atual)
            visitados[aresta_atual[1]] = True
        return arestas
    
    def biparticionar_grafo(self):
        color = {}
        for vertex in self.vertices:
            color[vertex] = None

        queue = deque()

        for start in self.vertices:
            if color[start] is None:  # Não visitado
                color[start] = 0
                queue.append(start)

                while queue:
                    current = queue.popleft()
                    current_color = color[current]

                    for neighbor_index, weight in enumerate(self.grafo[self.vertices.index(current)]):
                        if weight > 0:  # Se há uma aresta
                            neighbor = self.vertices[neighbor_index]

                            if color[neighbor] is None:  # Não visitado
                                color[neighbor] = 1 - current_color
                                queue.append(neighbor)
                            elif color[neighbor] == current_color:  # Conflito de cores
                                print("O grafo não pode ser bipartido.")
                                return None, None, None

        # Criar os conjuntos
        conjunto_a = [v for v in color if color[v] == 0]
        conjunto_b = [v for v in color if color[v] == 1]

        print(f"Conjunto A: {conjunto_a}")
        print(f"Conjunto B: {conjunto_b}")

        # Criar a matriz de custos que reflete a bipartição (A -> B)
        matriz_bipartida = []
        for i in range(len(conjunto_a)):
            linha = []
            for j in range(len(conjunto_b)):
                peso = self.grafo[self.vertices.index(conjunto_a[i])][self.vertices.index(conjunto_b[j])]
                linha.append(peso if peso > 0 else float('inf'))  # Usar infinito se não houver aresta
            matriz_bipartida.append(linha)

        return conjunto_a, conjunto_b, np.array(matriz_bipartida)
    
    def aplicar_algoritmo_hungaro(self):
        conjunto_a, conjunto_b, cost_matrix = self.biparticionar_grafo()

        if conjunto_a is None or conjunto_b is None:
            print("Não foi possível aplicar o algoritmo Húngaro devido a falhas na bipartição.")
            return

        # Aplicando o algoritmo Húngaro (linear sum assignment)
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        total_cost = cost_matrix[row_ind, col_ind].sum()

        # Exibindo o resultado
        print("\nAtribuição ótima (Conjunto A -> Conjunto B):")
        for i, j in zip(row_ind, col_ind):
            if cost_matrix[row_ind[i], col_ind[j]] != float('inf'):  # Ignorar atribuições inválidas
                print(f"{conjunto_a[i]} -> {conjunto_b[j]}")

        print(f"Custo total mínimo: {total_cost}")
