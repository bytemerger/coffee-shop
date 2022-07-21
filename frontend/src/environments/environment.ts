/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'identeefy.eu', // the auth0 domain prefix
    audience: 'identeefy', // the audience set for the auth0 app
    clientId: 'NAOhedHox4CpCTP0Quyg7yNJO9DGzp6W', // the client id generated for the auth0 app
    callbackURL: 'https://localhost:8100', // the base url of the running ionic application. 
  }
};
