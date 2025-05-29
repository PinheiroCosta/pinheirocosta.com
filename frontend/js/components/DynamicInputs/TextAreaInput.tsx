import React from "react";
import { Form } from "react-bootstrap";

interface TextAreaInputProps {
  name: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  rows?: number;
  disabled?: boolean;
}

export const TextAreaInput: React.FC<TextAreaInputProps> = ({
  name,
  label,
  value,
  onChange,
  rows = 4,
  disabled = false,
}) => {
  return (
    <Form.Group className="mb-3" controlId={`textarea-${name}`}>
      <Form.Label>{label}</Form.Label>
      <Form.Control
        as="textarea"
        name={name}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={rows}
        disabled={disabled}
      />
    </Form.Group>
  );
};

export default TextAreaInput;

