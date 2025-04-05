import React from "react";
import { Navbar, Nav, Container } from "react-bootstrap";
import CustomNavLink from "./CustomNavLink";
import logoMain from "../../assets/images/logo-website.svg";

const Header = () => {
  return (
    <Navbar collapseOnSelect expand="sm">
      <Container>
        <Nav
          className="align-items-center text-uppercase fw-bold mx-auto"
          style={{
          }}>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" className="m-1" />
          <Navbar.Collapse id="responsive-navbar-nav" >
          <CustomNavLink to="/" >Home</CustomNavLink>
          <CustomNavLink to="/blog">Blog</CustomNavLink>
          <Navbar.Brand className="mx-auto d-none d-md-block logo">
            <CustomNavLink to="/" >
              <img
                src={logoMain}
                alt="PinheiroCosta"
                style={{
                  borderRadius: "50%",
                  width: "180px",
                }}
              />
            </CustomNavLink>
          </Navbar.Brand>
          <CustomNavLink to="/tools" >Tools</CustomNavLink>
          <CustomNavLink to="/sobre">Sobre</CustomNavLink>
          </Navbar.Collapse>
        </Nav>
      </Container>
    </Navbar>
  );
};

export default Header;

