import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card} from "react-bootstrap";
import PhilosophySection from "../components/PhilosophySection";
import LatestArticle from "../components/LatestArticle";
import RandomToolCard from "../components/RandomToolCard";

import logoMain from "../../assets/images/logo-website.svg";
import { RestService } from "../api/services.gen";

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
          <Card.Header className="text-center mb-2 pb-3 pt-3 fs-5">Novidades</Card.Header>
            <Card.Body>
              <Card.Text className="text-truncate-card">
                Em breve, vou adicionar aqui um feed com as últimas publicações que fiz nas redes.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        {/* Última publicação */}
        <Col md={4} className="d-flex mb-2">
            <LatestArticle />
        </Col>
        <Col md={4} className="d-flex mb-2">
            <RandomToolCard />
        </Col>
      </Row>
    </Container>
  );
};

export default Home;
