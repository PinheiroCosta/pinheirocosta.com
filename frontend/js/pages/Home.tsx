import React, { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import Motd from "../components/Motd";
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
    <Container className="p-4" style={{ maxWidth: 960 }}>
    <Motd />
      <Row className="justify-content-center mb-4">
        {/* Última publicação */}
        <Col md={6} className="d-flex mb-3">
            <LatestArticle />
        </Col>
        <Col md={6} className="d-flex mb-3">
            <RandomToolCard />
        </Col>
      </Row>
    </Container>
  );
};

export default Home;
