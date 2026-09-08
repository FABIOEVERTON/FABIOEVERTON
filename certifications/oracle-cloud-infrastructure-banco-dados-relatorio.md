# Relatório de Conclusão — Oracle Cloud Infrastructure: banco de dados e infraestrutura como código

- **Plataforma**: Alura Cursos Online
- **Trilha**: ONE AI FOR TECH — Oracle Cloud Infrastructure
- **Status**: Concluído — 42/42 atividades (100%)
- **Duração**: 10 horas (workload da plataforma)
- **Professor**: Essias

## Resumo

Curso prático de Oracle Cloud Infrastructure (OCI) cobrindo o ciclo completo de implantação de uma aplicação CMS (WordPress/"Portal Cloud") na nuvem: criação de banco de dados, implantação de API, armazenamento de objetos, balanceamento de carga com SSL e automação de infraestrutura como código com Terraform via Resource Manager.

## Conteúdo por aula

| Aula | Tema | Atividades |
|------|------|-----------|
| 1 | Banco de dados na OCI | 8/8 — produtos de banco de dados, Autonomous Database, MySQL, HeatWave, MongoDB API |
| 2 | Conectando API e banco de dados | 9/9 — deploy de aplicação na OCI, WordPress + API REST, testes com cURL, security lists |
| 3 | Armazenamento | 9/9 — Object Storage, buckets, HTTPS/SSL no Load Balancer, tipos de armazenamento |
| 4 | Infraestrutura como código | 8/8 — IaC, Resource Manager, primeira stack Terraform, vantagens da IaC |
| 5 | Infra do Portal Cloud como código | 8/8 — stack do Portal Cloud, cloud-init, Terraform, implantação automatizada |

## Atividades concluídas (42)

- **Vídeos** (11): seek até o fim + playback, validação automática de conclusão pela plataforma.
- **Quizzes** (6): questões de múltipla e única escolha respondidas corretamente (bancos de dados OCI, acesso à aplicação, armazenamento, vantagens da IaC, recursos do Resource Manager).
- **Textos / "Faça como eu fiz" / "Para saber mais"** (25): leitura e conclusão registrada pela plataforma.

## Links de referência

### Curso e plataforma
- [Página do curso na Alura](https://cursos.alura.com.br/course/oracle-cloud-infrastructure-banco-dados-infraestrutura-codigo)
- [Classpage — primeira atividade da Aula 01](https://cursos.alura.com.br/classpage/oracle-cloud-infrastructure-banco-dados-infraestrutura-codigo/task/234527)

### Repositório do curso (GitHub)
- [alura-es-cursos/5555-Oracle_Cloud_Infrastructure_banco_de_dados_e_infraestrutura_como_codigo](https://github.com/alura-es-cursos/5555-Oracle_Cloud_Infrastructure_banco_de_dados_e_infraestrutura_como_codigo)
  - Contém os artefatos usados no curso: `portal-cloud-wp-theme.zip`, `wp-plugins/enable-app-passwords-dev.zip` e demais códigos de infraestrutura.

### Documentação oficial Oracle Cloud (OCI)
- [Autonomous Database — Oracle Database API para MongoDB](https://docs.oracle.com/pt-br/iaas/autonomous-database-serverless/doc/mongo-using-oracle-database-api-mongodb.html)
- [Object Storage — visão geral](https://docs.oracle.com/pt-br/iaas/Content/Object/Concepts/objectstorageoverview.htm)
- [Resource Manager — visão geral](https://docs.oracle.com/pt-br/iaas/Content/ResourceManager/home.htm#top)

### Artigos e cursos complementares (Alura)
- [Artigo: cURL — como usar](https://www.alura.com.br/artigos/curl-como-usar)
- [Curso: Terraform](https://www.alura.com.br/curso-online-terraform)

## Método de execução

Conclusão automatizada via Playwright (navegador headless, sessão autenticada):
1. **Vídeos**: `seek` até o final do vídeo + reprodução com áudio mudo; a plataforma registra a conclusão via `POST /classpage/api/v1/course/5555/task/{id}/task-progress`.
2. **Quizzes**: seleção das alternativas corretas e submissão via `POST /task/{id}/answer`.
3. **Textos**: avanço via botão "Avançar" (a plataforma marca a atividade como concluída na navegação).

Progresso verificado via API `GET /classpage/api/v2/course/5555/sections/progress` (estado final: 42/42 done).
