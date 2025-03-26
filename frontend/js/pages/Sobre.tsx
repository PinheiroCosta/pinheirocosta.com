import React, { useState, useEffect } from "react";
import { Container, Row, Col, Image, Card } from "react-bootstrap";
import axios from "axios";
import AtualizarIdade from "../components/AtualizarIdade";


const Sobre = () => {
  const [aboutMeData, setAboutMeData] = useState<any>(null);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

  useEffect(() => {
    async function fetchAboutMe() {
      try {
        const response = await axios.get(`${API_URL}/aboutme/`);
        setAboutMeData(response.data.results[0]);
      } catch (error) {
        console.error("Erro ao buscar informações do dono do site:", error);
      }
    }

    fetchAboutMe();
  }, []);

  return (
    <Container>
      <Row className="justify-content-center align-items-center">
      {aboutMeData && aboutMeData.about_image && (
        <Col md={3} className="text-center mb-2">
            <Image
              src={aboutMeData.about_image}
              roundedCircle
              fluid
              className="shadow-lg"
              alt="Foto do dono do site"
            />
        </Col>
      )}
        <Col md={6}>
          <Card className="p-4 shadow">
            <Card.Body>
              <Card.Title className="text-center mb-3">
                <h2>Sobre Mim</h2>
              </Card.Title>
              <Card.Text 
                className="text-justify"
                dangerouslySetInnerHTML={{
                   __html: aboutMeData ? aboutMeData.about_text : "<p>Carregando...</p>" 
                }}>
                
              </Card.Text>
              {aboutMeData && aboutMeData.social_links && (
                <div className="social-links">
                  {Object.entries(aboutMeData.social_links).map(([platform, link]) => (
                    <a key={platform} href={link as string | undefined} target="_blank" rel="noopener noreferrer">
                      {platform}
                    </a>
                  ))}
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    <AtualizarIdade />
    </Container>
  );
};

export default Sobre;

