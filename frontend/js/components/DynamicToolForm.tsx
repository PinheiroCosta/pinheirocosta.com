import React, { useState } from "react";
import { Container, Col, Card, Form, Button, Alert } from "react-bootstrap";
import { ToolsRetrieveResponse, ProxyToolData, ProxyToolResponse } from "../api/types.gen";
import { ToolsService } from "../api/services.gen";
import { renderInputField } from "./DynamicInputs/InputDispatcher";


interface DynamicToolFormProps {
  tool: ToolsRetrieveResponse;
}

const generateFieldKey = (field: any): string =>
  `${field.name}__${field.label.replace(/\s+/g, "_").toLowerCase()}__${field.id}`;

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
      const payload: ProxyToolData = {
        ...formData,
        slug: tool.slug,
      };
      const data = await ToolsService.proxyTool({
        slug: tool.slug,
        requestBody: payload,
      });
      if (tool.slug === "masquerade" && data.ficha) {
        const ficha = data.ficha;
        const newFormData: { [key: string]: any } = {};

        for (const input of tool.inputs) {
            const path = input.name.split(".");
            let current: any = ficha;

            for (const segment of path) {
                if (current && segment in current) {
                    current = current[segment];
                } else {
                    current = undefined;
                    break;
                }
            }
            if (current !== undefined) {
                newFormData[input.name] = current;
            }
        }
        setFormData(prev => ({ ...prev, ...newFormData }));
      }
      setResult(data);
    } catch {
      setError("Erro ao executar ferramenta");
    } finally {
      setLoading(false);
    }
  };


  const getDisplayValue = (value: any, fieldType: string): React.ReactNode => {
    if (value === undefined || value === null) return "";

    switch (fieldType) {
      case "int":
      case "float":
        return new Intl.NumberFormat("pt-BR").format(Number(value));
      case "boolean":
        return value ? "Sim" : "Não";
      case "date":
      case "datetime":
        try {
          const date = new Date(value);
          return date.toLocaleDateString("pt-BR", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          });
        } catch {
          return String(value);
        }
      default:
        return String(value);
    }
  };

  const renderOutputField = (field: any) => {
    const value = result?.[field.name];
    const displayValue = Number(getDisplayValue(value, field.field_type)) || 0;

    return (
      <div
        key={`render-output-${field.name}`}
        className="mb-1 p-1 rounded"
        style={{
          backgroundColor: "#f8f9fa",
          border: "1px solid #aeb4ba",
          fontSize: "1.0rem",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <strong>{field.label}:</strong>
        <span>{displayValue}</span>
      </div>
    );
  };

  const isManyInputs = tool.inputs.length > 15;

  return (
    <Container className="d-flex justify-content-center align-items-start mt-5">
      <Col xs={12} md={10} lg={isManyInputs ? 10 : 5} xl={isManyInputs ? 9 : undefined}>
        <Card className="shadow">
          <Card.Header className="text-center p-1 mb-1 fs-3 fw-bold">
            {tool.name.charAt(0).toUpperCase() + tool.name.slice(1)}
          </Card.Header>
          <Card.Body>
            {tool.outputs?.length > 0 && (
              <div className="mb-4">
                {(tool.outputs as any[]).map((field) => (
                    <React.Fragment key={`${field.name}-${field.id}`}>
                    {renderOutputField(field)}
                    </React.Fragment>
                ))}
              </div>
            )}
            <Form onSubmit={handleSubmit}>
                {tool.inputs.length > 15 ? (
                    <div className="row">
                    {[0, 1, 2].map((colIndex) => (
                        <div className="col-md-4" key={`col-${colIndex}`}>
                        {(tool.inputs as any[])
                            .filter((_, index) => index % 3 === colIndex)
                            .map((field) => (
                                <React.Fragment key={`${field.name}-${field.id}`}>
                                {renderInputField({ field, formData, setFormData, handleChange })}
                                </React.Fragment>
                            ))}
                        </div>
                    ))}
                    </div>
                ) : (
                (tool.inputs as any[]).map((field) => (
                  <React.Fragment key={`${field.name}-${field.id}`}>
                    {renderInputField({ field, formData, setFormData, handleChange })}
                  </React.Fragment>
                ))
                )}
              <Button type="submit" className="w-100 fs-4" disabled={loading}>
                {loading ? "Executando..." : "Executar"}
              </Button>
              <Button className="w-100 fs-4 mt-2" disabled={loading} onClick={() => setFormData({})}>
                {loading ? "Executando..." : "Limpar Formulário"}
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
