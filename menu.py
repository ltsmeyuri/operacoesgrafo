from grafo import Grafo
import time

grafo = None

def escolher_opcao():
    global grafo
    # Exibe a lista de opções
    print()
    time.sleep(0.3)
    print('༺♥༻❀༺♥༻'*10)
    time.sleep(0.1)
    print('༘˚⋆𐙚｡⋆𖦹.✧'*8)
    time.sleep(0.5)
    print()
    print('Este programa faz operações diversas com um grafo informado! ')
    time.sleep(1)
    print()
    print('Selecione abaixo a opção desejada e divirta-se :D')
    time.sleep(1)
    print()
    print()
    print('1. Informar/mudar grafo.')
    time.sleep(0.1)
    print('2. Exibir grafo.')
    time.sleep(0.1)
    print('3. Verificar a existência de uma aresta.')
    time.sleep(0.1)
    print('4. Verificar o grau de um vértice.')
    time.sleep(0.1)
    print('5. Verificar a adjacência de um vértice.')
    time.sleep(0.1)
    print('6. Verificar se o grafo é cíclico.')
    time.sleep(0.1)
    print('7. Verificar se o grafo não-orientado é conexo.')
    time.sleep(0.1)
    print('8. Informar quantos e quais são os componentes fortemente conexos de um dígrafo.')
    time.sleep(0.1)
    print('9. Gerar ordenação topologica de um dígrafo acíclico.')
    time.sleep(0.1)
    print('10. Verificar se o grafo informado é euleriano.')
    time.sleep(0.1)
    print('11. Verificar se um conjunto de vértices é independente, um clique e/ou dominante.')
    time.sleep(0.1)
    print('12. Verificar se o grafo é planar.') 
    time.sleep(0.1)
    print('13. Verificar o caminho mais curto ou de menor custo entre dois vértices.') 
    time.sleep(0.1)
    print('14. Encontrar a árvore geradora minima de grafos não-orientados.') 
    time.sleep(0.1)
    print('15. Aplicar o Algoritmo Húngaro (para um grafo bipartido, completo e com ponderação)') 
    time.sleep(0.1)
    print()
    print()
    print('༘˚⋆𐙚｡⋆𖦹.✧'*8)
    time.sleep(0.1)
    print('༺♥༻❀༺♥༻'*10)
    print()

    # Solicita a escolha do usuário
    opcao = int(input("Digite o número da sua escolha: "))

    if opcao == 1:
        grafo = Grafo()
        grafo.adicionar_vertice()
        grafo.definir_tipo()
        grafo.definir_ponderacao()
        grafo.adicionar_arestas()
        escolher_opcao()
    elif opcao == 2:
        if grafo is None:  
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            grafo.exibir_grafo()
            time.sleep(3)
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 3:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            vertice1 = input("Informe o primeiro vértice: ")
            vertice2 = input("Informe o segundo vértice: ")
            grafo.verificar_aresta(vertice1, vertice2)
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 4:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            grafo.grau_vertice()
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 5:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            grafo.informa_adjacencia()
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 6:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            grafo.encontrar_ciclos()
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 7:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            grafo.eh_conexo()
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 8:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            grafo.componentes_fortemente_conexos()
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 9:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            grafo.ordenacao_topologica()
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 10:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            grafo.verificar_euleriano()
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 11:  # Nova opção adicionada
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            grafo.verificar_conjuntos()  # Chama a função para verificar conjunto
            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao == 12:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
        else:
            if grafo.eh_planar():
                print("O grafo é planar.")
            else:
                print("O grafo não é planar.")
        input('Para retornar ao menu, pressione enter:')
        escolher_opcao()
    elif opcao == 13:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            while True:
                # Solicita os vértices de início e fim ao usuário
                inicio = input("Digite o vértice inicial: ")
                fim = input("Digite o vértice final: ")

                # Verifica se os vértices existem no grafo
                if inicio not in grafo.vertices or fim not in grafo.vertices:
                    print("Erro: O grafo não possui um ou ambos os vértices inseridos. Por favor, tente novamente.")
                else:
                    # Chama a função caminho_mais_curto com os vértices informados
                    resultado = grafo.caminho_mais_curto(inicio, fim)
                    
                    # Exibe o resultado
                    if isinstance(resultado, tuple):  # Para o caso de grafos ponderados (retorna caminho e custo)
                        caminho, custo = resultado
                        print(f"Caminho mais curto de {inicio} para {fim}: {caminho} com custo: {custo}")
                    else:  # Para grafos não ponderados (retorna apenas o caminho)
                        print(f"Caminho mais curto de {inicio} para {fim}: {resultado}")

                    break  # Sai do loop se os vértices foram válidos

            input('Para retornar ao menu, pressione enter:')
            escolher_opcao()
    elif opcao ==14:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
                vertice_partida_nome = input("Digite o nome do vértice de partida: ")
                if vertice_partida_nome in grafo.vertices:
                    vertice_partida = grafo.vertices.index(vertice_partida_nome)
                    arvore_minima = grafo.arvore_geradora_minima(vertice_partida)
                    if arvore_minima:
                        print("Arestas da árvore geradora mínima:")
                        for aresta in arvore_minima:
                            print(f"Aresta: {grafo.vertices[aresta[0]]} - {grafo.vertices[aresta[1]]} com peso: {grafo.grafo[aresta[0]][aresta[1]]}")
                        time.sleep(1)
                        input('Para retornar ao menu, pressione enter:')
                        escolher_opcao()
                    
                else:
                    print("Erro: Vértice não encontrado.")
                    time.sleep(1)
                    input('Para retornar ao menu, pressione enter:')
                    escolher_opcao()
    elif opcao == 15:
        if grafo is None:
            print("O grafo ainda não foi informado :(. Por favor, selecione a opção 1.")
            escolher_opcao()
        else:
            # Chamar o algoritmo húngaro no grafo
            grafo.aplicar_algoritmo_hungaro()
            input('Pressione enter para voltar ao menu.')
            escolher_opcao()
    else:
        print("Opção inválida :/. Por favor, escolha um número correspondente a uma opção exibida na lista.")
        time.sleep(2)
        escolher_opcao()
