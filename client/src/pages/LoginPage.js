import React, { useEffect, useState } from "react";
import GoogleButton from 'react-google-button';
import axiosInstance from "../axiosApi.js";


const REACT_APP_GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID;


function LoginPage() {
  const [externalPopup, setExternalPopup] = useState(null);

  const connectClick = () => {
    const width = 500;
    const height = 400;
    const left = window.screenX + (window.outerWidth - width) / 2;
    const top = window.screenY + (window.outerHeight - height) / 2.5;
    const title = `WINDOW TITLE`;
    const url = makeAuthUrl();
    const popup = window.open(url, title, `width=${width},height=${height},left=${left},top=${top}`);
    setExternalPopup(popup);
  }
  function makeAuthUrl() {
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
    const redirectUri = 'auth/return';

    const scope = [
      'https://www.googleapis.com/auth/userinfo.email',
      'https://www.googleapis.com/auth/userinfo.profile'
    ].join(' ');

    const params = {
      response_type: 'code',
      client_id: REACT_APP_GOOGLE_CLIENT_ID,
      redirect_uri: `${location.origin}/${redirectUri}`, // eslint-disable-line no-restricted-globals
      prompt: 'select_account',
      access_type: 'offline',
      scope
    };

    const urlParams = new URLSearchParams(params).toString();
    return `${googleAuthUrl}?${urlParams}`
  };

  async function get(loginPayload, redirectUri) {
    axiosInstance.defaults.headers['Authorization'] = null
    let response = await axiosInstance.post(redirectUri, loginPayload) // eslint-disable-line no-restricted-globals
    return response
  }

  useEffect(() => {
    if (!externalPopup) {
      return;
    }

    const timer = setInterval(() => {
      if (!externalPopup) {
        timer && clearInterval(timer);
        return;
      }
      const currentUrl = externalPopup.location.href;
      if (!currentUrl) {
        return;
      }
      const searchParams = new URL(currentUrl).searchParams;
      const code = searchParams.get('code');
      if (code) {
        externalPopup.close();
        const redirectUri = 'auth/login/';
        const loginPayload = {
          "code": code,
          "redirectUri": `${location.origin}/auth/return` // eslint-disable-line no-restricted-globals
        }
        get(loginPayload, redirectUri).then((e) => {
          let payload = e.data;
          localStorage.setItem("accessToken", payload.accessToken);
          localStorage.setItem("refreshToken", payload.refreshToken);
          localStorage.setItem("user", JSON.stringify(payload.user));
          setExternalPopup(null);
          timer && clearInterval(timer);
          window.location.href = `${location.origin}/home/` // eslint-disable-line no-restricted-globals

        })
      }
    }, 3000)
  },
    [externalPopup]
  );

  const handleLogout = () => {
    try {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem("user");
      window.location.href = "/" // eslint-disable-line no-restricted-globals
    }
    catch (e) {
      console.log(e);
    }
  };


  return (
    localStorage.getItem("accessToken") ?
      <div className="loginpage">

        <button className="google-logout" onClick={handleLogout}>Logout</button>
      </div>
      :
      <div className="loginpage">
        <GoogleButton
          onClick={connectClick}
          label="Sign in with Google"
          disabled={!REACT_APP_GOOGLE_CLIENT_ID}
        />
      </div>
  );
}

export default LoginPage;