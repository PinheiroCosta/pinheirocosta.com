import React from "react";
import { Container } from "react-bootstrap";

const PrivacyPolicy: React.FC = () => {
  return (
    <Container className="py-5">
      <h1 className="mb-4">Política de Privacidade</h1>

      <p>
        Este site respeita a sua privacidade. Abaixo explicamos de forma
        objetiva quais dados podem ser coletados e como são utilizados.
      </p>

      <h4 className="mt-4">1. Coleta e uso de dados</h4>
      <ul>
        <li>
          Ao utilizar ferramentas disponibilizadas neste site, os dados
          inseridos pelo usuário são enviados aos nossos servidores apenas para
          processamento e resposta. Nenhuma informação é armazenada após a
          conclusão da operação.
        </li>
        <li>
          Não utilizamos cookies para rastreamento ou fins de marketing.
        </li>
        <li>
          Podemos coletar e registrar endereços IP de forma automática para
          fins de segurança, como controle de abusos e bloqueio temporário em
          caso de uso excessivo ou malicioso.
        </li>
      </ul>

      <h4 className="mt-4">2. Compartilhamento de dados</h4>
      <ul>
        <li>Nenhum dado é compartilhado com terceiros.</li>
      </ul>

      <h4 className="mt-4">3. Armazenamento</h4>
      <ul>
        <li>
          Os dados fornecidos são processados temporariamente apenas durante o
          uso das ferramentas. Não são armazenados em banco de dados.
        </li>
        <li>
          Logs de IP e uso podem ser mantidos por tempo limitado para fins de
          auditoria e segurança.
        </li>
      </ul>

      <h4 className="mt-4">4. Formulário de contato</h4>
      <ul>
        <li>
          Quando você entrar em contato conosco via formulário (quando
          disponível), seu nome e e-mail serão utilizados exclusivamente para
          retorno do contato.
        </li>
        <li>
          Você pode solicitar a exclusão de seus dados a qualquer momento.
        </li>
      </ul>

      <h4 className="mt-4">5. Seus direitos</h4>
      <p>
        Nos termos da Lei Geral de Proteção de Dados (Lei 13.709/18), você tem
        o direito de acessar, corrigir ou excluir seus dados pessoais. Para
        exercer esses direitos, entre em contato conosco pela página{" "}
        <a href="/sobre">Sobre Mim</a>.
      </p>
    </Container>
  );
};

export default PrivacyPolicy;
