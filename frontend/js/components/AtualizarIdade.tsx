import { useEffect } from "react";

const AtualizarIdade = () => {
  useEffect(() => {
    const atualizarIdade = () => {
      const spanIdade = document.getElementById("idade");
      if (!spanIdade) return;

      const dataNascimento = new Date(1987, 10, 10); // Ano, Mês (0 = Janeiro), Dia
      const hoje = new Date();

      let idade = hoje.getFullYear() - dataNascimento.getFullYear();
      const aniversarioAindaNaoPassou =
        hoje.getMonth() < dataNascimento.getMonth() ||
        (hoje.getMonth() === dataNascimento.getMonth() && hoje.getDate() < dataNascimento.getDate());

      if (aniversarioAindaNaoPassou) {
        idade--; // Reduz a idade se ainda não fez aniversário este ano
      }

      spanIdade.textContent = idade.toString();
    };

    // Função para observar alterações no DOM
    const observer = new MutationObserver(() => {
      atualizarIdade(); // Atualiza a idade sempre que o conteúdo for alterado
    });

    // Alvo a ser observado
    const container = document.getElementById("sobre-mim-container");
    if (container) {
      observer.observe(container, {
        childList: true, // Observa a adição/remoção de elementos
        subtree: true, // Observa em todos os níveis do DOM
      });
    }

    // Executa a primeira atualização ao carregar
    setTimeout(atualizarIdade, 300);

    return () => {
      if (container) observer.disconnect();
    };
  }, []);

  return null;
};

export default AtualizarIdade;

