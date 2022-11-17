import './App.css';
import React, { useState, useEffect} from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import {
  BrowserRouter as Router,
  Switch,
  Redirect,
  Route,
  Link,
} from "react";
import Cookies from "js-cookie";

const AuthApi = React.createContext();
const TokenApi = React.createContext();


function App(){
    const [auth, setAuth] = useState(false);
    const [token, setToken] = useState("");
    const readCookie = () => {
        let token = Cookies.get("token");
        if (token) {
            setAuth(true);
            setToken(token);
    }
  };

    React.useEffect(() => {
    readCookie();
  }, []);

    return (
           <>
      <AuthApi.Provider value={{ auth, setAuth }}>
        <TokenApi.Provider value={{ token, setToken }}>
          <Router>
            <div>
              <nav>
                <ul>
                  {!auth ? (
                    <li>
                      <Link to="/register">Regsiter</Link>
                    </li>
                  ) : (
                    <></>
                  )}
                  {!auth ? (
                    <li>
                      <Link to="/login">Login</Link>
                    </li>
                  ) : (
                    <></>
                  )}
                  <li>
                    <Link to="/">Home</Link>
                  </li>
                </ul>
              </nav>
              <Routes />
            </div>
          </Router>
        </TokenApi.Provider>
      </AuthApi.Provider>
    </>
  );
}
const Routes = () => {
  const Auth = React.useContext(AuthApi);
  return (
    <Switch>
      <Route path="/register">
        <Register />
      </Route>
      <ProtectedLogin
        path="/login"
        auth={Auth.auth}
        component={Login}
      ></ProtectedLogin>
      <ProtectedRoute
        path="/"
        auth={Auth.auth}
        component={Home}
      ></ProtectedRoute>
    </Switch>
  );
};
const Home = () => {
  const [data, setData] = useState("");
  const Auth = React.useContext(AuthApi);
  const Token = React.useContext(TokenApi);
  const handleonclick = () => {
    Auth.setAuth(false);
    Cookies.remove("token");
  };
  let toke = Token.token;
  const headers = {
    Authorization: `Bearer ${toke}`,
  };
  const getdata = async () => {
    let res = await axios
      .get("http://127.0.0.1:8000/", { headers })
      .then((response) => {
        return response.data.data;
      });
    return res;
  };
  React.useEffect(async () => {
    let x = await getdata();
    setData(x);
    console.log(x);
  }, [getdata]);
  return (
    <>
      <h2>Home</h2>
      <button onClick={handleonclick}>Logout</button>
      <h1>{data}</h1>
    </>
  );
};

function Register() {
  const [name, setName] = useState("");
  const [company, setCompany] = useState("");
  const [password, setPassword] = useState("");
  const handleSubmit = (evt) => {
    evt.preventDefault();
    const data = {
      username: name,
      company: company,
      password: password,
    };
    axios
      .post("http://127.0.0.1:8000/create", data)
      .then((response) => {
        console.log(response);
        alert(response);
      })
      .catch((error) => {
        alert(error);
      });
  };
  return (
    <>
      <form
        style={{
          marginTop: "100px",
          marginLeft: "50px",
          border: "solid 1px",
          width: "max-content",
          borderColor: "green",
        }}
        onSubmit={handleSubmit}
      >
        <div style={{ textAlign: "center" }}>Register Yourself</div>
        <br />
        <label>Username:</label>
        <input
          type="text"
          className="username"
          value={name}
          onChange={(e) => setName(e.target.value)}
        ></input>
        <br />
        <br />
        <label>Company: </label>
        <input
          type="text"
          className="company"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
        ></input>
        <br />
        <br />
        <label>Password: </label>
        <input
          type="password"
          className="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        ></input>
        <br />
        <br />
        <div style={{ textAlign: "center" }}>
          <input type="submit" value="Submit" />
        </div>
      </form>
    </>
  );
}

const Login = () => {
  const Auth = React.useContext(AuthApi);
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const handleSubmit = async (evt) => {
    if (evt) {
      evt.preventDefault();
    }
    const data = {
      username: name,
      password: password,
    };
    const news = async () => {
      let res = await axios
        .post("http://127.0.0.1:8000/login", data)
        .then((response) => {
          console.log(response);
          Cookies.set("token", response.data.access_token);
          return response;
        })
        .catch((error) => {
          console.log(error.message);
        });
      return res;
    };
    let x = await news();
    if (x) {
      window.location.reload();
    }
  };
  return (
    <>
      <form
        style={{
          marginTop: "100px",
          marginLeft: "50px",
          border: "solid 1px",
          width: "max-content",
          borderColor: "green",
        }}
        onSubmit={handleSubmit}
      >
        <div style={{ textAlign: "center" }}>Login</div>
        <br />
        <label>Username:</label>
        <input
          type="text"
          className="username"
          value={name}
          onChange={(e) => setName(e.target.value)}
        ></input>
        <br />
        <br />
        <label>Password: </label>
        <input
          type="password"
          className="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        ></input>
        <br />
        <br />
        <div style={{ textAlign: "center" }}>
          <input type="submit" value="Submit" />
        </div>
      </form>
    </>
  );
};
const ProtectedRoute = ({ auth, component: Component, ...rest }) => {
  return (
    <Route
      {...rest}
      render={() => (auth ? <Component /> : <Redirect to="/login" />)}
    />
  );
};
const ProtectedLogin = ({ auth, component: Component, ...rest }) => {
  return (
    <Route
      {...rest}
      render={() => (!auth ? <Component /> : <Redirect to="/" />)}
    />
  );
};
export default App;
