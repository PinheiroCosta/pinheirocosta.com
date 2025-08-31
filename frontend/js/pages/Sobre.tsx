import React, { useState, useEffect } from "react";
import { Container, Row, Col, Image, Card } from "react-bootstrap";
import ContactForm from "../components/ContactForm";
import { AboutmeService, ParametrosService } from "../api/services.gen";
import BuyMeACoffee from "../components/BuyMeACoffeeButton";
import { GoogleReCaptchaProvider } from 'react-google-recaptcha-v3';
import { FaGithub, FaInstagram, FaLinkedin, FaGlobe } from "react-icons/fa";
import type { AboutmeListResponse, AboutMe } from "../api/types.gen";

const Sobre = () => {
  const [aboutMeData, setAboutMeData] = useState<AboutMe | null>(null);
  const [siteKey, setSiteKey] = useState<string | null>(null);
  const [captchaError, setCaptchaError] = useState<string | null>(null);

  const socialIconMap: Record<string, JSX.Element> = {
    Github: <FaGithub size={34} />,
    Instagram: <FaInstagram size={34} />,
    Linkedin: <FaLinkedin size={34} />,
    Website: <FaGlobe size={34} />,
  };

  useEffect(() => {
    AboutmeService.aboutmeList().then((res) => {
      setAboutMeData(res[0] || null);
    });

    ParametrosService.parametrosRetrievePorChave({ chave: "RECAPTCHA_SITE_KEY" })
      .then((res) => setSiteKey(res.valor))
      .catch(() => setCaptchaError("Falha ao carregar reCAPTCHA."));
  }, []);

  return (
    <Container>
      <Row className="mt-5 justify-content-center align-items-center" >
        <Col md={3} className="text-center mb-2">
          {aboutMeData?.about_image ? (
            <Image
              src={aboutMeData.about_image}
              roundedCircle
              fluid
              className="shadow about-me-img"
              alt="Foto do dono do site"
              style={{ width: "200px", height: "200px", objectFit: "cover" }}
            />
          ) : (
            <div
              className="bg-secondary rounded-circle"
              style={{ width: "200px", height: "200px", opacity: 0.3 }}
            />
          )}
        </Col>

        <Col md={6}>
          <Card className="p-4 shadow h-100" style={{ minHeight: "300px" }}>
            <Card.Body className="d-flex flex-column">
              <Card.Title className="text-center mb-3">
                <h2>Sobre Mim</h2>
              </Card.Title>

              <Card.Text
                className="text-justify"
                dangerouslySetInnerHTML={{
                  __html: aboutMeData?.about_text || "<p class='text-muted'>Carregando informações...</p>",
                }}
              />
              <BuyMeACoffee className="text-end" />
              {aboutMeData?.social_links && (
                <div className="social-links mt-3" >
                  {Object.entries(aboutMeData.social_links).map(([platform, link]) => (
                    <a
                      key={platform}
                      href={link as string}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="me-2"
                      aria-label={`Link para ${platform}`}
                    >
                    {socialIconMap[platform] || <FaGlobe size={24} />}
                    </a>
                  ))}
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mt-5">
        <Col md={{ span: 6, offset: 3 }}>
          <div className="mb-5 mt-5 text-justify">
            <p className="text-muted">
              Este site é open source — sinta-se livre para explorar e usar partes do código.
              Estou aberto a colaborações em projetos de código aberto e também disponível para trabalho profissional.
              Se quiser trocar uma ideia ou propor algo, é só me chamar.
            </p>
          </div>

          {captchaError && <p className="text-danger">{captchaError}</p>}

          {siteKey && (
            <GoogleReCaptchaProvider
              reCaptchaKey={siteKey}
              scriptProps={{ async: true, defer: true }}
            >
              <ContactForm siteKey={siteKey} />
            </GoogleReCaptchaProvider>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default Sobre;

