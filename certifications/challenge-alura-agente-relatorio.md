# Relatório — Challenge Alura Agente (RAG ONE BR)

- **Plataforma**: Alura Cursos Online
- **Trilha**: ONE AI FOR TECH
- **Curso**: Challenge Alura Agente
- **Professor**: Eric Monné Fraga de Oliveira
- **Código**: `challenge-rag`
- **Status**: Acessado e documentado — 0/6 atividades concluídas (construção do desafio pendente)
- **Carga horária**: 8 horas (workload da plataforma)

## Visão geral do desafio

O **Challenge Alura Agente** é o desafio prático final da trilha ONE AI FOR TECH. O cenário: você foi contratado por uma empresa (fintech, consultoria, startup) que possui tonelhas de documentos internos (manuais, relatórios, políticas, planilhas) e os colaboradores perdem horas procurando informação. A solução pedida é um **agente de IA (RAG — Retrieval Augmented Generation)** que responda perguntas em linguagem natural com base no conteúdo dos documentos, sem abrir cada arquivo.

O desafio possui 3 etapas principais:
1. **Documento**: escolher um documento (PDF ou CSV) e criar código que lê e processa o arquivo.
2. **Agente**: construir um agente de IA que responde perguntas sobre o documento (ex.: "qual foi o produto mais vendido em dezembro de 2015?").
3. **Deploy**: publicar o agente na nuvem **OCI (Oracle Cloud Infrastructure)** — aplicação acessível publicamente, provando o deploy funcionando.

### Tecnologias sugeridas (não obrigatórias)
- **Linguagem**: Python
- **Framework**: LangChain (montar o agente)
- **Leitura de documentos**: PyPDF ou Pandas
- **Modelo de linguagem**: Gemini, ChatGPT, Cohere, Claude, ou outro
- **Deploy**: OCI Compute

### Dicas do professor
1. Comece pelo agente **local**, só depois faça o deploy.
2. Use **Google Colab** para prototipar (grátis, Python já configurado).
3. Não foque em interface bonita — o valor está no agente funcionando.

## Estrutura do curso

### Aula 01 — Challenge Alura Agente (0/2)
1. **RAG ONE BR** (07 min, vídeo) — apresentação do desafio (transcrição abaixo).
2. **Trello do Desafio** — quadro do desafio para organização e gestão de tarefas. Criar cópia do template pelo menu "3 pontos" → "Copiar quadro".

### Aula 02 — Construa seu Alura Agente (0/2)
1. **Cria sua documentação** — gerar a documentação que servirá de base para o agente. Sugestões por segmento:
   - Loja Online / E-commerce: política de privacidade, reembolso e devoluções, FAQ, guia de envios, termos e condições.
   - SaaS / Plataforma Digital: base de conhecimento, FAQ de suporte, planos e preços, termos de uso.
   - Logística / Envios: política de envios, rastreamento, reembolsos, reclamações.
   - Clínica de Saúde: privacidade de dados do paciente, agendamentos, cancelamentos, convênios.
   - Plataforma Educativa: regulamento do estudante, reembolso de matrículas, FAQ de cursos e certificados.
   - Fintech / Banco Digital: privacidade e proteção de dados, termos de uso, segurança e fraudes, tarifas.
   - O projeto é livre — pode-se usar qualquer documento (PDF ou CSV) que resolva um problema real.
2. **Opções de documentação** — exemplos prontos de documentação (PDFs) para download:
   - **Santos Pegasus Soluciones** (5 PDFs): guia de engenharia back-end, onboarding de devs, arquitetura de microsserviços, engenharia front-end, resiliência e resposta a incidentes.
   - **BimBam Buy** (5 PDFs): FAQ de métodos de pagamento, manual de garantia, guia de envios, programa de afiliados, política de reembolsos.
   - **Mercado Central 24h** (5 PDFs): política de atendimento/trocas, manual de fornecedores, regulamento interno, FAQ de clientes e funcionários.

### Aula 03 — Entrega do Challenge (0/2)
1. **Entregáveis do projeto**:
   - **Repositório público no GitHub** com código-fonte, histórico de commits e estrutura organizada.
   - **README** com: descrição do projeto, arquitetura, tecnologias, instruções de execução, exemplos de perguntas e de respostas.
   - **Agente funcional**: IA que responde perguntas baseadas em um PDF ou CSV (código que lê e processa o documento).
   - **Evidência do deploy na OCI**: link público da aplicação funcionando e/ou print da execução.
2. **Entrega do Projeto** — formulário de submissão:
   - Aceita **apenas URLs do GitHub**.
   - Baixar a **badge** após enviar e compartilhar no LinkedIn com **#Alura** e **#oraclenexteducation**.
   - **5 tentativas** de envio.

## Transcrição do vídeo "RAG ONE BR"

> "E aí pessoal. Meu nome é Eric Monné, e para fins de acessibilidade eu vou me auto-descrever. [...] Hoje eu vou te apresentar o challenge final, é o Alura Agente, que é o nosso desafio prático que vai reunir tudo o que você aprendeu até agora em um único projeto real. [...] você foi contratado por uma empresa [...] essa empresa tem toneladas de documentos internos [...] as pessoas passam horas procurando informação dentro desses arquivos [...] eles querem um agente de inteligência artificial que qualquer colaborador possa usar para fazer perguntas e receber respostas diretas em linguagem natural, sem precisar abrir nenhum documento.
>
> O desafio possui três partes principais: primeiro, você vai escolher um documento (PDF ou CSV) e criar um código que lê e processa esse arquivo. Segundo, você vai construir um agente de IA que consegue responder perguntas sobre esse documento. Terceiro, o grande diferencial: você vai fazer o deploy desse agente na nuvem na Oracle, a OCI, ou seja, a sua aplicação vai sair do seu computador e vai estar acessível publicamente, rodando de verdade na nuvem.
>
> As tecnologias sugeridas: Python, LangChain, PyPDF ou Pandas, e o modelo de linguagem (Gemini, ChatGPT, Cohere, Claude ou outro). Para o deploy a sugestão é o OCI Compute. São apenas sugestões — o importante é que a solução funcione.
>
> Para a aprovação vamos olhar se a aplicação funciona, se o código está organizado, e se o README explica bem o que foi feito e conta com uma demonstração do funcionamento. Três dicas: comece sempre pelo agente local; use o Google Colab para prototipar; não fique preso tentando fazer uma interface bonita. O projeto é seu, você pode personalizá-lo como quiser. Boa sorte e até mais."

## Links de referência

### Quadro do desafio (Trello)
- [Trello — Challenge AluraAgente ONE IA For Tech PT-BR](https://trello.com/b/IhB0NmMm/challenge-aluraagente-one-ia-for-tech-pt-br)
- [Trello (criar conta)](https://trello.com/)

### Documentação de exemplo (PDFs — CDN do curso)
Santos Pegasus Soluciones (desenvolvimento de software, microsserviços, RAG, OCI):
- [Santo Pegasus — Guia Oficial de Engenharia Back-end (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/443c88aa-deb6-4176-a00d-42ffcda3bd75.pdf)
- [Santo Pegasus — Manual de Onboarding para Desenvolvedores (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/af97c364-962e-4fb6-ab0b-7916857cbcd8.pdf)
- [Santo Pegasus — Arquitetura de Microsserviços e Mapa de Domínios (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/d0aeb4ee-cd16-4567-a469-0ba517a6260b.pdf)
- [Santo Pegasus — Guia Oficial de Engenharia Front-end (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/595e8e15-e730-47b0-9be9-8c6bd4613d80.pdf)
- [Santo Pegasus — Manual Maestro de Resiliência e Resposta a Incidentes v7.0 (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/53bc95ef-1ba9-477e-99d8-f71131bc2838.pdf)

BimBam Buy (e-commerce multiplataforma):
- [BimBam Buy — FAQ Métodos de Pagamento (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/7ebe3573-4469-40f6-86a2-05202fe07263.pdf)
- [BimBam Buy — Manual de Garantia (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/25e9efae-7a6b-4fca-adca-e33c6ad2edfe.pdf)
- [BimBam Buy — Guia de Envios (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/abba086c-9098-4450-9fff-97abe8037f4d.pdf)
- [BimBam Buy — Programa de Afiliados (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/036e7b2e-c962-4c5a-aa2b-50d92d97d65b.pdf)
- [BimBam Buy — Política de Reembolsos e Devoluções (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/5ceb0972-62c4-4825-9364-fd21477df4e1.pdf)

Mercado Central 24h (supermercado 24/7):
- [Mercado Central 24h — Política de Atendimento, Trocas e Devoluções (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/52396afd-6b6b-40b9-9b0b-ccab8f068b98.pdf)
- [Mercado Central 24h — Manual de Fornecedores e Política de Compras (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/4004dbe0-3589-4b44-bb97-ab605f22ad37.pdf)
- [Mercado Central 24h — Regulamento Interno e Procedimentos Operacionais (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/3948104b-f5ed-4825-b8af-b1b107eb4fd9.pdf)
- [Mercado Central 24h — FAQ Clientes e Funcionários (PT-BR)](https://cdn1.gnarususercontent.com.br/documents/1/internal/422750d7-8191-43da-a4e7-480d6f0fde40.pdf)

### Entrega
- Link de entrega do projeto (aceita apenas URLs do GitHub): a definir com o repositório do projeto.
- Badge: baixar após envio e compartilhar com **#Alura** e **#oraclenexteducation**.

## Próximos passos

1. Definir o segmento/empresa e escolher o documento (PDF/CSV) de base.
2. Construir o agente local (Python + LangChain + Gemini/Claude) no Google Colab.
3. Criar repositório público no GitHub com README completo.
4. Deploy na OCI (OCI Compute) e evidência de funcionamento.
5. Submeter URL no formulário de entrega e compartilhar a badge no LinkedIn.
