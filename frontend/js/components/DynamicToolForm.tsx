import React, { useState } from "react";
import { Container, Col, Card, Form, Button, Alert } from "react-bootstrap";
import { ToolsRetrieveResponse, ProxyToolData, ProxyToolResponse } from "../api/types.gen";
import { ToolsService } from "../api/services.gen";

interface DynamicToolFormProps {
  tool: ToolsRetrieveResponse;
}

const DynamicToolForm: React.FC<DynamicToolFormProps> = ({ tool }) => {
  const [formData, setFormData] = useState<{ [key: string]: any }>({});
  const [result, setResult] = useState<ProxyToolResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const parsedValue = type === "number" ? parseFloat(value) : value;
    setFormData(prev => ({ ...prev, [name]: parsedValue }));
  };

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const payload: ProxyToolData ={
        ...formData,
        slug: tool.slug,
      };
      const data = await ToolsService.proxyTool({
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

const renderInputField = (field: any) => {
  const widget = field.widget_type || field.data_type;
  const commonProps = {
    name: field.name,
    value: formData[field.name] ?? "",
    onChange: handleChange,
    required: field.required,
  };

  switch (widget) {
    case "checkbox":
    case "bool":
      return (
        <Form.Group className="mb-3" controlId={field.name} key={field.name}>
          <Form.Check
            type="checkbox"
            label={field.label}
            name={field.name}
            checked={
                formData[field.name] !== undefined ? formData[field.name] : true
            }
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                [field.name]: e.target.checked,
              }))
            }
          />
        </Form.Group>
      );

    case "select":
      return (
        <Form.Group className="mb-3" controlId={field.name} key={field.name}>
          <Form.Label>{field.label}</Form.Label>
          <Form.Select
              name={field.name}
              value={formData[field.name] ?? ""}
              onChange={handleSelectChange}
              required={field.required}
            >
              <option value="">Selecione uma opção</option>
              {field.options?.map((opt: any) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </Form.Select>
        </Form.Group>
      );

    case "textarea":
    case "text":
      return (
        <Form.Group className="mb-3" controlId={field.name} key={field.name}>
          <Form.Label>{field.label}</Form.Label>
          <Form.Control
            as="textarea"
            rows={12}
            {...commonProps}
            style={{
              minHeight: "240px",
              fontFamily: "monospace",
              fontSize: "0.95rem",
              verticalAlign: "top",
            }}
          />
        </Form.Group>
      );

    case "number":
    case "int":
    case "float":
      return (
        <Form.Group className="mb-3" controlId={field.name} key={field.name}>
          <Form.Label>{field.label}</Form.Label>
          <Form.Control type="number" {...commonProps} />
        </Form.Group>
      );

    default: // fallback para input text padrão
      return (
        <Form.Group className="mb-3" controlId={field.name} key={field.name}>
          <Form.Label>{field.label}</Form.Label>
          <Form.Control type="text" {...commonProps} />
        </Form.Group>
      );
  }
};

  const getDisplayValue = (value: any, fieldType: string): React.ReactNode => {
    if (value !== undefined && value !== null) {
        return value;
    }
    
    switch (fieldType) {
        case "string":
        case "text":
            return <textarea />;
        case "int":
        case "float":
            return <input type="number" />;
        case "boolean":
            return <input type="checkbox" />;
        case "select":
            return <select>...</select>;
    }
  };

  const renderOutputField = (field: any) => {
    const value = result?.[field.name];
    const displayValue = getDisplayValue(value, field.field_type);

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
  };

  return (
    <Container className="d-flex justify-content-center align-items-start mt-5">
      <Col xs={12} md={8} lg={6}>
        <Card className="shadow p-4">
          <Card.Body>
            <Card.Title className="text-center mb-5">{tool.name.charAt(0).toUpperCase() + tool.name.slice(1)}</Card.Title>

            {tool.outputs?.length > 0 && (
              <div className="mb-4">
                {Array.isArray(tool.outputs) &&
                     (tool.outputs as any[]).map(renderOutputField)}
              </div>
            )}

            <Form onSubmit={handleSubmit}>
              {Array.isArray(tool.inputs) &&
                (tool.inputs as any[]).map(renderInputField)}

              <Button
                variant="primary"
                type="submit"
                className="w-100"
                disabled={loading}
              >
                {loading ? "Calculando..." : "Calcular"}
              </Button>
            </Form>

            {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
          </Card.Body>
        </Card>
      </Col>
    </Container>
  );
};

export default DynamicToolForm;

