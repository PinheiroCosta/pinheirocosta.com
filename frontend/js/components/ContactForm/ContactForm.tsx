import { Form, Button, Card, Spinner } from "react-bootstrap";
import { FaPaperPlane } from "react-icons/fa";
import { SubjectEnum } from "../../api/types.gen";
import { ErrorMessage, SuccessMessage } from "../../MessageCard";
import type { useContactFormLogic } from "./useContactFormLogic";

type ContactFormProps = ReturnType<typeof useContactFormLogic> & {
    siteKey: string;
};

export default function ContactForm({
  siteKey,
  formData,
  setFormData,
  subjectOptions,
  isSending,
  success,
  error,
  handleSubmit,
}: ContactFormProps) {
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;

    if (name === "subject") {
      const isValidSubject = subjectOptions.some((opt) => opt.value === value);
      setFormData((prev) => ({
        ...prev,
        subject: isValidSubject ? (value as SubjectEnum) : "other",
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  if (success) {
    return (
        <SuccessMessage 
            title="Mensagem enviada!" 
            message="Obrigado pelo contato. Retornarei a mensagem assim que possível." 
        />
    );
  }

  return (
    <Card className="my-4 shadow-sm">
      <Card.Body>
        <Card.Title className="text-center">Contato</Card.Title>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3" controlId="name">
            <Form.Label>Nome</Form.Label>
            <Form.Control
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Seu nome"
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="email">
            <Form.Label>E-mail</Form.Label>
            <Form.Control
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="seu@email.com"
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="subject">
            <Form.Label>Assunto</Form.Label>
            <Form.Select
              name="subject"
              value={formData.subject}
              onChange={handleChange}
              required
            >
              {subjectOptions.map(({ value, label }) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Form.Select>
          </Form.Group>

          <Form.Group className="mb-3" controlId="message">
            <Form.Label>Mensagem</Form.Label>
            <Form.Control
              as="textarea"
              rows={5}
              name="message"
              value={formData.message}
              onChange={handleChange}
              required
              placeholder="Escreva sua mensagem aqui..."
            />
          </Form.Group>


      {error && <ErrorMessage title="Erro" message={error} />}
          <Button
            variant="primary"
            type="submit"
            disabled={isSending}
            className="d-flex align-items-center"
          >
            {isSending && <Spinner animation="border" size="sm" className="me-2" />}
            <FaPaperPlane style={{ marginRight: 8 }} />
            {isSending ? "Enviando..." : "Enviar"}
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
}

