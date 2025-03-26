import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import { FaGithub, FaTwitter, FaInstagram, FaLinkedin } from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="mt-5 py-4">
      <Container>
        <Row xs="auto" className="justify-content-center mb-1">
          {/* Links para redes sociais */}
          <Col >
            <a
              href="https://www.github.com/pinheirocosta"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dark mx-2"
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
            >
              <FaLinkedin size={24} className="icon-social" />
            </a>
          </Col>
        </Row>
        {/* Texto do footer */}
        <Row className="footer-text">
          <Col className="text-center mt-2">
            <small className="text-muted">
              &copy; {new Date().getFullYear()} PinheiroCosta. 
              Todos os direitos reservados.
            </small>
          </Col>
        </Row>
        <Row className="footer-text">
          <Col className="text-center">
            <small className="text-muted">
              Desenvolvido com o 
              <a href="https://github.com/vintasoftware/django-react-boilerplate" target="_blank" rel="noopener noreferrer"> boilerplate da Vinta</a>.
            </small>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;

