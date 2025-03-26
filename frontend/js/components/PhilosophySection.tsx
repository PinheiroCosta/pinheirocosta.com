import React from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import { FaCodeBranch } from "react-icons/fa";

const PhilosophySection = () => {
  return (
    <section className="philosophy-section mb-5 text-center">
      <Container>
        <Row className="">
          <Col md={5} className="mb-5">
            <FaCodeBranch size={80} className="icon-code-branch" />
          </Col>
          <Col md={6} >
            <h5 className="mb-3 lead text-start philosophy-section-title">Compartilhar é crescer.</h5>
            <p className="fs-6 lh-1 text-muted text-start"><strong>Acreditar</strong> no poder da colaboração transforma ideias em realidade.</p>
            <p className="fs-6 lh-1 text-muted text-start"><strong>Aprender</strong> com a comunidade abre portas para o crescimento.</p>
            <p className="fs-6 lh-1 text-muted text-start"><strong>Compartilhar</strong> o que criamos, é semear um futuro melhor.</p>
          </Col>
        </Row>
      </Container>
    </section>
  );
};

export default PhilosophySection;

