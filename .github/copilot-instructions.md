## Segurança

- Valide as práticas de higienização de entradas (*input sanitization*).
- Busque por riscos que possam expor dados de usuários.
- Dê preferência ao carregamento de configurações e conteúdo a partir do banco de dados, em vez de conteúdo fixo no código (*hard-coded*). Se for absolutamente necessário, carregue-os a partir de variáveis ​​de ambiente ou de um arquivo de configuração não versionado.

## Qualidade de Código

- Utilize convenções de nomenclatura consistentes.
- Tente reduzir a duplicação de código.
- Priorize a manutenibilidade e a legibilidade em detrimento da otimização.
- Se um método for muito utilizado, tente otimizá-lo para melhorar o desempenho.
- Priorize o tratamento explícito de erros em vez de falhas silenciosas.