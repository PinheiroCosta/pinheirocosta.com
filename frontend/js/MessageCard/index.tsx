import React from "react";
import { Card } from "react-bootstrap";

interface MessageCardProps {
  variant: "success" | "danger" | "warning" | "info";
  title: string;
  message: string;
}

const getTextColor = (variant: string) => {
  switch (variant) {
    case "danger":
    case "success":
      return "white";
    case "warning":
    case "info":
    default:
      return "dark";
  }
};

const MessageCard: React.FC<MessageCardProps> = ({ variant, title, message }) => (
  <Card bg={variant} text={getTextColor(variant)} className="m-2">
    <Card.Body>
      <Card.Title>{title}</Card.Title>
      <Card.Text>{message}</Card.Text>
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
  <MessageCard variant="info" {...props} />
);

export default MessageCard;

