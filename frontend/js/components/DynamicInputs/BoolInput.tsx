import React from "react";
import { Form } from "react-bootstrap";

interface BoolInputProps {
  field: {
    name: string;
    label: string;
    required?: boolean;
  };
  value: boolean;
  onChange: (name: string, value: boolean) => void;
}

export const BoolInput: React.FC<BoolInputProps> = ({ field, value, onChange }) => {
  return (
    <Form.Group className="mb-1" controlId={field.name}>
      <Form.Check
        type="checkbox"
        label={field.label}
        name={field.name}
        checked={value}
        onChange={(e) => onChange(field.name, e.target.checked)}
      />
    </Form.Group>
  );
};

export default BoolInput;
