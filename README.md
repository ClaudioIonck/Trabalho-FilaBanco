## Trabalho Univille - Fila de Banco

### Título
Fila de Banco

### Descrição
Este projeto é uma simulação da fila de atendimento em um banco durante seu horário de pico, das 11:00 às 13:00. O objetivo é determinar o número ideal de atendentes de caixa para que cada cliente não espere mais de 2 minutos na fila antes de ser atendido.

### Contexto
O banco Firmeza Investimentos deseja otimizar o número de atendentes de caixa durante o horário de maior fluxo de clientes. A simulação ajudará a entender melhor a dinâmica das filas e a eficiência dos atendentes.

### Instruções do Projeto
Os clientes chegam ao banco em intervalos variando entre 5 e 50 segundos. Cada cliente é atendido pelo caixa em um período que varia entre 30 segundos e 120 segundos. A simulação deve ser realizada utilizando conceitos de programação concorrente para modelar o fluxo de clientes e o processo de atendimento.

### Objetivos da Simulação
- **Determinar o número ideal de atendentes de caixa** para que nenhum cliente espere mais de 2 minutos na fila.
- **Analisar e gerar estatísticas sobre o atendimento**, incluindo:
  - Quantidade de clientes atendidos durante o período simulado.
  - Tempo máximo de espera na fila.
  - Tempo máximo de atendimento por um caixa.
  - Tempo médio de permanência de um cliente no banco (desde a chegada até a saída).
  - Tempo médio de espera na fila.

### Como Rodar a Simulação
1. **Instalação das Dependências**:
   - Certifique-se de que Python 3.8 ou superior está instalado em seu sistema.
   - Instale as bibliotecas necessárias utilizando o comando:
     ```bash
     pip install -r requirements.txt
     ```

2. **Execução**:
   - Execute o script principal da simulação com o comando:
     ```bash
     python main.py
     ```

3. **Visualização de Resultados**:
   - Após a execução, os resultados serão exibidos no terminal. Verifique se os tempos médios e máximos estão dentro das expectativas e se o objetivo de tempo de espera máximo de 2 minutos é alcançado.

### Tecnologias Utilizadas
- **Python**: Linguagem de programação usada para desenvolver a simulação.
- **Threading ou asyncio**: Bibliotecas de Python utilizadas para programação concorrente.

### Autores
- [Claudio L. Defrein Ionck](https://github.com/ClaudioIonck)
- [Gabriel P. Hames de Souza](https://github.com/Hammes01)
