import React from "react";
import { Nav } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

const CustomNavLink = ({ to, children }: { to: string; children: React.ReactNode }) => {
  const navigate = useNavigate();

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    navigate(to);
  };

  return (
    <Nav.Link href={to} onClick={handleClick}>
      {children}
    </Nav.Link>
  );
};

export default CustomNavLink;

