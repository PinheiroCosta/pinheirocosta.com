import React, { useEffect, useState } from "react";
import { Container, Row, Col, Spinner } from "react-bootstrap";
import { MotdService, MotdConfigService } from "../api/services.gen";

const Motd = () => {
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMotd = async () => {
      let messageHtml = "<p><em>Hoje não temos uma mensagem especial... Mas segue o jogo!</em></p>";
  
      try {
        const config = await MotdConfigService.motdConfigSingletonRetrieve();
        if (config?.message_override_text) {
          messageHtml = config.message_override_text;
        } else {
          const motds = await MotdService.motdRandomRetrieve();
          if (motds.text) {
            messageHtml = motds.text;
          }
        }
      } catch (error: any) {
        const status = error?.status;
  
        if (status === 404) {
          try {
            const motds = await MotdService.motdRandomRetrieve();
            if (motds.text) {
              messageHtml = motds.text;
            }
          } catch (innerError) {
            console.error("Erro ao buscar MOTD aleatória:", innerError);
          }
        } else {
          console.error("Erro inesperado ao buscar MOTDConfig:", error);
        }
      } finally {
        setMessage(messageHtml);
        setLoading(false);
      }
    };
  
    fetchMotd();
  }, []);

  return (
    <section className="philosophy-section mb-5 text-center">
      <Container>
        <Row>
          <Col md={4} className="my-auto">
            <div className="d-flex mb-2 justify-content-end">
              <div title="Mensagem do dia" className="px-2 py-1 fw-bold fs-5 border border-dark rounded">
                MOTD
              </div>
            </div>
          </Col>
          <Col md={5} className="text-start ">

            {loading ? (
              <Spinner animation="border" variant="secondary" />
            ) : (
              <div
                className="fs-6 text-muted"
                dangerouslySetInnerHTML={{ __html: message || "" }}
              />
            )}
          </Col>
        </Row>
      </Container>
    </section>
  );
};

export default Motd;

