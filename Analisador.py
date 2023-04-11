import os
import json
import pathlib
import re
    

class Analisador:
    def __init__(self, word, frequency):
        self.word = word
        self.frequency = frequency
    
    # Compara dois objetos Analisador com base em sua frequência
    def __lt__(self, other):
        return self.frequency > other.frequency
    
    # Retorna uma string formatada como um objeto JSON com as propriedades "palavra" e "frequencia"
    def __str__(self):
        return f'{{palavra: {self.word}, frequencia: {self.frequency}}}'

if __name__ == "__main__":
   
    # Cria scanner para ler a entrada do usuário
    print("Digite o nome do diretório: ")
    directory = input().strip()
    
    # Obtém o caminho absoluto do diretório informado pelo usuário
    path = str(pathlib.Path.cwd()) + os.sep + directory
    
    # Verifica se o diretório informado pelo usuário existe
    if not os.path.exists(path):
        print("O diretório fornecido não existe.")
        exit()
    
    # Verifica se o diretório informado pelo usuário é válido
    if not os.path.isdir(path):
        print("O caminho fornecido não é um diretório válido.")
        exit()
    
    # Obtém a lista de arquivos .srt do diretório informado pelo usuário
    files = [f for f in os.listdir(path) if f.endswith('.srt')]
    
    if not files:
        print("Não há arquivos .srt no diretório fornecido.")
        exit()
    
    # Cria o diretório "resultados" se ele não existir
    results = pathlib.Path("resultados")
    if not results.exists():
        results.mkdir()
    
    # Processa cada arquivo .srt encontrado no diretório
    for filename in files:
        try:
            # Lê o conteúdo do arquivo
            with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Converte todo o texto para letras minúsculas e remove caracteres especiais
            result = content.lower()
            result = re.sub(r'\b(-->)\b|[<>]|[1234567890.:;?!@#$%&♪_\'\",-]+', '', result)
            
            # Separa as palavras em um array e conta a frequência de cada uma
            words = result.split()
            count = {}
            for word in words:
                count[word] = count.get(word, 0) + 1
            
            # Converte o resultado em um array de Analisador 
            final_result = [Analisador(word, frequency) for word, frequency in count.items()]
            
            # Ordena pelo número de ocorrências
            final_result.sort()
            
            # Converte o array para JSON
            json_str = json.dumps(final_result, indent='\t', default=str)
            
            # Escreve o resultado em um arquivo JSON
            with open(results / f"{filename}.json", 'w', encoding='utf-8') as file:
                file.write(json_str)
        except IOError as e:
            # Imprime mensagem de erro caso ocorra uma exceção ao escrever o arquivo
            print(e)


