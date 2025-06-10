import React, { useEffect, useState, useRef } from "react";
import { Form, Button, Row, Col, Card } from "react-bootstrap";
import { ContatoProfissionalService } from "../api/services.gen";
import type { ContatoProfissionalCreateData, SubjectEnum } from "../api/types.gen";
import { useSearchParams } from "react-router-dom";

function isValidSubject(value: string, validSubjects: Record<string, string>): value is SubjectEnum {
  return Object.keys(validSubjects).includes(value);
}

export function ContactForm() {
  const [formData, setFormData] = useState<ContatoProfissionalCreateData>({
    requestBody: {
      name: "",
      email: "",
      subject: "hire",
      message: "",
      utm_source: "",
      utm_medium: "",
      utm_campaign: "",
    },
  });

  const [subjects, setSubjects] = useState<Record<string, string>>({});
  const [isSending, setIsSending] = useState(false);
  const [resultStatus, setResultStatus] = useState<"idle" | "success" | "error">("idle");
  const [searchParams] = useSearchParams();
  const alertRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    setFormData((prev) => ({
      requestBody: {
        ...prev.requestBody,
        utm_source: searchParams.get("utm_source") ?? "",
        utm_medium: searchParams.get("utm_medium") ?? "",
        utm_campaign: searchParams.get("utm_campaign") ?? "",
      },
    }));

    ContatoProfissionalService.contatoProfissionalSubjectsRetrieve()
      .then(setSubjects)
      .catch((err) => {
        console.error("Erro ao carregar assuntos:", err);
      });
  }, [searchParams]);

  useEffect(() => {
    if (resultStatus !== "idle" && alertRef.current) {
      const timer = setTimeout(() => setResultStatus("idle"), 5000);
      return () => clearTimeout(timer);
    }
  }, [resultStatus]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    const newValue =
      name === "subject" && !isValidSubject(value, subjects)
        ? ("" as SubjectEnum)
        : value;

    setFormData((prev) => ({
      requestBody: {
        ...prev.requestBody,
        [name]: newValue,
      },
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSending) return;

    setIsSending(true);
    setResultStatus("idle");

    try {
      await ContatoProfissionalService.contatoProfissionalCreate(formData);
      setResultStatus("success");
      setFormData({
        requestBody: {
          name: "",
          email: "",
          subject: "hire",
          message: "",
          utm_source: "",
          utm_medium: "",
          utm_campaign: "",
        },
      });
    } catch (err) {
      console.error("Erro ao enviar:", err);
      setResultStatus("error");
    } finally {
      setIsSending(false);
    }
  };

  return (
    <Card className="p-4 shadow-sm border-0 mt-5">
      <h3 className="mb-4 text-center">Entre em Contato</h3>

      {resultStatus !== "idle" && (
        <div
          ref={alertRef}
          className={`text-center mb-3 py-2 px-3 rounded-3 fw-medium ${
            resultStatus === "success" ? "bg-success text-white" : "bg-danger text-white"
          }`}
        >
          {resultStatus === "success"
            ? "Mensagem enviada com sucesso!"
            : "Erro ao enviar mensagem. Tente novamente."}
        </div>
      )}

      <Form onSubmit={handleSubmit}>
        <Row>
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>Nome</Form.Label>
              <Form.Control
                required
                type="text"
                name="name"
                value={formData.requestBody.name}
                onChange={handleChange}
                className="rounded-3"
              />
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                required
                type="email"
                name="email"
                value={formData.requestBody.email}
                onChange={handleChange}
                className="rounded-3"
              />
            </Form.Group>
          </Col>
        </Row>

        <Form.Group className="mb-3">
          <Form.Label>Assunto</Form.Label>
          <Form.Select
            required
            name="subject"
            value={formData.requestBody.subject}
            onChange={handleChange}
            className="rounded-3"
          >
            {Object.entries(subjects).map(([key, label]) => (
              <option key={key} value={key}>
                {label}
              </option>
            ))}
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Mensagem</Form.Label>
          <Form.Control
            required
            as="textarea"
            rows={5}
            name="message"
            value={formData.requestBody.message}
            onChange={handleChange}
            className="rounded-3"
          />
        </Form.Group>

        <div className="d-grid">
          <Button variant="primary" type="submit" disabled={isSending}>
            {isSending ? (
              <>
                <span
                  className="spinner-border spinner-border-sm me-2"
                  role="status"
                  aria-hidden="true"
                ></span>
                Enviando...
              </>
            ) : (
              "Enviar"
            )}
          </Button>
        </div>
      </Form>
    </Card>
  );
}

export default ContactForm;

