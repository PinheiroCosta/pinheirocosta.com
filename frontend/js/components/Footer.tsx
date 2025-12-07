import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import { FaGithub, FaInstagram, FaLinkedin } from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="mt-5 py-4">
      <Container>
        <Row xs="auto" className="justify-content-center mb-2">
          {/* Links para redes sociais */}
          <Col >
            <a
              href="https://www.github.com/pinheirocosta"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dark mx-2"
              aria-label="Github de Rômulo Pinheiro Costa"
            >
              <FaGithub size={24} className="icon-social" />
            </a>
          </Col>
          <Col >
            <a
              href="https://www.instagram.com/rompinheiro"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dark mx-2"
              aria-label="Instagram de Rômulo Pinheiro Costa"
            >
              <FaInstagram size={24} className="icon-social" />
            </a>
          </Col>
          <Col >
            <a
              href="https://www.linkedin.com/in/pinheirocosta"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dark mx-2"
              aria-label="LinkedIn de Rômulo Pinheiro Costa"
            >
              <FaLinkedin size={24} className="icon-social" />
            </a>
          </Col>
        </Row>
        {/* Texto do footer */}
        <Row className="footer-text">
          <Col className="text-center">
            <small className="text-muted">
              © {new Date().getFullYear()} PinheiroCosta.
              Todos os direitos reservados.
            </small>
          </Col>
        </Row>
        <Row className="footer-text">
          <Col className="text-center">
            <small className="text-muted">
             Ao utilizar este site, você concorda com nossa{" "}
              <a href="/privacidade" className="text-decoration-underline">
                 Política de Privacidade
              </a>.
            </small>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;

