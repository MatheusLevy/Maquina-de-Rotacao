# @Author: Matheus Levy de Lima Bessa

import argparse
from collections import deque

# Atributos do Rotor
# Passo = é a quantidade de rotações dados, as rotações avanção de 1 em 1 e tem a valor máximo de 25 indo de 0 até 25, ou seja 26 
# Saida = São as letras que ficam a direita do rotor correspondendo  a saida do rotor
# Entrada = São as letras que ficam a esquerda do rotor correspondendo ao alfabeto de entrada
# OBS: Ao executar uma rotação Saida e entradas rodam juntas, pois fazem parte do mesmo rotor.
# OBS2: A saida é informada como parametro na criação do rotor, o que permite escolher uma configuração diferente
#       da fornecida no exercicio. No entanto, a entrada é fixa na criação do objeto.
class Rotor:
    def __init__(self, saida):  #A saida na verdade é um dicionário que representa a combinação de valores e letras
        self.passo = 0          #que gera a saida do rotor
        self.prox = None        #prox é um direcionador para o proximo rotor, funciona como o cabo que liga dois rotores         
        self.saida = saida      #A entrada é todo mapeamento de Letrar para valores. É um dicionário onde cada letra tem seu respectivo valor
        self.entrada = {        #Assim como a saida.
            "A": 1,             
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8,
            "I": 9,
            "J": 10,
            "K": 11,
            "L": 12,
            "M": 13,
            "N": 14,
            "O": 15,
            "P": 16,
            "Q": 17,
            "R": 18,
            "S": 19,
            "T": 20,
            "U": 21,
            "V": 22,
            "W": 23,
            "X": 24,
            "Y": 25,
            "Z": 26
        }
    
    #Mapeia uma letra do lado esquerdo do rotor para um letra do lado direito do rotor
    #@Parametros:
    #letra: Letra que será cifrada baseado na configuração deste cilindro
    def cifrar(self, letra):
        #Busco no meu dicionario de entrada qual o valor da letra recebida
        
        valorEntrada = self.entrada[letra] # Valor da Letra na Entrada Corresponde ao valor da Letra do lado esquerdo do rotor
        for letraSaida, valorSaida in self.saida.items():   #Percorre o dicionário atrás da Letra que tem esse valor na saida, ou seja no lado direito do rotor.
            if valorSaida == valorEntrada:                  
                cifra = letraSaida   #Retorna a letra que foi mapeada com o mesmo valor do lado direito do rotor
        return cifra

    #Mapeia uma letra do lado direito para o lado esquerdo, faz o inverso da cifragem
    #@Parametros:
    #letra: Letra que será decifrada baseada na configuração deste cilindro
    def decifrar(self, letra):          #Busca na ordem inversa da cifragem. Pega o valor na saida e associa a um valor na entrada
        valorSaida = self.saida[letra]
        for letraEntrada, valorEntrada in self.entrada.items():
            if(valorEntrada == valorSaida):
                decifra = letraEntrada
        return decifra

    def passar(self):                   #Passar executa a rotação do cilindro. Quando chegar em 25 rotações ele volta para 0 passos e rotaciona o proximo cilindro 
        self.passo += 1
        if (self.passo > 25):           #Verifica se o valor de passos ultrapassou 25 [0..25] se tiver ultrapassado significa que rodou uma volta completa, ou sejam voltou para o inicio
            self.passo = 0              #Se isso acontecer então setamos os passos para 0 e
            if self.prox is not None:   #verificamos se existe um proximo cilindo ligado a este. Se existe
                self.prox.passar()      #passamos o proximo cilindro
        self.rotar(1)                   #Ao pasasr um cilindro precisamos rotacionar todos os valores dentro do cilindo em 1 grau

    #Função Responsável por rotacionar os valores dentro do cilindro
    # @Parametros:
    # K: Representa o valor da rotação, as funções que chamam rotar estão fixas para passar K=1, ou seja um grau de rotação
    def rotar(self, K):
        list_entrada = list(self.entrada.values()) #Pega os valores das letras de entrada converte em uma lista
        list_entrada = deque(list_entrada)         # Converte a lista de valores em um objeto deque que pode ser facilmente rotacionado
        list_entrada.rotate(K)                     # Rotaciona o deque
        list_entrada = list(list_entrada)          #Converte o deque de volta em umas lista de valores novamente
        i=0                                         
        for letra in self.entrada.keys():          # Colocar os novos valores rotacionados no dicionário de entrada em suas novas posições
            self.entrada[letra] = list_entrada[i]
            i+=1
        #Repetimos o mesmo processo para a saida
        list_saida = list(self.saida.values())
        list_saida = deque(list_saida)
        list_saida.rotate(K)
        list_saida = list(list_saida)
        i=0
        for letra in self.saida.keys():
            self.saida[letra] = list_saida[i]
            i+=1
        

#A maquina de rotação
#Esta possui uma lista de rotores, que é passada como seu construtor.
#Portanto para criar uma máquina de rotação precisamos antes ter criado os rotores.
#Utilizar uma lista de rotores facilita para expadir o número de rotores dentro da máquina, bastando passar mais rotores na lista
class Maquina:
    def __init__(self, rotores):
        self.rotores = rotores #Passamos os rotores para a classe
        self.encadearRotores() #Essa função é responsável por encadear/ligar os rotores entre si, corresponde a ligar fisicamente os cabos dos rotores uns nos outros

    #Função que faz o encadeamento dos rotores, ela liga o rotor inicial ao próximo e assim por diante até o último cilindro     
    def encadearRotores(self):
        for i in range(len(self.rotores)-1):
            if(i < len(self.rotores)-1):
                self.rotores[i].prox = self.rotores[i+1]

    #Função de cifragem da máquina
    #@Parametros:
    #Texto: Texto a ser cifrado
    def cifrar(self, Texto):
        TextoCifrado = ""
        i=0
        for letra in Texto:        #Percorre o texto letra a letra
            if(letra != ' '):      #pulando os espaços em branco
                for i in range(len(self.rotores)):              #Aqui percorremos os rotores pegando passando a letra na entrada do primeiro cilindro
                    letra = self.rotores[i].cifrar(letra)       #pegando a saida do primeiro cilindro e passando como entrada para o segundo cilindro e assim por diante até o último cilindro
                self.rotores[0].passar()  #-------              #Após terminar de cifrar uma letra passando por todos os rotores devemos executar o passo no primeiro rotor
                TextoCifrado+=letra       #   |                  #Concatenamos a letra cifrada no fim da nossa cadeia de caracteres de TextoCifrado
            else:                         #   |_> Chamamos a função cifrar do rotor aqui e não da maquina                  
                TextoCifrado+=letra
        return TextoCifrado


    #Função de Decifrar da Máquina
    #@Parametros
    #Texto: Texto Cifrado que irá ser Decifrado
    #ConfigInicial: Uma lista de rotores na configuração inical da máquina
    @staticmethod
    def decifrar( Texto, ConfigInicial):
        maquina_inversa = Maquina(ConfigInicial) #Primeiramente criamos uma máquina com a configuração inicial 
        TextoDecifrado = ""
        i = len(maquina_inversa.rotores)-1       #Pegamos a quantidade de rotores/cilindros da máquina
        for letra in Texto:                      #Iremos percorrer o texto cifrado letra a letra
            if(letra != ' '):                    #pulando os espaços
                for j in range(i, -1, -1):       #Percorreremos os rotores na ordem inversa, do último até o primeiro
                    letra = maquina_inversa.rotores[j].decifrar(letra) #Dessa vez usaremos a função decifra dos rotores
                maquina_inversa.rotores[0].passar()   #Após decifrar a letra iremos passar o primeiro rotor
                TextoDecifrado += letra
            else:
                TextoDecifrado += letra
        return TextoDecifrado


#Definição das Chaves da Máquina e das Configuraçõees Iniciais da Máquina
#Corresponde aos valores da direita do cilindro
#Chave Cilindro 1
chaveR1 ={
            "A": 4,
            "B": 5,
            "C": 10,
            "D": 1,
            "E": 11,
            "F": 15,
            "G": 2,
            "H": 6,
            "I": 17,
            "J": 20,
            "K": 16,
            "L": 8,
            "M": 21,
            "N": 7,
            "O": 23,
            "P": 25,
            "Q": 12,
            "R": 22,
            "S": 13,
            "T": 24,
            "U": 9,
            "V": 18,
            "W": 3,
            "X": 19,
            "Y": 26,
            "Z": 14
}
#Chave Cilindro 2
chaveR2 ={
            "A": 23,
            "B": 4,
            "C": 14,
            "D": 17,
            "E": 6,
            "F": 3,
            "G": 2,
            "H": 21,
            "I": 24,
            "J": 8,
            "K": 20,
            "L": 9,
            "M": 13,
            "N": 10,
            "O": 11,
            "P": 18,
            "Q": 25,
            "R": 1,
            "S": 16,
            "T": 19,
            "U": 15,
            "V": 22,
            "W": 7,
            "X": 5,
            "Y": 12,
            "Z": 26
}
#Chave Cilindro 3
chaveR3 ={
            "A": 20,
            "B": 17,
            "C": 15,
            "D": 3,
            "E": 5,
            "F": 4,
            "G": 13,
            "H": 18,
            "I": 22,
            "J": 24,
            "K": 6,
            "L": 9,
            "M": 12,
            "N": 8,
            "O": 1,
            "P": 25,
            "Q": 19,
            "R": 11,
            "S": 2,
            "T": 16,
            "U": 10,
            "V": 21,
            "W": 14,
            "X": 26,
            "Y": 7,
            "Z": 23
}

#Definindo as configurações Iniciais
#Configuração do Cilindro 1
ConfigInicalR1 =   {
            "A": 4,
            "B": 5,
            "C": 10,
            "D": 1,
            "E": 11,
            "F": 15,
            "G": 2,
            "H": 6,
            "I": 17,
            "J": 20,
            "K": 16,
            "L": 8,
            "M": 21,
            "N": 7,
            "O": 23,
            "P": 25,
            "Q": 12,
            "R": 22,
            "S": 13,
            "T": 24,
            "U": 9,
            "V": 18,
            "W": 3,
            "X": 19,
            "Y": 26,
            "Z": 14
}
#Configuração do Cilindro 2
ConfigInicalR2 = {
            "A": 23,
            "B": 4,
            "C": 14,
            "D": 17,
            "E": 6,
            "F": 3,
            "G": 2,
            "H": 21,
            "I": 24,
            "J": 8,
            "K": 20,
            "L": 9,
            "M": 13,
            "N": 10,
            "O": 11,
            "P": 18,
            "Q": 25,
            "R": 1,
            "S": 16,
            "T": 19,
            "U": 15,
            "V": 22,
            "W": 7,
            "X": 5,
            "Y": 12,
            "Z": 26
}
#Configuração Cilindro 3
ConfigInicalR3 = {
            "A": 20,
            "B": 17,
            "C": 15,
            "D": 3,
            "E": 5,
            "F": 4,
            "G": 13,
            "H": 18,
            "I": 22,
            "J": 24,
            "K": 6,
            "L": 9,
            "M": 12,
            "N": 8,
            "O": 1,
            "P": 25,
            "Q": 19,
            "R": 11,
            "S": 2,
            "T": 16,
            "U": 10,
            "V": 21,
            "W": 14,
            "X": 26,
            "Y": 7,
            "Z": 23
}

#Criando os rotores da maquina de cifragem
R1 = Rotor(chaveR1)
R2 = Rotor(chaveR2)
R3 = Rotor(chaveR3)
#Criando os rotores da maquina de decifragem
RI1 = Rotor(ConfigInicalR1)
RI2 = Rotor(ConfigInicalR2)
RI3 = Rotor(ConfigInicalR3)

# Argumentos do Programa
# -c para cifrar o arquivo claro.txt
# -d para decifrar o arquivo cifrado.txt
# -h para ajuda

#   Valores de const
#   1 - Cifrar
#   2 - Decifrar

#Criando o parse de argumentos
parser = argparse.ArgumentParser()
parser.add_argument("-c", help="Cifra o arquivo claro.txt", action="store_const", const=1, dest='opcao') 
parser.add_argument("-d", help="Decifra o arquivo cifrado.txt", action="store_const", const=2, dest='opcao')
argumento = parser.parse_args()
#definindo variaveis globais para representar os argumentos
cifrar = False
decifrar = False

#Verificando se o usuário colocou um argumento -c ou -d para cifrar ou decifrar, caso não exibe a tela de ajuda
if(argumento.opcao == None):
    print(parser.parse_args(['-h'])) #Exibe ajuda
    exit()    #Finaliza o programa
elif argumento.opcao == 1:          
    cifrar = True                   #Defino Variaveis Boolean para saber se a operação é de cifrar ou decifrar
else:                               #Não é necessario, mas é mais facil de entender tendo um boolean cifrar e um decifrar
    decifrar = True                 #doque ficar lembrando o que é argumento.opcao == 1 ou argumento.opcao == 2



#Função de leitura do arquivo
#@Parametros:
#ArquivoNome: Nome do arquivo para ser aberto, deve estar dentro do diretorio do programa
def LerArquivo(ArquivoNome):
    arquivo = open(ArquivoNome) #Abre o arquivo 
    Texto = ""                  
    linhas = arquivo.readlines()    #Lê linha a linha e concatena tudo em uma String única
    for linha in linhas:
        Texto += linha
    return Texto

#Verifica se o usuário escolheu cifrar ou decifrar
if cifrar:
    Texto = LerArquivo("claro.txt") #Lê o conteudo do arquivo claro.txt
    m1 = Maquina([R1,R2, R3])       #Cria a máquina a partir dos Rotores R1, R2, R3
    cifrado = m1.cifrar(Texto.upper()) #Chama a função de cifragem da maquina
    cifradotxt = open(r"cifrado.txt","w+")  #Abre o arquivo cifrado.txt
    cifradotxt.write(cifrado)               #Escreve o resultado no arquivo cifrado.txt    
else:
    Texto = LerArquivo("cifrado.txt")  #Lê o conteudo do arquivo cifrado.txt
    decifrado = Maquina.decifrar(Texto, [RI1, RI2, RI3] ) # Utiliza o metodo estatico da classe Maquina para decifrar o texto e passa a configuração Inical dos rotores
    decifradotxt = open(r"decifrado.txt", "w+") #Abre o arquivo decifrado.txt
    decifradotxt.write(decifrado)   #Escreve o resutlado no arquivo decifrado.txt