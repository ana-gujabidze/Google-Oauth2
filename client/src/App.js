import 'bootstrap/dist/css/bootstrap.min.css';
import React, { Component } from "react";
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { Route, Switch } from "react-router-dom";
import './App.css';
import RouteGuard from "./components/RouteGuard";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import LoremIpsum from "./pages/LoremIpsum";

class App extends Component {
    render() {
        return (
            <div className="site">
            <Navbar expand="md">
                <Container fluid>
                  <Navbar.Brand href={"/home/"}>Ana's OAuth2 & JWT App</Navbar.Brand>
                  <Navbar.Toggle aria-controls="navbar" />
                  <Navbar.Collapse id="navbar">
                    <Nav className="ml-auto">
                      <NavDropdown
                        id="nav-dropdown"
                        title={localStorage.getItem("accessToken")?JSON.parse(localStorage.getItem("user")).email:"Anonymous"}
                        menuVariant="dark"
                      >
                        <NavDropdown.Item href={"/home/"}>Homepage</NavDropdown.Item>
                        <NavDropdown.Item href={"/lorem_ipsum/"}>Lorem Ipsum</NavDropdown.Item>
                        <NavDropdown.Divider />
                        <NavDropdown.Item href={"/"}>Login/Logout</NavDropdown.Item>
                      </NavDropdown>
                    </Nav>
                  </Navbar.Collapse>
                </Container>
              </Navbar>
                <main>
                    <Switch>
                        <RouteGuard exact path={"/home/"} component={HomePage}/>
                        <RouteGuard exact path={"/lorem_ipsum/"} component={LoremIpsum}/>
                        <Route path={"/"} component={LoginPage}/>
                    </Switch>
                </main>
            </div>
        );
    }
}

export default App;
