import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card} from "react-bootstrap";
import PhilosophySection from "../components/PhilosophySection";
import LatestArticle from "../components/LatestArticle";

import logoMain from "../../assets/images/logo-website.svg";
import { RestService } from "../api";

const Home = () => {
  const [restCheck, setRestCheck] =
    useState<Awaited<ReturnType<typeof RestService.restRestCheckRetrieve>>>();

  useEffect(() => {
    async function onFetchRestCheck() {
      try {
        const result = await RestService.restRestCheckRetrieve();
        setRestCheck(result);
      } catch (error) {
        console.error("Erro ao buscar dados da API:", error);
      }
    }
    onFetchRestCheck();
  }, []);

  return (
    <Container className="p-4">
    <PhilosophySection />
      <Row className="justify-content-center">
        <Col md={4} className="d-flex mb-2">
          <Card className="text-start ">
            <Card.Body>
              <Card.Header className="text-center fs-5">Novidades</Card.Header>
              <Card.Text className="text-truncate-card">
                Em breve, vou adicionar aqui um feed com as últimas publicações que fiz nas redes. Como vou integrar isso de forma segura?
                Ainda não faço ideia, mas vou pensar num jeito. 
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        {/* Última publicação */}
        <Col md={4} className="d-flex mb-2">
            <LatestArticle />
        </Col>
        <Col md={4} className="d-flex mb-2">
          <Card className="text-start ">
            <Card.Body>
              <Card.Header className="text-center fs-5">Ferramentas</Card.Header>
              <Card.Text>
                Este card será dedicado à uma das ferramentas que disponibilizarei de forma gratuita nesse site. 
                A ideia é exibir uma ferramenta aleatoria que ta no repositório com uma breve descrição do que ela faz, e como
                utilizar.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Home;
