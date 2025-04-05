import React, { useState } from "react";
import { Container, Row, Col, Card, Form, Button, Alert } from "react-bootstrap";
import { ToolsService, ToolsRetrieveResponse, ProxyToolData, ProxyToolResponse } from "../api/services.gen";

interface GenericCalculatorToolProps {
  tool: ToolsRetrieveResponse;
}

const GenericCalculatorTool: React.FC<GenericCalculatorToolProps> = ({ tool }) => {
const [formData, setFormData] = useState<{ [key: string]: any }>({});
const [result, setResult] = useState<{ [key: string]: any } | null>(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);

const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
  const { name, value, type } = e.target;
  setFormData({
    ...formData,
    [name]: type === "number" ? parseFloat(value) : value,
  });
};

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setLoading(true);
  setError(null);
  setResult(null);

  try {
      const payload: ProxyToolData = formData;
      const data: ProxyToolResponse = await ToolsService.proxyTool({
        slug: tool.slug, 
        requestBody: payload
      });
      setResult(data);
  } catch (err) {
      setError("Erro ao executar ferramenta");
  } finally {
      setLoading(false);
  }
};

return (
  <Container className="d-flex justify-content-center align-items-start mt-5">
    <Col xs={12} md={8} lg={6}>
      <Card className="shadow p-4">
          <Card.Body>
            <Card.Title className="text-center mb-5">{tool.description}</Card.Title>

            {tool.outputs && (
                <div className="mb-4">
                {tool.outputs?.map((field) => {
                    const value = result?.[field.name] ?? (
                        field.type === "number" 
                        ? 0 
                        : field.type === "string" || field.type === "text" 
                        ? "" : "—"
                    );
                    const isNumeric = field.type === "number";
                    const isText = field.type === "string" || field.type === "text";
                    const displayValue =
                        value !== null && value !== undefined
                        ? value
                        : Isnumeric
                        ? 0
                        : isText
                        ? ""
                        : "-";

                    return (
                        <div
                            key={field.name}
                            className="mb-2 p-3 rounded"
                            style={{
                                backgroundColor: "#f8f9fa",
                                border: "1px solid #ced4da",
                                fontSize: "1.2rem",
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                            }}
                        >
                            <strong>{field.label}</strong>
                            <span>{displayValue}</span>
                        </div>
                    );
                })}
            </div>
            )}
            <Form onSubmit={handleSubmit}>
              {tool.inputs?.map((field) => (
                <Form.Group className="mb-3" controlId={field.name} key={field.name}>
                  <Form.Label>{field.label}</Form.Label>
                  {["text", "string"].includes(field.field_type) ? (
                    <Form.Control
                      as="textarea"
                      rows={12}
                      name={field.name}
                      value={formData[field.name] || ""}
                      onChange={handleChange}
                      required={field.required}
                      style={{ 
                        minHeight: "240px", 
                        fontFamily: "monospace", 
                        fontSize: "0.95rem",
                        verticalAlign: "top", 
                     }}
                    />
                  ) : (
                    <Form.Control
                      type={field.field_type === "number" ? "number" : "text"}
                      name={field.name}
                      value={formData[field.name] || ""}
                      onChange={handleChange}
                      required={field.required}
                    />
                  )}
                </Form.Group>
              ))}

              <Button variant="primary" type="submit" className="w-100" disabled={loading}>
                {loading ? "Executando..." : "Executar"}
              </Button>
            </Form>

            {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
          </Card.Body>

      </Card>
    </Col>
  </Container>
);
};

export default GenericCalculatorTool;

