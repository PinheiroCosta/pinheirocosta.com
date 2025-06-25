import React, { useState } from "react";
import { FaPlay, FaRedo } from "react-icons/fa";
import { Container, Col, Card, Form, Button } from "react-bootstrap";
import { ToolsRetrieveResponse, ProxyToolData, ProxyToolResponse } from "../../api/types.gen";
import { ToolsService } from "../../api/services.gen";
import { useToolSubmit } from "../../hooks/useToolSubmit";
import { renderInputField } from "../DynamicInputs/InputDispatcher";
import OutputRenderer from "../DynamicOutputs/OutputRenderer";
import { ErrorMessage } from "../../MessageCard";


interface DynamicToolFormProps {
  tool: ToolsRetrieveResponse;
}

const getInitialFormData = (tool: ToolsRetrieveResponse): { [key: string]: any } => {
  const initialData: { [key: string]: any } = {};
  tool.inputs.forEach((field) => {
    switch (field.data_type) {
      case "int":
        initialData[field.name] = 0;
        break;
      case "bool":
        initialData[field.name] = false;
        break;
      default:
        initialData[field.name] = "";
    }
  });
  return initialData;
};

const DynamicToolForm: React.FC<DynamicToolFormProps> = ({ tool }) => {
  const [formData, setFormData] = useState<{ [key: string]: any }>(() => getInitialFormData(tool));
  const { submit, loading, result, error, reset } = useToolSubmit(tool);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const parsedValue = type === "number" ? parseFloat(value) : value;
    setFormData(prev => ({ ...prev, [name]: parsedValue }));
  };

  const handleResetForm = () => {
    setFormData(getInitialFormData(tool));
    reset();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await submit(formData);
  }
  
  const isManyInputs = tool.inputs.length > 15;

  return (
    <Container className="d-flex justify-content-center align-items-start mt-5">
      <Col xs={12} md={10} lg={isManyInputs ? 10 : 5} xl={isManyInputs ? 9 : undefined}>
        <Card className="shadow">
          <Card.Header className="text-center p-1 mb-1 fs-3 fw-bold">
            {tool.name.charAt(0).toUpperCase() + tool.name.slice(1)}
          </Card.Header>
          <Card.Body>
            <OutputRenderer outputs={tool.outputs} result={result} />
            {error && <ErrorMessage title="Erro" message={error}></ErrorMessage>}

            <Form onSubmit={handleSubmit}>
              {isManyInputs ? (
                <div className="row">
                  {[0, 1, 2].map((colIndex) => (
                    <div className="col-md-4" key={`col-${colIndex}`}>
                      {tool.inputs
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
                tool.inputs.map((field) => (
                  <React.Fragment key={`${field.name}-${field.id}`}>
                    {renderInputField({ field, formData, setFormData, handleChange })}
                  </React.Fragment>
                ))
              )}

              <Button type="submit" className="w-100 fs-4" disabled={loading}>
                {loading ? "Executando..." : <> <FaPlay className="me-2" /> Executar </>}
              </Button>
              <Button
                className="w-100 fs-4 mt-2"
                disabled={loading}
                onClick={handleResetForm}
              >
                {loading ? "Executando..." : <> <FaRedo className="me-2" /> Limpar Formulário </>}
              </Button>
            </Form>

          </Card.Body>
        </Card>
      </Col>
    </Container>
  );
};

export default DynamicToolForm;

