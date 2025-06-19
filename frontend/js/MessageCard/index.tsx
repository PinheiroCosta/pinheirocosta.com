import React from "react";
import { Card } from "react-bootstrap";

interface MessageCardProps {
  variant: "primary" | "secondary" | "danger" | "success" | "warning" | "info" | "light";
  title: string;
  message: string;
  className?: string;
  children?: React.ReactNode;
}

const getTextColor = (variant: string) => {
  switch (variant) {
    case "primary":
    case "secondary":
    case "danger":
    case "success":
      return "white";
    case "warning":
    case "info":
    case "light":
    default:
      return "dark";
  }
};

const MessageCard: React.FC<MessageCardProps> = ({ variant, title, message, className, children }) => (
  <Card bg={variant} text={getTextColor(variant)} className="m-2">
    <Card.Body>
      <Card.Title>{title}</Card.Title>
      <Card.Text>{message}{children}</Card.Text>
    </Card.Body>
  </Card>
);

export const SuccessMessage = (props: Omit<MessageCardProps, "variant">) => (
  <MessageCard variant="success" {...props} />
);

export const ErrorMessage = (props: Omit<MessageCardProps, "variant">) => (
  <MessageCard variant="danger" {...props} />
);

export const WarningMessage = (props: Omit<MessageCardProps, "variant">) => (
  <MessageCard variant="warning" {...props} />
);

export const InfoMessage = (props: Omit<MessageCardProps, "variant">) => (
  <MessageCard variant="secondary" {...props} />
);

export default MessageCard;

