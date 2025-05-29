import React, { useEffect } from "react";
import { Form, Row, Col } from "react-bootstrap";

interface RadioInputProps {
  field: {
    name: string;
    label: string;
    options: { value: string; label: string }[];
    min_value?: number;
    max_value?: number;
  };
  value: Record<string, number>;
  possibleValues: number[];
  onChange: (name: string, updatedDict: Record<string, number>) => void;
}


export const RadioInput: React.FC<RadioInputProps> = ({ field, value, possibleValues, onChange }) => {
  useEffect(() => {
    const initialValue: Record<string, number> = { ...value };

    let updated = false;
    field.options.forEach((opt) => {
      const key = opt.value;
      if (initialValue[key] === undefined && field.min_value !== undefined) {
        initialValue[key] = parseInt(field.min_value as any, 10);
        updated = true;
      }
    });

    if (updated) {
      onChange(field.name, initialValue);
    }
  }, [field, value, onChange]);

  const handleChange = (key: string, val: number) => {
    onChange(field.name, { ...value, [key]: val });
  };

  return (
    <Form.Group 
        controlId={field.name} 
        className="mb-5 p-2"
        style={{ maxHeight: "15rem" }}
    >
      <Form.Label className="fw-bold">{field.label}</Form.Label>
      {field.options?.map((option) => {
        const attrKey = option.value;
        const attrLabel = option.label;

        return (
          <Row key={attrKey} className="align-items-center mx-0 my-0 small" >
            <Col xs={7} className="">
            <strong>{attrLabel}</strong>:
            </Col>
            <Col xs={5} className="d-flex flex-nowrap gap-1">
            {possibleValues.map((val) => (
              <Form.Check
                key={`radio${attrKey}-${val}`}
                inline
                type="radio"
                className="mx-0 justify-content-end"
                name={`${field.name}-${attrKey}`}
                checked={value?.[attrKey] === val}
                onChange={() => handleChange(attrKey, val)}
              />
            ))}
          </Col>
        </Row>
        );
      })}
    </Form.Group>
  );
};

export default RadioInput;
