import React from 'react';
import { Redirect, Route } from 'react-router-dom';
 
const RouteGuard = ({ component: Component, ...rest }) => {
 
   return (
       <Route {...rest}
           render={props => (
            localStorage.getItem("accessToken") ?
                   <Component {...props} />
                   :
                   <Redirect to={{ pathname: '/' }} />
           )}
       />
   );
};
 
export default RouteGuard;